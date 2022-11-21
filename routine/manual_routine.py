import time

import constants as c
import common_helpers
import conveyors

def manual_routine():
    pick_conveyor = conveyors.EnipServoConveyor(1400, 113000, 121, c.SERVO_DRIVE_HOST)
    location, speed = common_helpers.collect_params()

    common_helpers.check_ready()
    pick_conveyor.servo.send_command(300, 4, 7, 1)
    pick_conveyor.forward_two_third_length.trigger_path()
    time.sleep(5)
    pick_conveyor.backwards_one_third_length.trigger_path()
    time.sleep(5)
    pick_conveyor.go_home.trigger_path()

    print("Manual routine finished.")

if __name__ == '__main__':
    manual_routine()