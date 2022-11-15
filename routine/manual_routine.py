import time

import constants
import common_helpers

def return_parcels():
    common_helpers.enip_send_command(constants.SERVO_DRIVE_HOST,constants.STOP_SERVO_PATH)
    print('Running conveyor 1/3 backwards')
    
    time.sleep(1)


def manual_routine():
    protos_x = common_helpers.tcp_client_initialization(constants.PROTOS_X_HOST)

    location, speed = common_helpers.collect_params()
    common_helpers.check_ready()
    conveyor_rpm = int(input("Default Conveyor RPM: ")) * 10
    common_helpers.run_short_conveyor(conveyor_rpm)


    common_helpers.alignment_routine(protos_x, location, speed)

    time.sleep(constants.MANUAL_WAIT_TIME)
    return_parcels()

    print("Manual routine finished.")

if __name__ == '__main__':
    manual_routine()