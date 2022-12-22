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

# Starting point (Robot coordinate axes)
DEFAULT_X = 268.701
DEFAULT_Y = -395.98

# Perform 45 deg rotation matrix on origin x-y axes, and then offset the origin
X_OFFSET = - (2**0.5 / 2 * (DEFAULT_X) + 2**0.5 / 2 * (DEFAULT_Y))
Y_OFFSET = 2**0.5 / 2 * (DEFAULT_X) - 2**0.5 / 2 * (DEFAULT_Y)

# Limits for the robot arm travel (Robot coordinate axes).
MAX_X = 640.895
MIN_X = -473.762
MAX_Y = 763.676
MIN_Y = -395.99
MAX_Z = 500
MIN_Z = -440
