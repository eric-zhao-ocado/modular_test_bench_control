"""
Constants related to controlling the Yaskawa V1000 VFD through ModbusTCP

May need to change some of the constants depending on the motor. These
constants are tailored to the motor currently attached to the conveyor
that I am making this for.
"""

VFD_DEFAULT_IP_ADDR = '192.168.1.20'

VFD_MAX_FREQ_HZ = 60