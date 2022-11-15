# REMINDER TO HAVE FEATURE TO JOG THE CONVEYOR SO THAT THE BELT IS AT THE RIGHT POSITION!!!







from cpppo.server.enip import client
from cpppo.server.enip.get_attribute import attribute_operations

HOST = "192.168.1.152"
DISABLE_NV_MEM_WRITES = "@0x300/2/60=(DINT)5"
ENABLE_SERVO = "@0x300/2/60=(DINT)1"
TRIGGER_PATH_1  = "@0x300/5/14=(DINT)1"
TRIGGER_PATH_5  = "@0x300/5/14=(DINT)5"
DISABLE_SERVO = "@0x300/2/60=(DINT)-1"
READ_IO = "@0x300/4/14"
STOP_SERVO = "@0x300/4/14=(DINT)60" # better to first read the value, change last bit to 1 or 0, and then return that value instead of hardcoding it herec
START_SERVO = "@0x300/4/14=(DINT)61"
STOP_SERVO_PATH = "@0x300/5/14=(DINT)6"

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


send_command([DISABLE_NV_MEM_WRITES])



while True:
    pass
# the =(TYPE)DATA signifies a SET operation
# DINT important here
# DATA IS RETURNED AS SIZE OF SINT, MAX VALUE OF 256 (array is [multiple of 1, multiple of 256, multiple of 65536, ... ])
# SINT = 1 BYTE (8 bits, unsigned), DINT = 4 BYTES (32 bits, unsigned)


        # client.connector.get_attribute_single()