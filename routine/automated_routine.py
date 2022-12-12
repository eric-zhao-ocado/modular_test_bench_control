import sure_servo_2_control
import sure_servo_2_constants as sv2_const
import yaskawa_vfd_control
import common_helpers
import conveyors
# USE PYTHON 3.8.0!!!!!

def automated_routine():
    pick_conveyor = conveyors.EnipServoConveyor(1400, 113000, 121, c.SERVO_DRIVE_HOST)
    protos_x = common_helpers.tcp_client_initialization(c.PROTOS_X_HOST)

    location, speed = common_helpers.collect_params()

    cycles = int(input('Number of cycles: '))

    common_helpers.check_ready()

    common_helpers.run_short_conveyor()
    common_helpers.alignment_routine(pick_conveyor, protos_x, location, speed, cycles)
    print("Automated routine finished.")


if __name__ == '__main__':
    automated_routine()