import time
import atexit
import sure_servo_2_control as sv2_ctrl
import sure_servo_2_constants as sv2_const
import yaskawa_vfd_control as vfd_ctrl
import test_bench_constants as tb_const
import common_helpers
import conveyors
from fanucpy import Robot
# USE PYTHON 3.8.0!!!!!

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
    print("Exit")
    servo.exit_handler()
    vfd.exit_handler()
        

def automated_routine():
    pick_conveyor = conveyors.EnipServoConveyor(1400, 113000, 121, tb_const.SERVO_DRIVE_HOST)
    protos_x = common_helpers.tcp_client_initialization(tb_const.PROTOS_X_HOST)
    feed_conveyor = vfd_ctrl.YaskawaVfd(tb_const.VFD_HOST)
    robot = Robot(
    robot_model="Fanuc",
    host="192.168.1.52",
    port=18735,
    ee_DO_type="RDO",
    ee_DO_num=7,
    )
    robot.connect()
    atexit.register(exit_routine, servo=pick_conveyor.servo, vfd=feed_conveyor)
    cycles = int(input('Number of cycles: '))

    common_helpers.check_ready()
    feed_conveyor.change_freq(100)
    feed_conveyor.start_motor_forwards()
    start_time = time.perf_counter()
    speed_monitor = sv2_ctrl.Sv2Monitor(pick_conveyor.servo, 1, sv2_const.MON_SPEED_FEEDBACK_TYPE)
    pick_conveyor.servo.clear_alarms()
    pick_conveyor.servo.enable_servo()
    pick_conveyor.backwards_constant.trigger_path()
    while cycles > 0:
        if check_prox_sensors(protos_x):
            pick_conveyor.stop.trigger_path()
            while speed_monitor.check_value() != 0:
                pass
            pick_conveyor.forwards_distance.trigger_path()
            while speed_monitor.check_value() != 0:
                pass
            robot.move(
                "pose",
                vals=[268.701, -395.98, 100.0, 180.0, 0.0, 0.0],
                velocity=100,
                acceleration=100,
                cnt_val=0,
                linear=False
            )
            robot.move(
                "pose",
                vals=[268.701, -395.98, 200, -180, 0.0, 0.0],
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
                vals=[268.701, -395.98, 200, -180, 0.0, 0.0],
                velocity=100,
                acceleration=100,
                cnt_val=0,
                linear=False
            )
            cycles -= 1
            start_time = time.perf_counter()
            pick_conveyor.backwards_constant.trigger_path()
        elif time.perf_counter()-start_time < 3:
            pass
        else:
            pick_conveyor.forwards_one_length.trigger_path()
            while speed_monitor.check_value() != 0:
                pass
            pick_conveyor.backwards_constant.trigger_path()
            start_time = time.perf_counter()
        
    print("Automated routine finished.")


if __name__ == '__main__':
    automated_routine()