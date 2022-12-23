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
from pymodbus.exceptions import ModbusIOException

import yaskawa_vfd_constants as vfd_const

class YaskawaVfd:
    """
    Basic class for control of the Yaskawa V1000 drive.
    """
    def __init__(self, ip_addr):
        self.ip_addr = ip_addr
        self.host = ModbusTcpClient(ip_addr)

    def send_command(self, command, addr, num=1, data=None):
        """
        Sends the specified command to the VFD through ModbusTCP

        Args:
            command: ModbusTCP function.
            addr: Address of register being read or written to.
            num: Number of registers to be read from.
            data: Data to write to register.
        """
        addr = int(addr, 16) - 1
        while True:
            try:
                if data is None:
                    reg_data = command(addr, num)
                else:
                    reg_data = command(addr, data)
            except ConnectionException:
                print(ConnectionException)
            except ModbusIOException:
                print(ModbusIOException)
            else:
                return reg_data

    def write_register(self, addr, data):
        """
        Writes data to specified register address.

        Args:
            addr: Address of register being read or written to.
            data: Data to write to register.
        """
        return self.send_command(self.host.write_registers, addr, data=data)

    def read_regs(self, addr, num=1):
        """
        Reads data starting from specified register address.

        Args:
            addr: Address of register being read or written to.
            num: Number of registers to be read from.
        """
        return self.send_command(self.host.read_holding_registers, addr, num)

    def initial_setup(self):
        """
        Performs the initial setup of a Yaskawa VFD drive motor.
        Only needs to be run once on a fresh servo drive and motor.
        """
        self.host = ModbusTcpClient(vfd_const.VFD_DEFAULT_IP_ADDR)
        self.host.connect()
        self.write_register(
            vfd_const.COMM_ENTER_FUNC_ADDR,
            vfd_const.NO_ENTER_NEEDED
        )
        # Stationary auto tune motor parameters.
        self.write_register(
            vfd_const.AUTO_TUNE_MODE_ADDR,
            vfd_const.STATIONARY_TUNE
        )
        self.write_register(
            vfd_const.MOTOR_RATED_POWER_ADDR,
            int(vfd_const.MOTOR_RATED_POWER * 100)
        )
        self.write_register(
            vfd_const.MOTOR_RATED_CURRENT_ADDR,
            int(vfd_const.MOTOR_RATED_CURRENT * 100)
        )
        # Select Option PCB for network communications
        self.write_register(
            vfd_const.FREQ_REF_SELEC_ADDR,
            vfd_const.OPTION_PCB
        )
        self.write_register(
            vfd_const.RUN_CMD_SELEC_ADDR,
            vfd_const.OPTION_PCB
        )
        # Select static address option.
        self.write_register(
            vfd_const.ADDR_STARTUP_MODE_ADDR,
            vfd_const.STATIC_OPTION
        )
        # Set IP address.
        ip_addr_octets = str(self.ip_addr).split('.')
        print(ip_addr_octets)
        for num, octet in enumerate(ip_addr_octets):
            self.write_register(
                vfd_const.IP_OCTET_ADDR[num],
                int(octet)
            )
        # Save to EEPROM
        # DO NOT USE THIS TOO OFTEN, MAXIMUM 100,000 WRITES
        self.write_register(vfd_const.EEPROM_ENTER_ADDR, 0)
        # Power cycle drive to set parameters
        while input("Power cycled drive (Y/N): ") != 'Y':
            pass
        # User needs to start the auto-tuning procedure on the drive.
        print("Starting auto-tuning on drive...")
        self.write_register(
            vfd_const.START_AUTO_TUNE_ADDR,
            1,
        )
        while self.read_regs(vfd_const.START_AUTO_TUNE_ADDR).registers[0] > 0:
            pass
        self.host = ModbusTcpClient(self.ip_addr)
        while not self.host.connect():
            print("Unable to connect, recheck initialization.")
            return False
        self.write_register(
            vfd_const.POWER_LOSS_OPER_ADDR,
            vfd_const.CPU_POWER_ACTIVE
        )
        print("Finished initialization.")
        return True

    def change_freq(self, percentage):
        """
        Changes VFD frequency up to the max frequency.

        Args:
            percentage: Percentage of max speed
        """
        freq = round(vfd_const.VFD_MAX_FREQ_HZ / 100.0 * percentage)
        if 0 <= freq <= vfd_const.VFD_MAX_FREQ_HZ:
            self.write_register(vfd_const.MOTOR_FREQUENCY_ADDR, freq * 100)

    def stop_motor(self):
        """
        Stops the motor.
        """
        self.write_register(vfd_const.MOTOR_OPERATION_ADDR, 0)

    def start_motor_forwards(self):
        """
        Starts motor in forwards direction.
        """
        self.write_register(vfd_const.MOTOR_OPERATION_ADDR, 1)

    def start_motor_reverse(self):
        """
        Starts motor in reverse direction.
        """
        self.write_register(vfd_const.MOTOR_OPERATION_ADDR, 2)

    def exit_handler(self):
        """
        Exit routine to stop motor whenever code is exited.
        """
        self.stop_motor()
        self.change_freq(0)


if __name__ == "__main__":
    test_drive = YaskawaVfd('192.168.1.20')
    atexit.register(test_drive.exit_handler)
    if input("Initial setup (Y/N): ") == 'Y':
        test_drive.initial_setup()
    test_drive.start_motor_forwards()
    while True:
        percent = int(input('Speed (%): '))
        test_drive.change_freq(percent)
    