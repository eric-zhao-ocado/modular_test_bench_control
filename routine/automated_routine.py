from pymodbus.client import ModbusTcpClient

import constants
import common_helpers
# USE PYTHON 3.8.0!!!!!

def automated_routine():
    protos_x = common_helpers.tcp_client_initialization(constants.PROTOS_X_HOST)

    
    location, speed = common_helpers.collect_params()

    cycles = int(input('Number of cycles: '))

    common_helpers.check_ready()

    common_helpers.run_short_conveyor()

    common_helpers.alignment_routine(protos_x, location, speed, cycles)
    print("Automated routine finished.")

if __name__ == '__main__':
    automated_routine()