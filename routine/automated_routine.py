import time
import atexit
import sure_servo_2_control as sv2_ctrl
import sure_servo_2_constants as sv2_const
import yaskawa_vfd_control as vfd_ctrl
import test_bench_constants as tb_const
from pymodbus.client import ModbusTcpClient
from tkinter import *
import conveyors
from fanucpy import Robot
import multiprocessing

def check_prox_sensors(protos_x):
    data = protos_x.read_discrete_inputs(tb_const.PROX_1_ADDR, 2)
    try:
        prox_1_sense = data.bits[0]
        prox_2_sense = data.bits[1]
        if(prox_1_sense and prox_2_sense):
            print("Both sensors activated.")
            return True
        elif(prox_1_sense):
            print("Only sensor 1 activated.")
        elif(prox_2_sense):
            print("Only sensor 2 activated")
        else:
            print("Nothing detected.")
        return False
    except AttributeError:
        return False

def exit_routine(servo:sv2_ctrl.Sv2Servo, vfd:vfd_ctrl.YaskawaVfd):
    print("Exiting...")
    vfd.exit_handler()
    servo.exit_handler()

def tcp_client_initialization(host):
    protos_x = ModbusTcpClient(host)
    print('Connecting to Protos X...')
    while(not protos_x.connect()):
        print('No available connections.')
        while(input('Enter "Y" when ready: ') != 'Y'):
            pass
        print('Attempting to connect...')
    print('Connected.')
    return protos_x

def check_ready():
    width = int(input("Width (mm): "))
    height = int(input("Height (mm): "))
    while (input('Input "Y" to start: ') != 'Y'):
        pass
    return width, height

def start_motor(move_direction, path:sv2_ctrl.Sv2ConstSpeed, speed):
    print(f"starting motor...{move_direction}")
    if move_direction == "Forward":
        path.change_speed(speed)
    else:
        path.change_speed(-speed)
    path.trigger_path()
    
def update_origin(path:sv2_ctrl.Sv2PointPoint, position, move_arm_event:multiprocessing.Event):
    path.change_position(position)
    move_arm_event.set()
    
def move_arm(quit_event, move_arm_event, pos, vel, accel):
    robot = Robot(
        robot_model="Fanuc",
        host=tb_const.ROBOT_HOST,
        port=18735,
        ee_DO_type="RDO",
        ee_DO_num=7,
        )
    robot.connect()
    while not quit_event.is_set():
        move_arm_event.wait()
        if tb_const.MIN_X < pos[0] < tb_const.MAX_X and tb_const.MIN_Y < pos[1] < tb_const.MAX_Y:
            try: 
                robot.move(
                    "pose",
                    vals=pos,
                    velocity=vel.value,
                    acceleration=accel.value,
                    cnt_val=0,
                    linear=False
                )
            except:
                pass
        move_arm_event.clear()
        print(robot.get_curpos())
    robot.disconnect()
        
def pick_conveyor_init():
    pick_conveyor = conveyors.EnipServoConveyor(
        top_length=1400,
        max_speed=113000,
        turn_circum=121,
        servo_addr=tb_const.SERVO_DRIVE_HOST
        )
    pick_conveyor.servo.clear_alarms()
    pick_conveyor.servo.enable_servo()
    pick_speed_mon = sv2_ctrl.Sv2Monitor(
        servo=pick_conveyor.servo,
        mon_num=1,
        mon_type=sv2_const.MON_SPEED_FEEDBACK_TYPE
        )
    pick_pos_mon = sv2_ctrl.Sv2Monitor(
        servo=pick_conveyor.servo,
        mon_num=2,
        mon_type=sv2_const.MON_POS_FEEDBACK_TYPE
    )
    return pick_conveyor, pick_speed_mon, pick_pos_mon

def feed_conveyor_init():
    feed_conveyor = vfd_ctrl.YaskawaVfd(ip_addr=tb_const.VFD_HOST)
    feed_conveyor.change_freq(percentage=100)
    return feed_conveyor

def add_point(paths, arm_mover):
    paths.append(arm_mover[:])
    print(paths)

def automated_routine():
    pick_conveyor, pick_speed_mon, pick_pos_mon = pick_conveyor_init()
    feed_conveyor = feed_conveyor_init()
    protos_x = tcp_client_initialization(tb_const.PROTOS_X_HOST)
    atexit.register(exit_routine, servo=pick_conveyor.servo, vfd=feed_conveyor)

    next_window_event = multiprocessing.Event()
    move_arm_event = multiprocessing.Event()
    quit_event = multiprocessing.Event()
    
    width, height = check_ready()

    origin = [tb_const.DEFAULT_X, tb_const.DEFAULT_Y, height-95, 180.0, 0.0, 0.0]
    arm_mover = multiprocessing.Array('d', range(6))
    vel = multiprocessing.Value('d', 100)
    accel = multiprocessing.Value('d', 100)
    
    for i in range(6):
        arm_mover[i] = origin[i]
    arm_process = multiprocessing.Process(target=move_arm, args=(quit_event, move_arm_event, arm_mover, vel, accel))
    arm_process.start()
    
    pick_conveyor.backwards_constant.trigger_path()
    feed_conveyor.start_motor_forwards()
    
    move_arm_event.set()
    while not check_prox_sensors(protos_x):
        pass
    pick_conveyor.stop.trigger_path()
    feed_conveyor.stop_motor()
    while pick_speed_mon.check_value() != 0:
        pass
    time.sleep(1)
    pick_conveyor.set_home()
    
    jog_path = sv2_ctrl.Sv2ConstSpeed(pick_conveyor.servo, 16)
    jog_path.change_acc(1000)

    jog_conveyor_window = Tk()
    
    for test_direction in ("Forward", "Backward"):
        button = Button(jog_conveyor_window, text=test_direction)
        button.pack(side=LEFT)
        button.bind('<ButtonPress-1>', lambda event, dir=test_direction:
            start_motor(dir, jog_path, 50))
        button.bind('<ButtonRelease-1>', lambda event: pick_conveyor.stop.trigger_path())

    button = Button(jog_conveyor_window, text= "Set end")
    button.pack(side = LEFT)
    button.bind('<ButtonPress-1>', lambda event: update_origin(pick_conveyor.forwards_distance, pick_pos_mon.check_value(), next_window_event))
    
    jog_conveyor_window.attributes("-topmost", True)
    jog_conveyor_window.lift()
    
    while not next_window_event.is_set():
        jog_conveyor_window.update_idletasks()
        jog_conveyor_window.update()
        move_arm_event.set()
        position = pick_pos_mon.check_value()
        
        turns = position / sv2_const.E_GEAR_DEN
        distance = pick_conveyor.turn_circum * turns
        diagonal = (width ** 2 * 2) ** 0.5 / 2 - 95
        max_pos = round((((tb_const.MAX_X - origin[0]) ** 2 * 2) ** 0.5 - diagonal )/ pick_conveyor.turn_circum * sv2_const.E_GEAR_DEN)
        # print(max_pos)
        reset_path = sv2_ctrl.Sv2PointPoint(pick_conveyor.servo, 15, sv2_const.CMD_ABS, max_pos, 100)
        reset_path.change_acc(1000)
        print(position)
        if position >= 4000000000:
            pick_conveyor.stop.trigger_path()
            while pick_speed_mon.check_value() > 0:
                pass
            pick_conveyor.set_home()
        elif 4000000000 >= position >= max_pos:
            pick_conveyor.stop.trigger_path()
            position = tb_const.MAX_CONVEYOR_POSITION
            reset_path.trigger_path()
        if max_pos >= position >= 0:
            # turns = position / sv2_const.E_GEAR_DEN
            # distance = pick_conveyor.turn_circum * turns
            # diagonal = (width ** 2 * 2) ** 0.5 / 2 - 95
            arm_mover[0] = origin[0] + (((distance + diagonal) ** 2) / 2) ** 0.5
            arm_mover[1] = origin[1] + (((distance + diagonal) ** 2) / 2) ** 0.5
    jog_conveyor_window.destroy()
    next_window_event.clear()
    paths = []
    # paths[0][2] -= 75
    # origin_higher = arm_mover[:]
    # origin_higher[2] += 100
    # paths.append(origin_higher)
    # paths.append([168.709, 538.398, 200.0, 180.0, 0.0, -0.0])
    # paths.append(origin_higher)
    
    rotation_matrix = [
            [2**0.5 / 2, -2**0.5 / 2],
            [2**0.5 / 2, 2**0.5 / 2]
    ]
    jog_arm_window = Tk()
    
    print(arm_mover[:])
    
    x_pos = Scale(jog_arm_window, from_=0, to=500+90, orient=HORIZONTAL, resolution=0.001, length=500)
    x_pos.pack()
    x_pos.set((arm_mover[1] + arm_mover[0])/ (2.0 ** 0.5) + tb_const.X_OFFSET)
    
    y_pos = Scale(jog_arm_window, from_=0, to=580+470, orient=HORIZONTAL, resolution=0.001, length=500)
    y_pos.pack()
    y_pos.set((arm_mover[1] - arm_mover[0]) / (2.0 ** 0.5) + tb_const.Y_OFFSET)
    
    z_pos = Scale(jog_arm_window, from_=-125, to=500, orient=HORIZONTAL, resolution=0.001, length=500)
    z_pos.pack()
    z_pos.set(arm_mover[2])
    
    button = Button(jog_arm_window, text= "Save point")
    button.pack(side = LEFT)
    button.bind('<ButtonPress-1>', lambda event: add_point(paths, arm_mover))
    
    button = Button(jog_arm_window, text= "Start")
    button.pack(side = LEFT)
    button.bind('<ButtonPress-1>', lambda event: next_window_event.set())
    
    jog_arm_window.attributes("-topmost", True)
    jog_arm_window.lift()
    
    while not next_window_event.is_set():
        jog_arm_window.update_idletasks()
        jog_arm_window.update()
        slider_x = x_pos.get()
        slider_y = y_pos.get()
        slider_z = z_pos.get()
        arm_mover[0] = 2**0.5 / 2 * (slider_x-tb_const.X_OFFSET) - 2**0.5 / 2 * (slider_y-tb_const.Y_OFFSET)
        arm_mover[1] = 2**0.5 / 2 * (slider_x-tb_const.X_OFFSET) + 2**0.5 / 2 * (slider_y-tb_const.Y_OFFSET)
        arm_mover[2] = slider_z
        
        move_arm_event.set()
    jog_arm_window.destroy()
    
    cycles = int(input('Number of cycles: '))
    while not protos_x.connect():
        pass
    feed_conveyor.start_motor_forwards()
    start_time = time.perf_counter()

    pick_conveyor.backwards_constant.trigger_path()
    origin_higher = origin.copy()
    origin_higher[2] += 100
    
    while cycles > 0:
        if check_prox_sensors(protos_x):
            pick_conveyor.stop.trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            pick_conveyor.forwards_distance.trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            cycles -= 1
            
            for path in paths:
                print(path)
                for i in range(6):
                    arm_mover[i] = path[i]
                move_arm_event.set()
                while move_arm_event.is_set():
                    pass
            start_time = time.perf_counter()
            pick_conveyor.backwards_constant.trigger_path()
        elif time.perf_counter()-start_time < 3:
            pass
        else:
            pick_conveyor.forwards_one_length.trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            pick_conveyor.backwards_constant.trigger_path()
            start_time = time.perf_counter()
    quit_event.set()
    print("Automated routine finished.")
    quit_event.set()
    pick_conveyor.forwards_one_length.trigger_path()
    while pick_speed_mon.check_value() > 0:
        pass
    quit()


if __name__ == '__main__':
    automated_routine()
    