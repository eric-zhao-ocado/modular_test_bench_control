"""
Automated gripper testing routine.
"""

import atexit
import multiprocessing as mp
import time
import tkinter
import sys
import csv

from fanucpy import Robot

import servo_conveyor
import protos_x_control as px_ctrl
import sure_servo_2_control as sv2_ctrl
import sure_servo_2_constants as sv2_cnst
import yaskawa_vfd_control as vfd_ctrl
import test_bench_constants as tb_cnst


def exit_routine(
    protos_x: px_ctrl.ProtosX,
    servo: sv2_ctrl.Sv2Servo,
    vfd: vfd_ctrl.YaskawaVfd,
    paths,
    pick_speed_mon,
    quit_event,
):
    """
    Exit routine to stop conveyors and vacuums on exit.

    Args:
        protos_x: ProtosX ModbusTCP client.
        servo: Sv2Servo object for pick conveyor.
        vfd: YaskawaVfd object for place conveyor.
        paths: Conveyor servo path dictionary
        pick_speed_mon: Servo speed monitor
        quit_event: Event to quit all processes.
    """
    quit_event.set()
    print("Exiting...")
    print("Disconnecting from ProtosX...")
    protos_x.exit_handler()
    paths["forwards_one_length"].trigger_path()
    while pick_speed_mon.check_value() != 0:
        pass
    print("Stopping servo...")
    servo.exit_handler()
    print("Stopping vfd...")
    vfd.exit_handler()

def check_ready():
    """
    Gets the required input and checks if user is ready.
    PLACEHOLDER FUNCTION, for testing purposes only.

    Returns:
        width: Width of box in mm
        height: Height of box in mm
    """
    parcel = input("Box or Bag (x/g): ")
    width = float(input("Width (mm): "))
    length = float(input("Length (mm): "))
    height = float(input("Height (mm): "))
    grippr_len = float(input("Gripper length (mm): "))
    compress_gripr_len = float(input("Gripper compressed length (mm): "))
    gripr_rad = float(input("Gripper radius (mm): "))
    while input('Input "Y" to start: ') != 'Y':
        pass
    return parcel, width, length, height, grippr_len, compress_gripr_len, gripr_rad

def jog_servo(
    move_direction: str,
    path: sv2_ctrl.Sv2ConstSpeed,
    speed,
    jog_conveyor_event,
):
    """
    Function for jogging the pick conveyor servo forwards and backwards.

    Args:
        move_direction: String indicating direction of movement.
        path: Sv2ConstSpeed path for constant speed servo control.
        speed: Speed at which to jog the motor at in rpm.
    """
    if jog_conveyor_event.is_set():
        print(f"Starting motor...{move_direction}")
        if move_direction == "Forward":
            path.change_speed(speed)
        else:
            path.change_speed(-speed)
        path.trigger_path()

def save_end_point(
    path: sv2_ctrl.Sv2PointPoint,
    position: int,
    next_stage_event: mp.Event,
):
    """
    Saves the current servo position as the end position for the box.

    Args:
        path: Sv2PointPoint point to point position movement path.
        position: Current position of servo.
        move_arm_event: Event to move onto the next GUI window.
    """
    path.change_position(position)
    next_stage_event.set()

def move_arm(
    quit_event: mp.Event,
    move_arm_event: mp.Event,
    pos: mp.Array,
    vel: mp.Value,
    accel: mp.Value,
    min_y: mp.Value,
):
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
        host=tb_cnst.ROBOT_HOST,
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
            tb_cnst.MIN_X < pos[0] < tb_cnst.MAX_X
            and min_y.value < pos[1] < tb_cnst.MAX_Y
        ):
            try:
                robot.move(
                    "pose",
                    vals=pos,
                    velocity=vel.value,
                    acceleration=accel.value,
                    cnt_val=0,
                    linear=False,
                )
            # Except the generic exception raised "position-is-not-reachable"
            except Exception as exception:
                print(repr(exception))
        # Clear the move arm event.
        move_arm_event.clear()
    quit_event.set()
    robot.disconnect()
    sys.exit(0)

def pick_conveyor_init():
    """
    Initializes the servo attached to the pick conveyor.

    Returns:
        pick_conveyor: conveyors.EnipServoConveyor for the servo.
        pick_speed_mon: sv2_ctrl.Sv2Monitor to monitor speed.
        pick_pos_mon: sv2_ctrl.Sv2Monitor to monitor position of servo.
    """
    pick_conveyor = servo_conveyor.EnipServoConveyor(
        top_length=1400,
        max_speed=113000,
        turn_circum=121,
        servo_addr=tb_cnst.SERVO_DRIVE_HOST,
    )
    pick_conveyor.servo.clear_alarms()
    pick_conveyor.servo.enable_servo()

    pick_speed_mon = sv2_ctrl.Sv2Monitor(
        servo=pick_conveyor.servo,
        mon_num=1,
        mon_type=sv2_cnst.MON_SPEED_FEEDBACK_TYPE,
    )
    pick_pos_mon = sv2_ctrl.Sv2Monitor(
        servo=pick_conveyor.servo,
        mon_num=2,
        mon_type=sv2_cnst.MON_POS_FEEDBACK_TYPE,
    )

    pick_conveyor.add_const_speed_path(
        path_name="backwards_constant",
        speed=-5000,
        acc=100,
    )
    pick_conveyor.add_point_point_path(
        path_name="forwards_one_length",
        cmd=sv2_cnst.CMD_REL,
        position=pick_conveyor.puu_per_length,
        speed=500,
        acc=100,
    )
    pick_conveyor.add_point_point_path(
        path_name="forwards_one_length_fast",
        cmd=sv2_cnst.CMD_REL,
        position=pick_conveyor.puu_per_length,
        speed=900,
        acc=100,
    )
    pick_conveyor.add_point_point_path(
        path_name="backwards_one_third_length",
        cmd=sv2_cnst.CMD_REL,
        position=-round(pick_conveyor.puu_per_length / 3),
        speed=900,
        acc=100,
    )
    # Path used to move the parcel a set distance.
    # Specific position to be updated later in the script.
    pick_conveyor.add_point_point_path(
        path_name="forwards_distance",
        cmd=sv2_cnst.CMD_REL,
        position=0,
        speed=100,
        acc=4000,
    )
    pick_conveyor.add_const_speed_path(
        path_name="slow_stop",
        speed=0,
        acc=4000,
    )
    pick_conveyor.add_const_speed_path(
        path_name="fast_stop",
        speed=0,
        acc=100,
    )
    pick_conveyor.add_const_speed_path(
        path_name="jog_path",
        speed=100,
        acc=1000,
    )

    return pick_conveyor, pick_speed_mon, pick_pos_mon

def feed_conveyor_init():
    """
    Initialize the VFD on the feed conveyor.

    Returns:
        Initialized vfd_ctrl.YaskawaVfd object
    """
    feed_conveyor = vfd_ctrl.YaskawaVfd(ip_addr=tb_cnst.VFD_HOST)
    feed_conveyor.change_freq(percentage=100)
    return feed_conveyor

def add_point(paths, arm_mover, vel, acc):
    """
    Adds the current position as a waypoint to the given array.

    Args:
        paths: Array containing waypoints
        arm_mover: Array containing coordinates of arm.
    """
    paths.append(["WAYPOINT", arm_mover[:], vel.value, acc.value])
    print(paths)

def add_vacuum(paths, index):
    """
    Adds a vacuum ON point to the array.

    Args:
        paths: Array containing waypoints
        index: Valve index
    """
    paths.append(["VACUUM", index])

def add_blowoff(paths):
    """
    Adds a blowoff point to the array.

    Args:
        paths: Array containing waypoints
    """
    paths.append(["BLOWOFF"])
    
def add_delay(paths, dly_time):
    """
    Adds a delay point to the array.
    
    Args:
        paths: Array containing waypoints
        dly_time: Delay time in seconds
    """
    paths.append(["DELAY", dly_time])

def reset_parcel(
    conveyor_paths: dict,
    protos_x: px_ctrl.ProtosX,
    pick_speed_mon: sv2_ctrl.Sv2Monitor,
):
    """
    Resets the parcel orientation on the pick conveyor.

    Args:
        conveyor_paths: Dictionary containing conveyor paths.
        protos_x: ProtosX object for reading proximity sensors.
        pick_speed_mon: Speed monitor for pick conveyor servo.
    """
    start_time = time.perf_counter()
    conveyor_paths["backwards_constant"].trigger_path()
    counter = 0

    while True:
        # Wait for package to be detected.
        if protos_x.check_prox_sensors():
            conveyor_paths["slow_stop"].trigger_path()
            # Wait for conveyor to stop moving
            while pick_speed_mon.check_value() != 0:
                pass
            return
        # Perform parcel orientation reset every 2 seconds.
        if time.perf_counter()-start_time < 2:
            pass
        elif counter < 1:
            conveyor_paths["forwards_one_length"].trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            conveyor_paths["backwards_constant"].trigger_path()
            counter += 1
            start_time = time.perf_counter()
        else:
            conveyor_paths["forwards_one_length"].trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            conveyor_paths["backwards_one_third_length"].trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            conveyor_paths["forwards_one_length_fast"].trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            conveyor_paths["backwards_constant"].trigger_path()
            start_time = time.perf_counter()

def rotate_45_deg(old_x, old_y):
    """
    Function for rotating and offsetting a coordinate point.

    Args:
        old_x: Original x value.
        old_y: Original y value.

    Returns:
        new_x, new_y: New values after rotation and translation.
    """
    # Rotation matrix to rotate points CW by 45 degrees
    rtn_mtrx = [[2**0.5 / 2, -2**0.5 / 2], [2**0.5 / 2, 2**0.5 / 2]]
    new_x = rtn_mtrx[0][0] * (old_x - tb_cnst.X_OFFSET) \
            + rtn_mtrx[0][1] * (old_y - tb_cnst.Y_OFFSET)
    new_y = rtn_mtrx[1][0] * (old_x - tb_cnst.X_OFFSET) \
            + rtn_mtrx[1][1] * (old_y - tb_cnst.Y_OFFSET)
    return new_x, new_y

def gui_app(
    conveyor_paths,
    pick_pos_mon,
    next_stage_event,
    arm_mover,
    paths,
    height,
    sliders,
    jog_conveyor_event,
    compress_gripr_len,
    vel,
    acc,
    min_arm_x,
    max_arm_x,
):
    """
    Process for running the GUI.
    """
    # Create window to jog the conveyor.
    jog_conveyor_window = tkinter.Tk()
    jog_conveyor_window.attributes("-topmost", True)
    jog_conveyor_window.lift()

    for test_direction in ("Forward", "Backward"):
        button = tkinter.Button(jog_conveyor_window, text=test_direction)
        button.pack(side=tkinter.LEFT)
        button.bind('<ButtonPress-1>', lambda event, dir=test_direction:
            jog_servo(dir, conveyor_paths["jog_path"], 50, jog_conveyor_event))
        button.bind(
            '<ButtonRelease-1>',
            lambda event: conveyor_paths["fast_stop"].trigger_path()
        )

    button = tkinter.Button(jog_conveyor_window, text= "Set end")
    button.pack(side = tkinter.LEFT)
    button.bind(
        '<ButtonPress-1>',
        lambda event: save_end_point(
            conveyor_paths["forwards_distance"],
            pick_pos_mon.check_value(),
            next_stage_event
        )
    )

    while not next_stage_event.is_set():
        jog_conveyor_window.update_idletasks()
        jog_conveyor_window.update()
    jog_conveyor_window.destroy()

    # Window to jog the arm and save waypoints.
    jog_arm_window = tkinter.Tk()
    jog_arm_window.attributes("-topmost", True)
    jog_arm_window.lift()

    # X coordinate slider.
    x_pos = tkinter.Scale(
        jog_arm_window,
        from_=min_arm_x + 0.001, to=max_arm_x,
        orient=tkinter.HORIZONTAL,
        resolution=0.001,
        length=500
    )
    x_pos.pack()
    # Calculate slider starting value (current position of arm)
    x_pos.set((arm_mover[1] + arm_mover[0])/ (2.0 ** 0.5) + tb_cnst.X_OFFSET)

    # Y coordinate slider.
    y_pos = tkinter.Scale(
        jog_arm_window,
        from_=0, to=900,
        orient=tkinter.HORIZONTAL,
        resolution=0.001,
        length=500
    )
    y_pos.pack()
    # Calculate slider starting value (current position of arm)
    y_pos.set((arm_mover[1] - arm_mover[0]) / (2.0 ** 0.5) + tb_cnst.Y_OFFSET)

    # Z coordinate slider.
    z_pos = tkinter.Scale(
        jog_arm_window,
        from_=tb_cnst.MIN_Z + compress_gripr_len + height,
        to=tb_cnst.MAX_Z,
        orient=tkinter.HORIZONTAL,
        resolution=0.001,
        length=500
    )
    z_pos.pack()
    z_pos.set(arm_mover[2])

    vel_slider = tkinter.Scale(
        jog_arm_window,
        from_=1,
        to=100,
        orient=tkinter.HORIZONTAL,
        resolution=1,
        length=500
    )
    vel_slider.pack()
    vel_slider.set(1)

    acc_slider = tkinter.Scale(
        jog_arm_window,
        from_=1,
        to=100,
        orient=tkinter.HORIZONTAL,
        resolution=1,
        length=500
    )
    acc_slider.pack()
    acc_slider.set(1)

    # Button to save current position as a point.
    button = tkinter.Button(jog_arm_window, text= "Save point")
    button.pack(side = tkinter.LEFT)
    button.bind('<ButtonPress-1>', lambda event: add_point(paths, arm_mover, vel, acc))
    # Button to add a Vacuum ON point.
    button = tkinter.Button(jog_arm_window, text= "Vacuum")
    button.pack(side = tkinter.LEFT)
    button.bind('<ButtonPress-1>', lambda event: add_vacuum(paths, 1))
    # Button to add a blow-off point.
    button = tkinter.Button(jog_arm_window, text= "Blow-off")
    button.pack(side = tkinter.LEFT)
    button.bind('<ButtonPress-1>', lambda event: add_blowoff(paths))
    # Button to start the automated routine.
    button = tkinter.Button(jog_arm_window, text= "Start")
    button.pack(side = tkinter.LEFT)
    button.bind('<ButtonPress-1>', lambda event: next_stage_event.set())

    sliders[0] = x_pos.get()
    sliders[1] = y_pos.get()
    sliders[2] = z_pos.get()

    next_stage_event.set()
    next_stage_event.clear()

    while not next_stage_event.is_set():
        jog_arm_window.update_idletasks()
        jog_arm_window.update()
        sliders[0] = x_pos.get()
        sliders[1] = y_pos.get()
        sliders[2] = z_pos.get()
        vel.value = vel_slider.get()
        acc.value = acc_slider.get()
    jog_arm_window.destroy()


def automated_routine():
    """
    Routine for automating the testing of grippers on parcels.
    """
    # Initial initialization
    pick_conveyor, pick_speed_mon, pick_pos_mon = pick_conveyor_init()
    conveyor_paths = pick_conveyor.path_dict
    feed_conveyor = feed_conveyor_init()
    protos_x = px_ctrl.ProtosX(tb_cnst.PROTOS_X_HOST)

    # Initialize events.
    next_stage_event = mp.Event()
    move_arm_event = mp.Event()
    quit_event = mp.Event()
    jog_conveyor_event = mp.Event()
    jog_conveyor_event.set()

    atexit.register(
        exit_routine,
        protos_x=protos_x,
        servo=pick_conveyor.servo,
        vfd=feed_conveyor,
        paths=conveyor_paths,
        pick_speed_mon=pick_speed_mon,
        quit_event=quit_event,
    )

    # Get dimensions of package.
    parcel, width, length, height, gripr_len, compress_gripr_len, gripr_rad = check_ready()

    # NOTE: TESTING PURPOSES ONLY, need dynamic value
    gripr_len = 335
    compress_gripr_len = 265
    gripr_rad = 74

    # Calculate the origin of the gripper
    # Makes sure the gripper doesn't hit the guards
    arm_origin_x = tb_cnst.DEFAULT_X + (gripr_rad-5) / (2 ** 0.5)
    arm_origin_y = tb_cnst.DEFAULT_Y + (gripr_rad-5) / (2 ** 0.5)

    min_y = mp.Value('d', arm_origin_y - 1)

    # Set default_origin. The last 3 parameters in the list should not be changed.
    default_origin = [
        tb_cnst.DEFAULT_X, tb_cnst.DEFAULT_Y,
        height + tb_cnst.MIN_Z + 15 + gripr_len, 180.0, 0.0, 0.0
    ]

    # Create multiprocessing variables to share between processes.
    arm_mover = mp.Array('d', range(6))
    vel = mp.Value('d', 50)
    accel = mp.Value('d', 1)

    # Initialize arm_mover which holds the coordinates to move the arm to.
    arm_mover[0] = arm_origin_x
    arm_mover[1] = arm_origin_y
    for i in range(4):
        arm_mover[i + 2] = default_origin[i + 2]
    # Initialize the arm mover process.
    arm_process = mp.Process(
        target=move_arm,
        args=(quit_event, move_arm_event, arm_mover, vel, accel, min_y)
    )
    arm_process.start()

    move_arm_event.set()

    # Move package and arm to the starting point
    feed_conveyor.start_motor_forwards()
    reset_parcel(conveyor_paths, protos_x, pick_speed_mon)
    feed_conveyor.stop_motor()
    time.sleep(0.2)
    pick_conveyor.set_home()

    # Calculate center of diagonal of box (offset by 96)
    half_diagonal = (width ** 2 * 2) ** 0.5 / 2 - 96
    long_diagonal = width / (2 ** 0.5) + length / (2 ** 0.5)
    # Calculate maximum conveyor position
    max_conveyor_pos = (tb_cnst.MAX_X - default_origin[0]) * (2 ** 0.5) - half_diagonal
    max_grip_conv_pos = max_conveyor_pos - gripr_rad + 61
    # Check to ensure box does not hit conveyor guards
    if long_diagonal > 184 and parcel == 'x':
        max_conveyor_pos = max_conveyor_pos - (long_diagonal - 183 / 2) / 2 \
            - ((length - width) / (2 ** 0.5)) * 2.6
    # Check to ensure gripper does not hit conveyor guards.
    max_conveyor_pos = min(max_grip_conv_pos, max_conveyor_pos)
    # Calculate PUU position
    max_conveyor_pos = round((max_conveyor_pos / pick_conveyor.turn_circum) * sv2_cnst.E_GEAR_DEN)

    pick_conveyor.add_point_point_path(
        "reset_path",
        sv2_cnst.CMD_ABS,
        max_conveyor_pos-1,
        50,
        4000,
    )
    max_arm_x = pick_conveyor.turn_circum * max_conveyor_pos / sv2_cnst.E_GEAR_DEN + half_diagonal
    min_arm_x = (arm_origin_x + arm_origin_y) / (2.0 ** 0.5) + tb_cnst.X_OFFSET
    manager = mp.Manager()
    paths = manager.list()
    sliders = mp.Array('d', range(3))
    gui_process = mp.Process(
        target=gui_app,
        args=(
            conveyor_paths, pick_pos_mon, next_stage_event, arm_mover,
            paths, height, sliders, jog_conveyor_event, compress_gripr_len,
            vel, accel, min_arm_x, max_arm_x
        )
    )
    gui_process.start()
    vel.value = 100
    accel.value = 100
    min_conveyor_pos = round(sv2_cnst.E_GEAR_DEN * (2 ** 0.5 * (arm_origin_x - default_origin[0])-half_diagonal) / pick_conveyor.turn_circum) + 1000
    pick_conveyor.add_point_point_path(
        "min_location",
        sv2_cnst.CMD_ABS, min_conveyor_pos + 100, 50, 4000)
    # Loop to jog the conveyor.
    while not next_stage_event.is_set():
        # Move arm to current set position
        move_arm_event.set()
        # Get conveyor position
        position = pick_pos_mon.check_value()
        # Calculate distance the box has travelled.
        distance = pick_conveyor.turn_circum * position / sv2_cnst.E_GEAR_DEN

        # Check if conveyor has been jogged too far backwards, and reset if so.
        if position >= 4000000000 or position < min_conveyor_pos:
            jog_conveyor_event.clear()
            conveyor_paths["min_location"].trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            time.sleep(0.2)
            jog_conveyor_event.set()
        # Check if conveyor position is too far forwards, reset position if so.
        elif 4000000000 >= position >= max_conveyor_pos:
            jog_conveyor_event.clear()
            # conveyor_paths["fast_stop"].trigger_path()
            # position = max_conveyor_pos
            conveyor_paths["reset_path"].trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            time.sleep(0.2)
            jog_conveyor_event.set()
        # Move arm to above the center of the diagonal of the box.
        if max_conveyor_pos >= position >= 0:
            arm_mover[0] = default_origin[0] + (distance + half_diagonal) / 2 ** 0.5
            arm_mover[1] = default_origin[1] + (distance + half_diagonal) / 2 ** 0.5
    next_stage_event.clear()

    while not next_stage_event.is_set():
        pass
    next_stage_event.clear()

    while not next_stage_event.is_set():
        arm_mover[0], arm_mover[1] = rotate_45_deg(sliders[0], sliders[1])
        arm_mover[2] = sliders[2]
        move_arm_event.set()

    cycles = int(input('Number of cycles: '))
    feed_conveyor.start_motor_forwards()

    # reset data file
    with open('data.csv', "w+", encoding='UTF8', newline='') as file:
        headings = ['Cycle number', 'Time (s)', 'Type', 'Value', 'Velocity (%)', 'Acceleration (%)']
        # create the csv writer
        writer = csv.writer(file)
        writer.writerow(headings)
    start_time = time.perf_counter()
    cycle_num = 1
    while cycle_num <= cycles:
        # Wait for package to be detected.
        reset_parcel(conveyor_paths, protos_x, pick_speed_mon)
        time.sleep(0.2)
        pick_conveyor.set_home()
        # Move parcel to preset location
        conveyor_paths["forwards_distance"].trigger_path()
        while pick_speed_mon.check_value() != 0:
            pass
        for path in paths[:]:
            # open the file in the write mode
            with open('data.csv', 'a', encoding='UTF8', newline='') as file:
                info = path.copy()
                info.insert(0, time.perf_counter()-start_time)
                info.insert(0, cycle_num)
                # create the csv writer
                writer = csv.writer(file)
                # write a row to the csv file
                writer.writerow(info)
            if path[0] == "VACUUM":
                protos_x.vacuum(path[1])
            elif path[0] == "BLOWOFF":
                protos_x.blowoff()
            elif path[0] == "DELAY":
                time.sleep(path[1])
            elif path[0] == "WAYPOINT":
                for i in range(6):
                    arm_mover[i] = path[1][i]
                    vel.value = path[2]
                    accel.value = path[3]
                move_arm_event.set()
                while move_arm_event.is_set():
                    pass
        cycle_num += 1
    print("Automated routine finished.")
    quit_event.set()
    move_arm_event.set()
    conveyor_paths["forwards_one_length"].trigger_path()
    while pick_speed_mon.check_value() > 0:
        pass


if __name__ == '__main__':
    automated_routine()
