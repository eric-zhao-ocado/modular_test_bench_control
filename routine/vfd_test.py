from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException

import yaskawa_vfd_control as vfd_ctrl

VFD_HOST = '192.168.1.20'

vfd = vfd_ctrl.YaskawaVfd(VFD_HOST)

if(vfd.host.connect()):
    pass
else:
    print('No available connections.')

def routine():
    while True:
        typ = input("R or W: ")
        if typ == 'R':
            addr = input("Address: ")
            try:
                data = vfd.send_command(vfd.host.read_holding_registers, addr, 4)
            except ConnectionException:
                print("connection error try again")
            else:
                print(f"data: {data.registers}")
        elif typ == 'W':
            addr = input("Address: ")
            data = int(input("Data: "))
            try:
                print(vfd.send_command(vfd.host.write_registers, addr, data))
            except ConnectionException:
                print('connection error try again')

if __name__ == '__main__':
    routine()