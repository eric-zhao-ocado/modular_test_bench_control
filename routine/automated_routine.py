import time
from threading import Timer
from pymodbus.client import ModbusTcpClient

PROTOS_X_HOST = '192.168.1.142'
PROX_1_ADDR = 0
PROX_2_ADDR = 1

REORIENT_TIMEOUT = 1.0

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

def reset_reorient():
    global routine_state
    routine_state = 1
    time.sleep(1)
    print('Running conveyeor backwards')
    time.sleep(1)
    routine_state = 0
    t = Timer(REORIENT_TIMEOUT, reset_reorient)
    t.start()

def routine():
    # Create a graphic that will help with this
    location = input('Pick Location: ')
    # Create a slider from 1% speed to 100% speed
    # Add mid points?
    # Need to do dual check saftey DCS
    speed = input('Speed: ')
    cycles = int(input('Number of cycles: '))

    t = Timer(REORIENT_TIMEOUT, reset_reorient)
    t.start()

    while cycles > 0:
        # Requires prox sensors to be wired to consecutive addresses
        if (not routine_state):
            data = protos_x.read_discrete_inputs(PROX_1_ADDR, 2)
            prox_1_sense = data.bits[0]
            prox_2_sense = data.bits[1]

            if(prox_1_sense and prox_2_sense):
                print("Both sensors activated.")
                dummy_arm_routine(location)
                cycles -= 1
            elif(prox_1_sense):
                print("Only sensor 1 activated.")
            elif(prox_2_sense):
                print("Only sensor 2 activated")
            else:
                print("Nothing detected.")
    t.cancel()
    print("Automated routine finished.")

if __name__ == '__main__':
    routine()