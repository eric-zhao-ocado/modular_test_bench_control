"""
Constants related to the test bench setup.
"""
PROTOS_X_HOST = '192.168.1.142'
PROX_1_ADDR = 0
PROX_2_ADDR = 1

SERVO_DRIVE_HOST = '192.168.1.10'
SERVO_DRIVE_MAX_RPM = 3000

VFD_HOST = '192.168.1.20'

ROBOT_HOST = '192.168.1.52'

REORIENT_TIMEOUT = 1.0
MAX_TIME = 5
MANUAL_WAIT_TIME = 1

DEFAULT_X = 268.701
DEFAULT_Y = -395.98
MAX_CONVEYOR_POSITION = 447746

# Perform 45 deg rotation matrix on origin x-y axes, and then offset the origin
# Formula: - (2**0.5 / 2 * (DEFAULT_X) + 2**0.5 / 2 * (DEFAULT_Y))
X_OFFSET = 89.99984400264259
# Formula: - (2**0.5 / 2 * (DEFAULT_X) - 2**0.5 / 2 * (DEFAULT_Y))
Y_OFFSET = 470.0004424258557

MAX_X = 685.895
MIN_X = -473.762
MAX_Y = 763.676
MIN_Y = -395.99
