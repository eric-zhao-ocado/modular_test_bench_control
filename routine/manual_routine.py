from pymodbus.client import ModbusTcpClient
from time import sleep

import constants
import common_helpers

def return_parcels():
    print('Running conveyor 1/3 backwards')
    sleep(1)


def manual_routine():
    protos_x = ModbusTcpClient(constants.PROTOS_X_HOST)
    common_helpers.initializations(protos_x)
    
    location, speed = common_helpers.collect_params()
    common_helpers.check_ready()

    common_helpers.run_short_conveyor()


    common_helpers.alignment_routine(protos_x, location, speed)

    sleep(constants.MANUAL_WAIT_TIME)
    return_parcels()

    print("Manual routine finished.")

if __name__ == '__main__':
    manual_routine()