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
    
def edit_path():
    window = Toplevel(root)
    window.grab_set()
    
    button = Button(window, text="Some editing stuff")
    button.pack(side=LEFT)
    
def start_path(path:sv2_ctrl.Sv2PointPoint):
    path.trigger_path()
    
num = 0

def add_path(path_list):
    
    window = Toplevel(root)
    window.grab_set()
    
    button = Button(window, text="Some editing stuff")
    button.pack(side=LEFT)

    butt = Button(root, text="Edit Path")
    butt.pack(side=BOTTOM)
    butt.bind('<ButtonPress-1>', lambda event: edit_path())
    

test_servo = sv2_ctrl.Sv2Servo(tb_const.SERVO_DRIVE_HOST, 933)
test_servo.enable_servo()
moved_path = sv2_ctrl.Sv2ConstSpeed(test_servo, 1)
stopped_path = sv2_ctrl.Sv2ConstSpeed(test_servo, 2)

w = Scale(root, from_=0, to=932, orient=HORIZONTAL)
w.pack()

for test_direction in ("forward", "backward"):
    button = Button(root, text=test_direction)
    button.pack(side=LEFT)
    button.bind('<ButtonPress-1>', lambda event, dir=test_direction:
        start_motor(dir, moved_path, w))
    button.bind('<ButtonRelease-1>', lambda event: stop_motor(stopped_path))

button = Button(root, text= "Set origin")
button.pack(side = LEFT)
button.bind('<ButtonPress-1>', lambda event: set_origin(test_servo))

list_of_paths = []

button = Button(root, text="Add Path")
button.pack(side=BOTTOM)
button.bind('<ButtonPress-1>', lambda event: add_path(list_of_paths))

button = Button(root, text="Start Routine")
button.pack(side=RIGHT)
button.bind('<ButtonPress-1>', lambda event: start_path(list_of_paths[0]))

root.mainloop()
