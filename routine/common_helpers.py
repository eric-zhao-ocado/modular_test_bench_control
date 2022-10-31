import time

import constants

# Split this into separate files, have classes for conveyors?

def initializations(protos_x):
    print('Connecting to Protos X...')
    while(not protos_x.connect()):
        print('No available connections.')
        while(input('Enter "Y" when ready: ') != 'Y'):
            pass
        print('Attempting to connect...')
    print('Connected.')

def dummy_arm_routine(location, speed):
    print('Running arm routine')
    time.sleep(1)
    pass

def stop_long_conveyor():
    pass

def run_long_conveyor():
    print('Running long conveyor forwards.')

def run_short_conveyor():
    print('Set short conveyor to running forwards.')

def reset_parcel():
    print('Running conveyor backwards.')
    time.sleep(2)

def check_ready():
    while (input('Input "Y" to start: ') != 'Y'):
        pass

def check_prox_sensors(protos_x):
    data = protos_x.read_discrete_inputs(constants.PROX_1_ADDR, 2)
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

# ORRRRRR input dimensions of parcel LxHxW, H being the shortest side
def collect_params():
    # Create a graphic that will help with this
    # Make the same thing that they see on the teach pendant, but easily adjustable
    location = input('Pick Location: ')
    # Create a slider from 1% speed to 100% speed
    # Add mid points?
    # Need to do dual check saftey DCS
    speed = input('Speed: ')
    return location, speed

def alignment_routine(protos_x, location, speed, cycles:int =1):
    start_time = time.time()

    while cycles > 0:
        # Requires prox sensors to be wired to consecutive addresses
        if(check_prox_sensors(protos_x)):
            dummy_arm_routine(location, speed) # this can be shared between the manual and automated tests, find a way to import it
            cycles -= 1
            start_time = time.time()
        elif time.time()-start_time < constants.MAX_TIME:
            run_long_conveyor()
        else:
            reset_parcel()
            start_time = time.time()