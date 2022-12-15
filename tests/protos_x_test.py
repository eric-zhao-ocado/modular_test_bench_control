import time
from pymodbus.client import ModbusTcpClient

PROTOS_X_HOST = '192.168.1.142'
PROX_1_ADDR = 0
PROX_2_ADDR = 1

protos_x = ModbusTcpClient(PROTOS_X_HOST)

while not protos_x.connect:
    print("noo")

print(protos_x.read_discrete_inputs(0))
print(protos_x.read_coils(0))
print(protos_x.write_coil(1,False))
print(protos_x.write_register(1, 1))
