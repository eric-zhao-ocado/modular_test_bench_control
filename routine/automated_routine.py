from multiprocessing import dummy
import time
from threading import Timer
from pymodbus.client import ModbusTcpClient

PROTOS_X_HOST = '192.168.1.142'
PROX_1_ADDR = 0
PROX_2_ADDR = 1

REORIENT_TIMEOUT = 1.0
MAX_TIME = 5

routine_state = 0

protos_x = ModbusTcpClient(PROTOS_X_HOST)

if(protos_x.connect()):
    pass
else:
    print('No available connections.')

def dummy_arm_routine(location):
    time.sleep(1)
    pass

def stop_long_conveyor():
    pass

def run_long_conveyor():
    print('Running long conveyor forwards.')

# def reset_reorient():
#     global routine_state
#     routine_state = 1
#     time.sleep(1)
#     print('Running conveyeor backwards')
#     time.sleep(1)
#     routine_state = 0
#     t = Timer(REORIENT_TIMEOUT, reset_reorient)
#     t.start()

def reset_parcel():
    print('Running conveyor backwards.')
    time.sleep(2)

def check_prox_sensors():
    data = protos_x.read_discrete_inputs(PROX_1_ADDR, 2)
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


def routine():
    # Create a graphic that will help with this
    location = input('Pick Location: ')
    # Create a slider from 1% speed to 100% speed
    # Add mid points?
    # Need to do dual check saftey DCS
    speed = input('Speed: ')
    cycles = [0]
    cycles[0] = int(input('Number of cycles: '))

    # t = Timer(REORIENT_TIMEOUT, reset_reorient)
    # t.start()

    timer_start = time.time()

    while cycles[0] > 0:
        # Requires prox sensors to be wired to consecutive addresses
        if(check_prox_sensors()):
            dummy_arm_routine(location) # this can be shared between the manual and automated tests, find a way to import it
            cycles -= 1
            timer_start = time.time()
        elif time.time()-timer_start < MAX_TIME:
            run_long_conveyor()
        else:
            reset_parcel()
            timer_start = time.time()
            
    print("Automated routine finished.")

if __name__ == '__main__':
    routine()