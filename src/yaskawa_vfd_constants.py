"""
Constants related to controlling the Yaskawa V1000 VFD through ModbusTCP

May need to change some of the constants depending on the motor. These
constants are tailored to the motor currently attached to the conveyor
that I am making this for.
"""

VFD_DEFAULT_IP_ADDR = '192.168.1.20'

VFD_MAX_FREQ_HZ = 60

MOTOR_OPERATION_ADDR = '0001'
MOTOR_FREQUENCY_ADDR = '0002'

INITIALIZE_PARAM_ADDR = '0103'
USER_INITIALIZE = 1110
FREQ_REF_SELEC_ADDR = '0180'
RUN_CMD_SELEC_ADDR = '0181'
OPTION_PCB = 3

COMM_PARAM_RESET_ADDR = '036A'
RESET_PARAM = 1
IP_OCTET_ADDR = ['03E5', '03E6', '03E7', '03E8']
ADDR_STARTUP_MODE_ADDR = '03F1'
STATIC_OPTION = 0

POWER_LOSS_OPER_ADDR = '0485'
CPU_POWER_ACTIVE = 2
COMM_ENTER_FUNC_ADDR = '043C'
NO_ENTER_NEEDED = 0

USER_PARAM_DEFAULT_ADDR = '0507'
CLEAR_USER_PARAM = 2

AUTO_TUNE_MODE_ADDR = '0701'
STATIONARY_TUNE = 2
MOTOR_RATED_POWER_ADDR = '0702'
# Horsepower to kW conversion included, rounded to 2 decimal places
MOTOR_RATED_POWER = round(3/8 * 0.746, 2)
MOTOR_RATED_VOLTAGE_ADDR = '0703'
MOTOR_RATED_VOLTAGE = 230
MOTOR_RATED_CURRENT_ADDR = '0704'
MOTOR_RATED_CURRENT = 1.9
START_AUTO_TUNE_ADDR = '710'

EEPROM_ENTER_ADDR = '900'
