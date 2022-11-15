from cpppo.server.enip import client
from cpppo.server.enip.get_attribute import attribute_operations
import common_helpers

HOST = "192.168.1.152"

SV2_DATA_OBJ = "@x300/"

DISABLE_NV_MEM_WRITES = "@0x300/2/60=(DINT)5"
ENABLE_SERVO = "@0x300/2/60=(DINT)1"
TRIGGER_PATH_1  = "@0x300/5/14=(DINT)1"
TRIGGER_PATH_5  = "@0x300/5/14=(DINT)5"
DISABLE_SERVO = "@0x300/2/60=(DINT)-1"
READ_IO = "@0x300/4/14"
STOP_SERVO = "@0x300/4/14=(DINT)60" # better to first read the value, change last bit to 1 or 0, and then return that value instead of hardcoding it herec
START_SERVO = "@0x300/5/14=(DINT)1"
STOP_SERVO_PATH = "@0x300/5/14=(DINT)6"
TEST = "@0x400/5/14=(DINT)6"
TEST_1 = "@0x300/2/0"
TEST_2 = "@0x300/2/2"
SET_PATH_1_DATA = "@0x300/6/6=(DINT)"

def send_command(tag):
    with client.connector(host=HOST) as conn:
        for index, descr, op, reply, status, value in conn.synchronous(
            operations=attribute_operations(
                tag, route_path=[], send_path='')):
            print(": %20s: %s" % (descr, value))
            return value
# Enable and disable servo not working??
# Maybe something to do with not being able to set it in batch command? Check later

def convert_dec(sint_arr):
    sum = 0
    print(sum)
    for val_pow, val in enumerate(sint_arr):
        sum += val * (256**val_pow)
    return sum

while True:
    num = int(input("Starting number: "))
    start = int(input("Starting bit: "))
    end = int(input("ending bit: "))
    value = int(input("new value: "))
    common_helpers.write_to_bits(num,(start, end), value)

send_command([DISABLE_NV_MEM_WRITES])
while True:
    # obj_class = input('Object Class Number: ')
    # instance = input('Instance Number: ')
    # attribute = input('Attribute Number (Parameter * 2): ')
    # command = ['@0x'+obj_class+'/'+instance+'/'+attribute]
    # val = convert_dec(send_command(command))
    # print('Returned value: ' + str(val))

    val = ''
    command = int(input("Next command: "))
    if command == 1:
        send_command([DISABLE_NV_MEM_WRITES])
    elif command == 2:
        send_command([ENABLE_SERVO])
    elif command == 3:
        send_command([TRIGGER_PATH_5])
    elif command == 4:
        send_command([DISABLE_SERVO])  
    elif command == 5:
        val = convert_dec(send_command([READ_IO]))
        val |= 1
        command = "@0x300/4/14=(DINT)" + str(val)
        print(command)
    elif command == 6:
        send_command([STOP_SERVO_PATH])
    elif command == 7:
        send_command([START_SERVO])
    elif command == 8:
        send_command([TEST_1, TEST_2])
    elif command == 9:
        rpm = int(input("RPM: ")) * 10
        command = SET_PATH_1_DATA + str(rpm)
        send_command([SET_PATH_1_DATA + str(rpm)])
        send_command([TRIGGER_PATH_1])
    else:
        print("invalid")      
# the =(TYPE)DATA signifies a SET operation
# DINT important here
# DATA IS RETURNED AS SIZE OF SINT, MAX VALUE OF 256 (array is [multiple of 1, multiple of 256, multiple of 65536, ... ])
# SINT = 1 BYTE (8 bits, unsigned), DINT = 4 BYTES (32 bits, unsigned)


        # client.connector.get_attribute_single()