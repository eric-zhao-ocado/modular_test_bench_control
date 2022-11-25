"""
Constants related to controlling the SureServo2 drive through ENIP

CIP codes are noted by NAME_TYPE_NUM for easier search and autofills.
For example, instance 0 is MONITORING_INST_0.
"""
CPPPO_DATA_TYPES = {
    '(SINT)' : 8,
    '(INT)' : 16,
    '(DINT)' : 32
}

SERVO_DATA_OBJ_300 = 300

# Attributes related to monitoring the status and state of servo
MONITORING_INST_0 = 0
ALARM_ATTR = 1
MON_ONE_ATTR = 9
MON_ONE_SELECT_ATTR = 17
MON_SPEED_FEEDBACK_TYPE = 7
SPEED_FEEDBACK = 7
ABS_POS_TURNS = 51
ABS_POS_PUU = 52

MAX_PUU = 2147483647

# Attributes related to WHAT
BASIC_INST_1 = 1
OPERATION_MODE_ATTR = 1
E_GEAR_RATIO_NUM_ATTR = 44
# Probably won't need to change this unless gearbox is used
# (which may result in an irrational denominator value)
E_GEAR_NUM = 16777216
# Denominator represents pulses / 1 full revolution
E_GEAR_RATIO_DEN_ATTR = 45
E_GEAR_DEN = 100000

EXTENSION_INST_2 = 2
AUX_FUNC_ATTR_30 = 30
DISABLE_NV_WRITE = 5
# Set below to 1 to read pulse number, set to 0 to read PUU number
# (absolute position in PUU, affected by E-Gear ratio)
READ_DATA_SELECTION_ATTR = 70

DIAGNOSIS_INST_4 = 4
DIGITAL_INPUT_ATTR = 7


# Attributes related to controlling the servo paths
CONTROL_INST_5 = 5
HOMING_DEF_ATTR = 4
DEFINE_CURR_ORIGIN = 8
TRIG_POS_ATTR = 7
ACC_ONE_ATTR = 20
MIN_ACC = 1
MAX_ACC = 65500
DLY_ONE_ATTR = 40
MIN_DLY = 0
MAX_DLY = 32767
SPD_ONE_ATTR = 60

# Attributes related to defining the path definitions and data
PATH_INST_6 = 6
HOMING_ATTR = 0
# 0xB is the last path type ("Statement" type)
CONST_SPEED_TYPE = 1
POINT_POINT_STOP_TYPE = 2
POINT_POINT_PROCEED_TYPE = 3
MAX_TYPE_VALUE = 11
# Path definitions start at P6.002
PATH_ONE_ATTR = 2
CMD_ABS = 0
CMD_REL = 1
CMD_INC = 2
CMD_CAP = 3
