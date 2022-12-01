from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException

VFD_HOST = '192.168.1.20'

protos_x = ModbusTcpClient(VFD_HOST)

if(protos_x.connect()):
    pass
else:
    print('No available connections.')

def routine():
    while True:
        # Requires prox sensors to be wired to consecutive addresses
        typ = input("R or W: ")
        if typ == 'R':
            addr = int(input("Address: "), 16) - 1
            try:
                data = protos_x.read_holding_registers(int(addr), 5)
            except ConnectionException:
                print("connection error try again")
            else:
                print(f"data: {data.registers}")
        elif typ == 'W':
            addr = int(input("Address: "), 16) - 1
            data = int(input("Data: "))
            try:
                print(protos_x.write_registers(int(addr), data))
            except ConnectionException:
                print('connection error try again')
        
if __name__ == '__main__':
    routine()