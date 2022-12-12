import multiprocessing
from multiprocessing import Process, Value, Array

from tkinter import *

from fanucpy import Robot


root = Tk()

joint_sliders = []
for i in range(6):
    pos = Scale(root, from_=0, to=25, orient=HORIZONTAL, resolution=0.01, length=500)
    pos.pack()
    joint_sliders.append(pos)
    
accel_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL, resolution=1, length=500)
accel_slider.pack()
# j1 = Scale(root, from_=0, to=50, orient=HORIZONTAL)
# j1.pack()
# j2 = Scale(root, from_=0, to=10, orient=HORIZONTAL)
# j2.pack()
# j3 = Scale(root, from_=0, to=10, orient=HORIZONTAL)
# j3.pack()
# j4 = Scale(root, from_=0, to=10, orient=HORIZONTAL)
# j4.pack()
# j5 = Scale(root, from_=0, to=10, orient=HORIZONTAL)
# j5.pack()
# j6 = Scale(root, from_=0, to=10, orient=HORIZONTAL)
# j6.pack()

def gui_app(data:Array, accel):
    while True:
        for j in range(6):
            data[j] = joint_sliders[j].get()
        accel.value = accel_slider.get()
        root.update_idletasks()
        root.update()

def move_robot_routine(data, accel):
    robot = Robot(
    robot_model="Fanuc",
    host="192.168.1.52",
    port=18735,
    ee_DO_type="RDO",
    ee_DO_num=7,
    )
    
    robot.__version__()
    robot.connect()
    while True:
        robot.move(
            "joint",
            vals=[data[0], data[1], data[2], data[3], data[4], data[5]],
            velocity=100,
            acceleration=accel.value,
            cnt_val=0,
            linear=False
        )
        print(f"Current pose: {robot.get_curpos()}")
        print(f"Current joints: {robot.get_curjpos()}")
        print(f"Energy consumption: {robot.get_ins_power()}")

if __name__ == '__main__':
    accel = Value('i', 1)
    joint_pos = Array('d', range(6))
    p1 = multiprocessing.Process(target=gui_app, args=(joint_pos, accel))
    p2 = multiprocessing.Process(target=move_robot_routine, args=(joint_pos, accel))
    p1.start()
    p2.start()
