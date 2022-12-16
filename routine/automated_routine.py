"""
Automated gripper testing routine.
"""

import time
import atexit
import multiprocessing
import tkinter as tk
from pymodbus.client import ModbusTcpClient
from fanucpy import Robot

import conveyors
import sure_servo_2_control as sv2_ctrl
import sure_servo_2_constants as sv2_const
import yaskawa_vfd_control as vfd_ctrl
import test_bench_constants as tb_const


def check_prox_sensors(protos_x):
    """
    Checks to see if the proximity sensors are detecting anything.

    Args:
        protos_x: ProtosX ModbusTCP client.

    Returns:
        bool: True if both sensors detect an object, false otherwise.
    """
    data = protos_x.read_discrete_inputs(tb_const.PROX_1_ADDR, 2)
    try:
        prox_1_sense = data.bits[0]
        prox_2_sense = data.bits[1]
        if(prox_1_sense and prox_2_sense):
            return True
        return False
    except AttributeError:
        return False

def exit_routine(protos_x, servo:sv2_ctrl.Sv2Servo, vfd:vfd_ctrl.YaskawaVfd):
    """
    Exit routine to stop conveyors and vacuums on exit.

    Args:
        protos_x: ProtosX ModbusTCP client.
        servo: Sv2Servo object for pick conveyor.
        vfd: YaskawaVfd object for place conveyor.
    """
    # Disable vacuum and blow-off valves
    protos_x.write_coils(0,[1, 1, 1, 1, 1, 1, 1, 1])
    protos_x.write_coils(8,[1, 1, 1, 1, 1, 1, 1, 1])
    vfd.exit_handler()
    servo.exit_handler()

def protos_x_initialization(host):
    """
    Initializes ProtosX ModbusTCP object.

    Returns:
        protos_x: ModbusTcpClient for ModbusTCP I/O control.
    """
    protos_x = ModbusTcpClient(host)
    print('Connecting to Protos X...')
    while not protos_x.connect():
        print('Attempting to reconnect...')
    print('Connected to Protos X.')
    protos_x.write_coils(0,[1, 1, 1, 1, 1, 1, 1, 1])
    protos_x.write_coils(8,[1, 1, 1, 1, 1, 1, 1, 1])
    return protos_x

def check_ready():
    """
    Gets the required input and checks if user is ready.
    PLACEHOLDER FUNCTION, for testing purposes only.

    Returns:
        width: Width of box in mm
        height: Height of box in mm
    """
    width = int(input("Width (mm): "))
    height = int(input("Height (mm): "))
    while input('Input "Y" to start: ') != 'Y':
        pass
    return width, height

def jog_servo(move_direction, path:sv2_ctrl.Sv2ConstSpeed, speed):
    """
    Function for jogging the pick conveyor servo forwards and backwards.

    Args:
        move_direction: String indicating direction of movement.
        path: Sv2ConstSpeed path for constant speed servo control.
        speed: Speed at which to jog the motor at in rpm.
    """
    print(f"Starting motor...{move_direction}")
    if move_direction == "Forward":
        path.change_speed(speed)
    else:
        path.change_speed(-speed)
    path.trigger_path()

def save_end_point(
    path:sv2_ctrl.Sv2PointPoint,
    position,
    next_window_event:multiprocessing.Event
    ):
    """
    Saves the current servo position as the end position for the box.

    Args:
        path: Sv2PointPoint point to point position movement path.
        position: Current position of servo.
        move_arm_event: Event to move onto the next GUI window.
    """
    path.change_position(position)
    next_window_event.set()

def move_arm(quit_event, move_arm_event, pos, vel, accel):
    """
    Process to move the arm. Monitors the move_arm_event and signals
    the arm to move whenever the event is set.

    Args:
        quit_event: Event to signal the end of the routine.
        move_arm_event: Event to signal the arm to move.
        pos: Position to move arm to.
        vel: Velocity to move arm at.
        accel: Acceleration to move arm at.
    """
    robot = Robot(
        robot_model="Fanuc",
        host=tb_const.ROBOT_HOST,
        port=18735,
        ee_DO_type="RDO",
        ee_DO_num=7,
        )
    robot.connect()
    while not quit_event.is_set():
        # Wait for event telling arm to move to be set.
        move_arm_event.wait()
        # Check if the movement command is within the bounds of the testbench.
        if (
            tb_const.MIN_X < pos[0] < tb_const.MAX_X
            and tb_const.MIN_Y < pos[1] < tb_const.MAX_Y
            ):
            try:
                robot.move(
                    "pose",
                    vals=pos,
                    velocity=vel.value,
                    acceleration=accel.value,
                    cnt_val=0,
                    linear=False
                )
            # Except "position-is-not-reachable"
            except:
                pass
        # Clear the move arm event.
        move_arm_event.clear()
    robot.disconnect()
    quit()

def pick_conveyor_init():
    """
    Initializes the servo attached to the pick conveyor.

    Returns:
        pick_conveyor: conveyors.EnipServoConveyor for the servo.
        pick_speed_mon: sv2_ctrl.Sv2Monitor to monitor speed.
        pick_pos_mon: sv2_ctrl.Sv2Monitor to monitor position of servo.
    """
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
    """
    Initialize the VFD on the feed conveyor.

    Returns:
        Initialized vfd_ctrl.YaskawaVfd object
    """
    feed_conveyor = vfd_ctrl.YaskawaVfd(ip_addr=tb_const.VFD_HOST)
    feed_conveyor.change_freq(percentage=100)
    return feed_conveyor

def add_point(paths, arm_mover):
    """
    Adds the current position as a waypoint to the given array.

    Args:
        paths: Array containing waypoints
        arm_mover: Array containing coordinates of arm.
    """
    paths.append(arm_mover[:])
    print(paths)

def add_vacuum(paths):
    """
    Adds a vacuum ON point to the array.

    Args:
        paths: Array containing waypoints
    """
    paths.append("VACUUM")

def add_blowoff(paths):
    """
    Adds a blowoff point to the array.

    Args:
        paths: Array containing waypoints
    """
    paths.append("BLOWOFF")

def vacuum(protos_x):
    """
    Vacuum point that opens the vacuum valves and closes blowoff valves.

    Args:
        protos_x: ProtosX ModbusTCP client
    """
    # Open vacuum valves
    protos_x.write_coils(0,[0, 0, 0, 0, 0, 0, 0, 0])
    # Close blowoff valves
    protos_x.write_coils(8,[1, 1, 1, 1, 1, 1, 1, 1])

def blowoff(protos_x):
    """
    Vacuum point that opens the blowoff valves and closes vacuum valves.

    Args:
        protos_x: ProtosX ModbusTCP client
    """
    # Open blowoff valves
    protos_x.write_coils(8,[0, 0, 0, 0, 0, 0, 0, 0])
    # Close vacuum valves
    protos_x.write_coils(0,[1, 1, 1, 1, 1, 1, 1, 1])
    # Only need to blow-off for a very short amount of time.
    time.sleep(0.1)
    # Close blowoff valves
    protos_x.write_coils(8,[1, 1, 1, 1, 1, 1, 1, 1])

def automated_routine():
    """
    Routine for automating the testing of grippers on parcels.
    """
    # Initial initialization
    pick_conveyor, pick_speed_mon, pick_pos_mon = pick_conveyor_init()
    feed_conveyor = feed_conveyor_init()
    protos_x = protos_x_initialization(tb_const.PROTOS_X_HOST)
    atexit.register(exit_routine, protos_x, servo=pick_conveyor.servo, vfd=feed_conveyor)

    # Initialize events.
    next_window_event = multiprocessing.Event()
    move_arm_event = multiprocessing.Event()
    quit_event = multiprocessing.Event()

    # Get dimensions of package.
    width, height = check_ready()

    # Set origin. The last 3 parameters in the list should not be changed.
    origin = [tb_const.DEFAULT_X, tb_const.DEFAULT_Y, height-95, 180.0, 0.0, 0.0]
    # Create multiprocessing variables to share between processes.
    arm_mover = multiprocessing.Array('d', range(6))
    vel = multiprocessing.Value('d', 100)
    accel = multiprocessing.Value('d', 100)

    # Initialize arm_mover which holds the coordinates to move the arm to.
    for i in range(6):
        arm_mover[i] = origin[i]
    # Initialize the arm mover process.
    arm_process = multiprocessing.Process(
        target=move_arm,
        args=(quit_event, move_arm_event, arm_mover, vel, accel)
        )
    arm_process.start()

    # Move package and arm to the starting point
    pick_conveyor.backwards_constant.trigger_path()
    feed_conveyor.start_motor_forwards()
    move_arm_event.set()
    while not check_prox_sensors(protos_x):
        pass
    pick_conveyor.stop.trigger_path()
    feed_conveyor.stop_motor()
    while pick_speed_mon.check_value() != 0:
        pass
    pick_conveyor.set_home()

    # Create servo control path to jog the motor at a slow speed.
    jog_path = sv2_ctrl.Sv2ConstSpeed(pick_conveyor.servo, 16)
    jog_path.change_acc(1000)

    # Create window to jog the conveyor.
    jog_conveyor_window = tk.Tk()
    jog_conveyor_window.attributes("-topmost", True)
    jog_conveyor_window.lift()

    for test_direction in ("Forward", "Backward"):
        button = tk.Button(jog_conveyor_window, text=test_direction)
        button.pack(side=tk.LEFT)
        button.bind('<ButtonPress-1>', lambda event, dir=test_direction:
            jog_servo(dir, jog_path, 50))
        button.bind(
            '<ButtonRelease-1>',
            lambda event: pick_conveyor.stop.trigger_path()
            )

    button = tk.Button(jog_conveyor_window, text= "Set end")
    button.pack(side = tk.LEFT)
    button.bind(
        '<ButtonPress-1>',
        lambda event: save_end_point(
            pick_conveyor.forwards_distance,
            pick_pos_mon.check_value(),
            next_window_event
            )
        )

    # Loop to jog the conveyor.
    while not next_window_event.is_set():
        # Update GUI window
        jog_conveyor_window.update_idletasks()
        jog_conveyor_window.update()

        # Move arm to current set position
        move_arm_event.set()
        # Get conveyor position
        position = pick_pos_mon.check_value()
        # Calculate number of turns servo has undergone.
        turns = position / sv2_const.E_GEAR_DEN
        # Calculate distance the box has travelled.
        distance = pick_conveyor.turn_circum * turns
        # Calculate center of diagonal of box (offset by 95)
        diagonal = (width ** 2 * 2) ** 0.5 / 2 - 95
        # Calculate maximum conveyor position
        max_pos = round(
            (((tb_const.MAX_X - origin[0]) ** 2 * 2) ** 0.5 - diagonal)
            / pick_conveyor.turn_circum * sv2_const.E_GEAR_DEN
            )
        # Create a path to reset the conveyor to the max position
        reset_path = sv2_ctrl.Sv2PointPoint(
            servo=pick_conveyor.servo,
            path_num=15,
            cmd=sv2_const.CMD_ABS,
            position=max_pos,
            speed=100
            )
        reset_path.change_acc(1000)
        # Check if conveyor has been jogged too far backwards, and reset if so.
        if position >= 4000000000:
            pick_conveyor.stop.trigger_path()
            while pick_speed_mon.check_value() > 0:
                pass
            pick_conveyor.set_home()
        # Check if conveyor position is too far forwards, reset position if so.
        elif 4000000000 >= position >= max_pos:
            pick_conveyor.stop.trigger_path()
            position = tb_const.MAX_CONVEYOR_POSITION
            reset_path.trigger_path()
        # Move arm to above the center of the diagonal of the box.
        if max_pos >= position >= 0:
            arm_mover[0] = origin[0] + (((distance + diagonal) ** 2) / 2) ** 0.5
            arm_mover[1] = origin[1] + (((distance + diagonal) ** 2) / 2) ** 0.5
    jog_conveyor_window.destroy()
    next_window_event.clear()

    # Array to store the waypoints initialized here.
    paths = []

    # Window to jog the arm and save waypoints.
    jog_arm_window = tk.Tk()
    jog_arm_window.attributes("-topmost", True)
    jog_arm_window.lift()

    # X coordinate slider.
    x_pos = tk.Scale(
        jog_arm_window,
        from_=0, to=500+90,
        orient=tk.HORIZONTAL,
        resolution=0.001,
        length=500
        )
    x_pos.pack()
    # Calculate slider starting value (current position of arm)
    x_pos.set((arm_mover[1] + arm_mover[0])/ (2.0 ** 0.5) + tb_const.X_OFFSET)

    # Y coordinate slider.
    y_pos = tk.Scale(
        jog_arm_window,
        from_=0, to=580+470,
        orient=tk.HORIZONTAL,
        resolution=0.001,
        length=500
        )
    y_pos.pack()
    # Calculate slider starting value (current position of arm)
    y_pos.set((arm_mover[1] - arm_mover[0]) / (2.0 ** 0.5) + tb_const.Y_OFFSET)

    # Z coordinate slider.
    z_pos = tk.Scale(
        jog_arm_window,
        from_=-180+height,
        to=500,
        orient=tk.HORIZONTAL,
        resolution=0.001,
        length=500
        )
    z_pos.pack()
    z_pos.set(arm_mover[2])

    # Button to save current position as a point.
    button = tk.Button(jog_arm_window, text= "Save point")
    button.pack(side = tk.LEFT)
    button.bind('<ButtonPress-1>', lambda event: add_point(paths, arm_mover))
    # Button to add a Vacuum ON point.
    button = tk.Button(jog_arm_window, text= "Vacuum")
    button.pack(side = tk.LEFT)
    button.bind('<ButtonPress-1>', lambda event: add_vacuum(paths))
    # Button to add a blow-off point.
    button = tk.Button(jog_arm_window, text= "Blow-off")
    button.pack(side = tk.LEFT)
    button.bind('<ButtonPress-1>', lambda event: add_blowoff(paths))
    # Button to start the automated routine.
    button = tk.Button(jog_arm_window, text= "Start")
    button.pack(side = tk.LEFT)
    button.bind('<ButtonPress-1>', lambda event: next_window_event.set())


    # Rotation matrix to rotate points CW by 45 degrees
    rtn_mtrx = [[2**0.5 / 2, -2**0.5 / 2], [2**0.5 / 2, 2**0.5 / 2]]

    while not next_window_event.is_set():
        jog_arm_window.update_idletasks()
        jog_arm_window.update()
        slider_x = x_pos.get()
        slider_y = y_pos.get()
        slider_z = z_pos.get()
        # Rotates the axes and then offsets it to the starting point of the arm
        # Needed so that the sliders correspond to axes that are more intuitive
        arm_mover[0] = rtn_mtrx[0][0] * (slider_x-tb_const.X_OFFSET) \
            + rtn_mtrx[0][1] * (slider_y-tb_const.Y_OFFSET)
        arm_mover[1] = rtn_mtrx[1][0] * (slider_x-tb_const.X_OFFSET) \
            + rtn_mtrx[1][1] * (slider_y-tb_const.Y_OFFSET)
        arm_mover[2] = slider_z

        move_arm_event.set()
    jog_arm_window.destroy()

    cycles = int(input('Number of cycles: '))
    while not protos_x.connect():
        pass
    feed_conveyor.start_motor_forwards()
    start_time = time.perf_counter()

    pick_conveyor.backwards_constant.trigger_path()

    while cycles > 0:
        # Wait for package to be detected.
        if check_prox_sensors(protos_x):
            pick_conveyor.stop.trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            # Move package to set location.
            pick_conveyor.forwards_distance.trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            cycles -= 1

            # Cycle through the waypoints in the array.
            for path in paths:
                if path == "VACUUM":
                    vacuum(protos_x)
                elif path == "BLOWOFF":
                    blowoff(protos_x)
                else:
                    for i in range(6):
                        arm_mover[i] = path[i]
                    move_arm_event.set()
                    while move_arm_event.is_set():
                        pass
            start_time = time.perf_counter()
            pick_conveyor.backwards_constant.trigger_path()
        # Perform parcel orientation reset every 3 seconds.
        elif time.perf_counter()-start_time < 3:
            pass
        else:
            pick_conveyor.forwards_one_length.trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            pick_conveyor.backwards_constant.trigger_path()
            start_time = time.perf_counter()
    print("Automated routine finished.")
    quit_event.set()
    move_arm_event.set()
    pick_conveyor.forwards_one_length.trigger_path()
    while pick_speed_mon.check_value() > 0:
        pass
    quit()


if __name__ == '__main__':
    automated_routine()
    