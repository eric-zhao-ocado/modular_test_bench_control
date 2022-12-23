"""
Script to read and write to registers in the Yaskawa VFD drive through
ModbusTCP.
Useful for debugging when trying to work with Yaskawa VFD using Python.
"""
from pymodbus.exceptions import ConnectionException

import yaskawa_vfd_control as vfd_ctrl

def routine():
    """
    Function to read or write to registers.
    Read the Yaskawa V1000 documentaion to find the Modbus addresses.
    Search in the doc for "Addr. Hex" to navigate to the parameter addresses.
    """
    vfd_host = '192.168.1.20'

    vfd = vfd_ctrl.YaskawaVfd(vfd_host)
    while True:
        typ = input("Read or Write to addresses (R/W): ")
        if typ == 'R':
            addr = input("Address: ")
            try:
                # Reads 4 register values starting from the first address.
                data = vfd.send_command(
                    command=vfd.host.read_holding_registers,
                    addr=addr,
                    num=4
                    )
            except ConnectionException:
                print("Connection error try again.")
            else:
                print(f"Data: {data.registers}")
        elif typ == 'W':
            addr = input("Address: ")
            data = int(input("Write data: "))
            try:
                print(
                    vfd.send_command(
                        command=vfd.host.write_registers,
                        addr=addr,
                        data=data
                        )
                    )
            except ConnectionException:
                print('Connection error try again.')

if __name__ == '__main__':
    routine()
