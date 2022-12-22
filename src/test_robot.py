"""
Script for moving a FANUC arm using fanucpy and GUI sliders.
"""

import multiprocessing
import tkinter
import atexit

import test_bench_constants as tb_cnst
from fanucpy import Robot

def gui_app(data:multiprocessing.Array, acc, event):
    """
    Process for updating the GUI app.
    """
    default_xy_pos = [100, 100, 300, 180.0, 0.0, 0.0]
    min_pos = [0, 0, -160, -180, 0, 0]
    max_pos = [500+90, 580+470, 500, -180, 0, 360]

    root = tkinter.Tk()

    joint_sliders = []
    for j in range(6):
        pos = tkinter.Scale(
            root,
            from_=min_pos[j],
            to=max_pos[j],
            orient=tkinter.HORIZONTAL,
            resolution=0.001,
            length=500
        )
        pos.pack()
        pos.set(default_xy_pos[j])
        joint_sliders.append(pos)

    accel_slider = tkinter.Scale(
        root,
        from_=1,
        to=100,
        orient=tkinter.HORIZONTAL,
        resolution=1,
        length=500
    )
    accel_slider.pack()

    while not event.is_set():
        for j in range(6):
            data[j] = joint_sliders[j].get()
        acc.value = accel_slider.get()
        root.update_idletasks()
        root.update()
    print("gui done")
    event.set()


def move_robot_routine(data, acc, event):
    """
    Process for moving the FANUC robot arm.
    """
    robot = Robot(
        robot_model="Fanuc",
        host="192.168.1.52",
        port=18735,
        ee_DO_type="RDO",
        ee_DO_num=7,
    )

    robot.__version__()
    robot.connect()

    while not event.is_set():
        x_1 = 2**0.5 / 2 * (data[0]-tb_cnst.X_OFFSET) + -2**0.5 / 2 * (data[1]-tb_cnst.Y_OFFSET)
        y_1 = 2**0.5 / 2 * (data[0]-tb_cnst.X_OFFSET) + 2**0.5 / 2 * (data[1]-tb_cnst.Y_OFFSET)
        robot.move(
            "pose",
            vals=[x_1, y_1, data[2], data[3], data[4], data[5]],
            velocity=20,
            acceleration=acc.value,
            cnt_val=0,
            linear=False,
        )
        print(robot.get_curjpos())
    print("robot done")
    event.set()

def exit_handler(event):
    """
    Set event to stop all processes on exit.
    """
    event.set()

if __name__ == '__main__':
    accel = multiprocessing.Value('i', 1)
    event_1 = multiprocessing.Event()
    origin = [0, 0, 100, -180, 0.0, 45]

    joint_pos = multiprocessing.Array('d', range(6))
    for i in range(6):
        joint_pos[i] = origin[i]
    p1 = multiprocessing.Process(
        target=gui_app,
        args=(joint_pos, accel, event_1)
    )
    p2 = multiprocessing.Process(
        target=move_robot_routine,
        args=(joint_pos, accel, event_1)
    )
    atexit.register(exit_handler, event_1)
    p1.start()
    p2.start()
    while True:
        pass
