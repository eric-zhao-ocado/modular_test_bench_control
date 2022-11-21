PROTOS_X_HOST = '192.168.1.142'
PROX_1_ADDR = 0
PROX_2_ADDR = 1

SERVO_DRIVE_HOST = '192.168.1.152'

REORIENT_TIMEOUT = 1.0
MAX_TIME = 5
MANUAL_WAIT_TIME = 1

SERVO_DATA_OBJ = 300

# SureServo2 Constant Speed Control
CONST_SPEED_TYPE = 1
POINT_POINT_TYPE = 2

# Attributes related to monitoring the status and state of servo
MONITORING_INST = 0
ALARM_ATTR = 1
ABS_POS_TURNS = 51
# PUU OR PULSE??? WHAT DOES THIS MEAN?
ABS_POS_PUU = 52

MAX_PUU = 2147483647

# Attributes related to WHAT
BASIC_INST = 1
OPERATION_MODE_ATTR = 1
E_GEAR_RATIO_NUM_ATTR = 44
# Probably won't need to change this unless gearbox is used (which may result in an irrational denominator value)
E_GEAR_NUM = 16777216
# Denominator represents pulses / 1 full revolution
E_GEAR_RATIO_DEN_ATTR = 45
E_GEAR_DEN = 100000

EXTENSION_INST = 2
# Set below to 1 to read pulse number, set to 0 to read PUU number (absolute position in PUU) <- does e-gear ratio affect this? TEST!
READ_DATA_SELECTION_ATTR = 70

# Attributes related to controlling the servo paths
CONTROL_INST = 5
HOMING_DEF_ATTR = 4
DEFINE_CURR_ORIGIN = 8
TRIG_POS_ATTR = 7
FIRST_ACC_ATTR = 20
MIN_ACC = 1
MAX_ACC = 65500
FIRST_DLY_ATTR = 40
MIN_DLY = 0
MAX_DLY = 32767
FIRST_SPD_ATTR = 60

# Attributes related to defining the path definitions and data
PATH_INST = 6
HOMING_ATTR = 0
# 0xB is the last path type ("Statement" type)
MAX_TYPE_VALUE = 11
# Path definitions start at P6.002
FIRST_PATH_ATTR = 2
CMD_ABS = 0
CMD_REL = 1
CMD_INC = 2
CMD_CAP = 3
# RPM has a unit of 0.1 rpm, so this is really 933 rpm
# Do not exceed max speed that conveyor is designed for
DORNER_PRECISION_2200_MAX_RPM = 933
