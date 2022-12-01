"""
Module for VERY basic control of a conveyor motor through the Yaskawa
V1000 VFD using its ModbusTCP communication card.

Functions are designed for use with the basic test bench setup, and are
limited to essentially running the motor continuously forwards or
backwards at a set frequency.

Follow the ModbusTCP initial setup instructions in the manual to enable
ModbusTCP network communication before initiating any comms.
"""

import atexit

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException

import yaskawa_vfd_constants as vfd_const

class YaskawaVfd:
    """
    Basic class for control of the Yaskawa V1000 drive.
    """
    def __init__(self, ip_addr):
        self.ip_addr = ip_addr
        self.host = ModbusTcpClient(ip_addr)
        
    def send_command(self, command, addr, num=None, data=None):
        addr = int(addr, 16) - 1
        while True:
            try:
                if data is None:
                    command(addr, num)
                else:
                    command(addr, data)
            except ConnectionException:
                print("Connection broken, retrying...")
            else:
                break
            
        
    def initial_setup(self):
        self.host = ModbusTcpClient(vfd_const.VFD_DEFAULT_IP_ADDR)
        self.send_command(self.host.write_registers, '0180', data=3)
        self.send_command(self.host.write_registers, '0181', data=3)
        self.send_command(self.host.write_registers, '03A2', data=0)
        
if __name__ == "__main__":
    test_drive = YaskawaVfd(vfd_const.VFD_DEFAULT_IP_ADDR)
    test_drive.initial_setup()