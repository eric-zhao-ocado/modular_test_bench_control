# Sample code of GUI for jogging the motor
# Will be used for the MANUAL TEST, to recalibrate the conveyor
# Essentially line up marking on the conveyor with marking on the extrusion
from tkinter import *

import constants as c
import sure_servo_2_control

running = False
root = Tk()
jobid = None

def start_motor(direction, path, slider):
    print("starting motor...(%s)" % direction)
    speed = slider.get()
    if (direction == "forward"):
        path.change_speed(speed*10)
    else:
        path.change_speed(-speed*10)
    path.trigger_path()

def stop_motor(path):
    path.change_speed(0)
    path.trigger_path()

def set_origin(servo:sure_servo_2_control.Enip_Server):
    print("setting origin...")
    servo.send_command(300, 5, 7, 0)


servo = sure_servo_2_control.Enip_Server(c.SERVO_DRIVE_HOST)
servo.send_command(300, 4, 7, 1)
path = sure_servo_2_control.SV2_Const_Speed(servo, 1)
stopped_path = sure_servo_2_control.SV2_Const_Speed(servo, 2)

w = Scale(root, from_=0, to=932, orient=HORIZONTAL)
w.pack()

for direction in ("forward", "backward"):
    button = Button(root, text=direction)
    button.pack(side=LEFT)
    button.bind('<ButtonPress-1>', lambda event, direction=direction: start_motor(direction, path, w))
    button.bind('<ButtonRelease-1>', lambda event: stop_motor(stopped_path))

button = Button(root, text= "Set origin")
button.pack(side = LEFT)
button.bind('<ButtonPress-1>', lambda event: set_origin(servo))

root.mainloop()