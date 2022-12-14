from pymodbus.client import ModbusTcpClient
from cpppo.server.enip import client
from cpppo.server.enip.get_attribute import attribute_operations
import time

import conveyors
# REMINDER TO HAVE FEATURE TO JOG THE CONVEYOR SO THAT THE BELT IS AT THE RIGHT POSITION!!!
# BASICALLY PUT A HOMING FUNCTION FOR MANUAL TESTS AT BEGINNING OF PROCEDURE

# Split this into separate files, have classes for conveyors?

def tcp_client_initialization(host):
    protos_x = ModbusTcpClient(host)
    print('Connecting to Protos X...')
    while(not protos_x.connect()):
        print('No available connections.')
        while(input('Enter "Y" when ready: ') != 'Y'):
            pass
        print('Attempting to connect...')
    print('Connected.')
    return protos_x

def enip_send_command(host, tags):
    with client.connector(host) as conn:
        for index, descr, op, reply, status, value in conn.synchronous(
            operations=attribute_operations(
                tags, route_path=[], send_path='')):
            print(": %20s: %s" % (descr, value))
            return value


def dummy_arm_routine(location, speed):
    print('Running arm routine')
    time.sleep(1)
    pass


def run_short_conveyor():
    print('Set short conveyor to running forwards.')

def reset_parcel():
    print('Running conveyor backwards.')
    time.sleep(2)

def check_ready():
    while (input('Input "Y" to start: ') != 'Y'):
        pass


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

# Start bit is LSB (index starts at 0), end bit is MSB
def write_to_bits(bitfield, start_bit, num_bits, value):
    if(2 ** num_bits - 1 >= value):
        temp = value << start_bit
        bitfield |= temp
        print(bin(bitfield))
    else:
        print("Error writing value to register. Value too large.")



def alignment_routine(pick_conveyor:conveyors.EnipServoConveyor, protos_x, location, speed, cycles:int =1):
    start_time = time.perf_counter()
    pick_conveyor.forward_constant.trigger_path()
    
    while cycles > 0:
        # Requires prox sensors to be wired to consecutive addresses
        
        if(check_prox_sensors(protos_x)):
            pick_conveyor.stop.trigger_path()
            dummy_arm_routine(location, speed) # this can be shared between the manual and automated tests, find a way to import it
            cycles -= 1
            time.sleep(5)
            start_time = time.perf_counter()
            pick_conveyor.forward_constant.trigger_path()
        elif time.perf_counter()-start_time < 5:
            pass
        else:
            pick_conveyor.backwards_one_length.trigger_path()
            start_time = time.perf_counter()