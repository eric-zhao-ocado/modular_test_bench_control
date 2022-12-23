import test_bench_constants as tb_cnst
import time
from fanucpy import Robot

robot = Robot(
    robot_model="Fanuc",
    host=tb_cnst.ROBOT_HOST,
    port=18735,
    ee_DO_type="RDO",
    ee_DO_num=7,
)
robot.connect()

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

def move_arm(x, y, z):
    # Check if the movement command is within the bounds of the testbench.
    if (
        tb_cnst.MIN_X < x < tb_cnst.MAX_X
        and tb_cnst.MIN_Y < y < tb_cnst.MAX_Y
    ):
        try:
            print("\n")
            print(f'{"Calling move command:":<31}{time.perf_counter()}')
            start_time = time.perf_counter()
            robot.move(
                "pose",
                vals=[x, y, z, 180, 0, 0],
                velocity=100,
                acceleration=100,
                cnt_val=0,
                linear=False,
            )
            end_time = time.perf_counter()
            print(f"Move delay time: {end_time-start_time}")
        # Except the generic exception raised "position-is-not-reachable"
        except Exception as exception:
            print(repr(exception))
    # Clear the move arm event.
        
while True:
    # print(f"Joint position: {robot.get_curjpos()}")
    # print(f"Carte position: {robot.get_curpos()}")
    # x = int(input("x: "))
    # y = int(input("y: "))
    # z = int(input("z: "))
    x = 0
    for i in range(500):
        x += 1
        x_new, y = rotate_45_deg(x, 0)
        move_arm(x_new, y, 300)
        print(f"x vale: {x}")
   
    