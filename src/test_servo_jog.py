"""
Sample code of GUI for jogging the motor
"""

import tkinter

import test_bench_constants as tb_const
import sure_servo_2_control as sv2_ctrl

def start_motor(move_direction, path:sv2_ctrl.Sv2ConstSpeed, slider):
    """
    Starts motor in specified direction.
    """
    print(f"starting motor...{move_direction}")
    speed = slider.get()
    if move_direction == "forward":
        path.change_speed(speed)
    else:
        path.change_speed(-speed)
    path.trigger_path()

def stop_motor(path:sv2_ctrl.Sv2ConstSpeed):
    """
    Stops motor.
    """
    path.change_speed(0)
    path.trigger_path()

def set_origin(servo:sv2_ctrl.Sv2Servo):
    """
    Resets the origin to set the current position as "0".
    """
    print("setting origin...")
    servo.set_home()

def gui_app():
    """
    Main gui for jogging the servo.
    """
    root = tkinter.Tk()

    test_servo = sv2_ctrl.Sv2Servo(tb_const.SERVO_DRIVE_HOST, 933)
    test_servo.enable_servo()
    moved_path = sv2_ctrl.Sv2ConstSpeed(test_servo, 1)
    stopped_path = sv2_ctrl.Sv2ConstSpeed(test_servo, 2)

    speed = tkinter.Scale(root, from_=0, to=932, orient=tkinter.HORIZONTAL)
    speed.pack()

    for test_direction in ("forward", "backward"):
        button = tkinter.Button(root, text=test_direction)
        button.pack(side=tkinter.LEFT)
        button.bind('<ButtonPress-1>', lambda event, dir=test_direction:
            start_motor(dir, moved_path, speed))
        button.bind('<ButtonRelease-1>', lambda event: stop_motor(stopped_path))

    button = tkinter.Button(root, text= "Set origin")
    button.pack(side = tkinter.LEFT)
    button.bind('<ButtonPress-1>', lambda event: set_origin(test_servo))

    root.mainloop()

if __name__ == "__main__":
    gui_app()
    