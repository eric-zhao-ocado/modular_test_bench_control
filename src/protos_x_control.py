"""
Module for controlling vacuum valves and reading from proximity sensors
using a ProtosX ModbusTCP coupler.
"""

import time

from pymodbus.client import ModbusTcpClient

import test_bench_constants as tb_const

class ProtosX:
    """
    ProtosX object for ModbusTCP I/O communication.
    """
    def __init__(self, ip_addr):
        """
        Initializes ProtosX ModbusTCP object.

        Args:
            ip_addr: IP address of ProtosX
        """
        self.client = ModbusTcpClient(ip_addr)
        self.client.connect()
        # Close all valves.
        self.client.write_coils(0, [0, 0, 0, 0, 0, 0, 0, 0])
        self.client.write_coils(8, [0, 0, 0, 0, 0, 0, 0, 0])

    def check_prox_sensors(self):
        """
        Checks to see if the proximity sensors are detecting anything.

        Args:
            protos_x: ProtosX ModbusTCP client.

        Returns:
            bool: True if both sensors detect an object, false otherwise.
        """
        data = self.client.read_discrete_inputs(tb_const.PROX_1_ADDR, 2)
        try:
            prox_1_sense = data.bits[0]
            prox_2_sense = data.bits[1]
            if prox_1_sense and prox_2_sense:
                return True
            return False
        except AttributeError:
            return False

    def exit_handler(self):
        """
        Closes all valves and closes connection to ProtosX.
        """
        while True:
            try:
                self.client.connect()
                self.blowoff()
                print("Closing vacuum")
                self.client.write_coils(0, [0, 0, 0, 0, 0, 0, 0, 0])
                print("Closing blowoff")
                self.client.write_coils(8, [0, 0, 0, 0, 0, 0, 0, 0])
            except Exception:
                print("Exception")
            else:
                break
        self.client.close()

    def vacuum(self, valve):
        """
        Opens vacuum valves and closes blowoff valves.
        """
        # Open vacuum valves
        self.client.write_coils(valve - 1, 1)
        # Close blowoff valves
        self.client.write_coils(8, [0, 0, 0, 0, 0, 0, 0, 0])

    def blowoff(self):
        """
        Opens the blowoff valves and closes vacuum valves.
        """
        # Open blowoff valves
        self.client.write_coils(8, [1, 1, 1, 1, 1, 1, 1, 1])
        # Close vacuum valves
        self.client.write_coils(0, [0, 0, 0, 0, 0, 0, 0, 0])
        # Only need to blow-off for a very short amount of time.
        time.sleep(0.2)
        # Close blowoff valves
        self.client.write_coils(8, [0, 0, 0, 0, 0, 0, 0, 0])
