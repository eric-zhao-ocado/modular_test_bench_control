import time
from pymodbus.client import ModbusTcpClient
import time

client = ModbusTcpClient('192.168.1.142')

while True:
    try:
        print(client.write_coils(0,[1, 1, 1, 1, 1, 1, 1, 1])) #vacuum
        print(client.write_coils(8,[0, 0, 0, 0, 0, 0, 0, 0]))
        print("VACUUM")
        time.sleep(3)
        
        print(client.write_coils(8,[1, 1, 1, 1, 1, 1, 1, 1])) #vacuum
        print(client.write_coils(0,[0, 0, 0, 0, 0, 0, 0, 0]))
        time.sleep(0.1)
        print(client.write_coils(0,[1, 1, 1, 1, 1, 1, 1, 1])) #vacuum

        print("BLOW OFF")
        time.sleep(3)

    except KeyboardInterrupt:
        client.write_coils(16,[0,0]) #off
        print("Valve OFF. Exiting loop.")
        break

client.close()