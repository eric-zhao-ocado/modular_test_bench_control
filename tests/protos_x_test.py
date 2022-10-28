import time
from pymodbus.client import ModbusTcpClient

PROTOS_X_HOST = '192.168.1.142'
PROX_1_ADDR = 0
PROX_2_ADDR = 1

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

def routine():
    # Create a graphic that will help with this
    location = input('Pick Location: ')
    # Create a slider from 1% speed to 100% speed
    # Add mid points?
    # Need to do dual check saftey DCS
    speed = input('Speed: ')
    cycles = int(input('Number of cycles: '))

    while cycles > 0:
        timer_start = time.time()

        # Requires prox sensors to be wired to consecutive addresses
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

    print("Automated routine finished.")

if __name__ == '__main__':
    routine()