"""
Sample code of GUI for jogging the motor
Will be used for the MANUAL TEST, to recalibrate the conveyor
Essentially line up marking on the conveyor with marking on the extrusion
"""

from tkinter import *

import test_bench_constants as tb_const
import sure_servo_2_control as sv2_ctrl

running = False
root = Tk()
jobid = None

def start_motor(move_direction, path:sv2_ctrl.Sv2ConstSpeed, slider):
    print(f"starting motor...{move_direction}")
    speed = slider.get()
    if move_direction == "forward":
        path.change_speed(speed)
    else:
        path.change_speed(-speed)
    path.trigger_path()

def stop_motor(path:sv2_ctrl.Sv2ConstSpeed):
    path.change_speed(0)
    path.trigger_path()

def set_origin(servo:sv2_ctrl.Sv2Servo):
    print("setting origin...")
    servo.set_home()


test_servo = sv2_ctrl.Sv2Servo(tb_const.SERVO_DRIVE_HOST, 933)
test_servo.send_command(300, 4, 7, 1)
moved_path = sv2_ctrl.Sv2ConstSpeed(test_servo, 1)
stopped_path = sv2_ctrl.Sv2ConstSpeed(test_servo, 2)

w = Scale(root, from_=0, to=932, orient=HORIZONTAL)
w.pack()

for test_direction in ("forward", "backward"):
    button = Button(root, text=test_direction)
    button.pack(side=LEFT)
    button.bind('<ButtonPress-1>', lambda event, test_direction=test_direction:
        start_motor(test_direction, moved_path, w))
    button.bind('<ButtonRelease-1>', lambda event: stop_motor(stopped_path))

button = Button(root, text= "Set origin")
button.pack(side = LEFT)
button.bind('<ButtonPress-1>', lambda event: set_origin(test_servo))

root.mainloop()
