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
    # robot.disconnect()

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
    
def update_origin(path:sv2_ctrl.Sv2PointPoint, position, conveyor:conveyors.EnipServoConveyor, origin_arr, event_1:multiprocessing.Event):
    path.change_position(position)
    # turns = position / sv2_const.E_GEAR_DEN
    # distance = conveyor.turn_circum * turns
    # width = 130
    # diagonal = (width ** 2 * 2) ** 0.5 / 2 - 95
    # origin_arr[0] += (((distance + diagonal) ** 2) / 2) ** 0.5
    # origin_arr[1] += (((distance + diagonal) ** 2) / 2) ** 0.5
    event_1.set()
    
def move_arm(quit_event, event_0, event_1, event_2, pos):
    robot = Robot(
        robot_model="Fanuc",
        host=tb_const.ROBOT_HOST,
        port=18735,
        ee_DO_type="RDO",
        ee_DO_num=7,
        )
    robot.connect()
    while not event_0.is_set():
        position = []
        for i in range(6):
            position.append(pos[i])
        robot.move(
            "pose",
            vals=position,
            velocity=100,
            acceleration=100,
            cnt_val=0,
            linear=False
        )
    position_higher = position.copy()
    position_higher[2] = position[2] + 100
    robot.move(
            "pose",
            vals=position_higher,
            velocity=100,
            acceleration=100,
            cnt_val=0,
            linear=False
        )
    while not quit_event.is_set():
        # position = []
        # for i in range(6):
        #     position.append(pos[i])
        event_1.wait()
        robot.move(
            "pose",
            vals=position,
            velocity=100,
            acceleration=100,
            cnt_val=0,
            linear=False
        )
        robot.move(
            "pose",
            vals=position_higher,
            velocity=100,
            acceleration=100,
            cnt_val=0,
            linear=False
        )
        robot.move(
            "pose",
            vals=[168.709, 538.398, 200.0, 180.0, 0.0, -0.0],
            velocity=100,
            acceleration=100,
            cnt_val=0,
            linear=False
        )
        robot.move(
            "pose",
            vals=position_higher,
            velocity=100,
            acceleration=100,
            cnt_val=0,
            linear=False
        )
        event_2.set()
        time.sleep(1)

def automated_routine():
    pick_conveyor = conveyors.EnipServoConveyor(
        top_length=1400,
        max_speed=113000,
        turn_circum=121,
        servo_addr=tb_const.SERVO_DRIVE_HOST
        )
    pick_conveyor.servo.clear_alarms()
    pick_conveyor.servo.enable_servo()
    pick_speed_monitor = sv2_ctrl.Sv2Monitor(
        servo=pick_conveyor.servo,
        mon_num=1,
        mon_type=sv2_const.MON_SPEED_FEEDBACK_TYPE
        )
    pick_position_monitor = sv2_ctrl.Sv2Monitor(
        servo=pick_conveyor.servo,
        mon_num=2,
        mon_type=sv2_const.MON_POS_FEEDBACK_TYPE
    )

    feed_conveyor = vfd_ctrl.YaskawaVfd(ip_addr=tb_const.VFD_HOST)
    feed_conveyor.change_freq(percentage=100)
    atexit.register(exit_routine, servo=pick_conveyor.servo, vfd=feed_conveyor)

    protos_x = ModbusTcpClient(tb_const.PROTOS_X_HOST)
    protos_x.connect()
    
    event_0 = multiprocessing.Event()
    event_1 = multiprocessing.Event()
    event_2 = multiprocessing.Event()
    quit_event = multiprocessing.Event()
    width, height = check_ready()
    
    origin = [268.701, -395.98, height-95, 180.0, 0.0, 0.0]
    origin_mover = multiprocessing.Array('d', range(6))
    for i in range(6):
        origin_mover[i] = origin[i]
    p = multiprocessing.Process(target=move_arm, args=(quit_event, event_0, event_1, event_2, origin_mover,))
    p.start()
    pick_conveyor.backwards_constant.trigger_path()
    feed_conveyor.start_motor_forwards()
    while not check_prox_sensors(protos_x):
        pass
    pick_conveyor.stop.trigger_path()
    feed_conveyor.stop_motor()
    while pick_speed_monitor.check_value() != 0:
        pass
    time.sleep(1)
    pick_conveyor.set_home()
    
    jog_path = sv2_ctrl.Sv2ConstSpeed(pick_conveyor.servo, 16)
    jog_path.change_acc(1000)

    root = Tk()
    
    for test_direction in ("Forward", "Backward"):
        button = Button(root, text=test_direction)
        button.pack(side=LEFT)
        button.bind('<ButtonPress-1>', lambda event, dir=test_direction:
            start_motor(dir, jog_path, 50))
        button.bind('<ButtonRelease-1>', lambda event: pick_conveyor.stop.trigger_path())

    button = Button(root, text= "Set origin")
    button.pack(side = LEFT)
    button.bind('<ButtonPress-1>', lambda event: pick_conveyor.set_home())

    button = Button(root, text= "Set end")
    button.pack(side = LEFT)
    button.bind('<ButtonPress-1>', lambda event: update_origin(pick_conveyor.forwards_distance, pick_position_monitor.check_value(), pick_conveyor, origin, event_0))
    
    while not event_0.is_set():
        root.update_idletasks()
        root.update()
        position = pick_position_monitor.check_value()
        if 447746 > position >= 0:
            turns = position / sv2_const.E_GEAR_DEN
            distance = pick_conveyor.turn_circum * turns
            diagonal = (width ** 2 * 2) ** 0.5 / 2 - 95
            origin_mover[0] = origin[0] + (((distance + diagonal) ** 2) / 2) ** 0.5
            origin_mover[1] = origin[1] + (((distance + diagonal) ** 2) / 2) ** 0.5
        elif 4000000000 >= position >= 447746:
            position = 447746
            turns = position / sv2_const.E_GEAR_DEN
            distance = pick_conveyor.turn_circum * turns
            width = 130
            diagonal = (width ** 2 * 2) ** 0.5 / 2 - 95
            origin_mover[0] = origin[0] + (((distance + diagonal) ** 2) / 2) ** 0.5
            origin_mover[1] = origin[1] + (((distance + diagonal) ** 2) / 2) ** 0.5
            
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
            while pick_speed_monitor.check_value() != 0:
                pass
            pick_conveyor.forwards_distance.trigger_path()
            while pick_speed_monitor.check_value() != 0:
                pass
            cycles -= 1
            event_1.set()
            event_2.wait()
            event_1.clear()
            event_2.clear()
            start_time = time.perf_counter()
            pick_conveyor.backwards_constant.trigger_path()
        elif time.perf_counter()-start_time < 3:
            pass
        else:
            pick_conveyor.forwards_one_length.trigger_path()
            while pick_speed_monitor.check_value() != 0:
                pass
            pick_conveyor.backwards_constant.trigger_path()
            start_time = time.perf_counter()
        
    print("Automated routine finished.")
    quit_event.set()
    quit()


if __name__ == '__main__':
    automated_routine()
    