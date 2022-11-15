PROTOS_X_HOST = '192.168.1.142'
PROX_1_ADDR = 0
PROX_2_ADDR = 1

SERVO_DRIVE_HOST = '192.168.1.152'

REORIENT_TIMEOUT = 1.0
MAX_TIME = 5
MANUAL_WAIT_TIME = 1


# SureServo2 object class, instance, attributes
READ_ALARM = ['@0x300/0/2']

# RPM has a unit of 0.1 rpm, so this is really 933 rpm
MAX_RPM = 9330

SERVO_DATA_OBJ = 300

# SureServo2 Constant Speed Control
CONST_SPEED_TYPE = 1
PATH_INST = 6
CONTROL_INST = 5
# ^^ enumerate the instances?

# need better way of organizing this stuff
TRIG_POS_CMD = 7
PATH_START_INDEX = (6, 2)
ACC_TIME_START_INDEX = (5, 20)