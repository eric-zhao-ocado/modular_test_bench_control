from pymodbus.client import ModbusTcpClient

PROTOS_X_HOST = '192.168.1.142'
PROX_1_ADDR = 0
PROX_2_ADDR = 1

client = ModbusTcpClient(PROTOS_X_HOST)

client.connect()

while True:
    # Slower but allows for inputs to be wired non-consecutively
    # prox_1_sense = client.read_discrete_inputs(PROX_1_ADDR, 1).bits[0]
    # prox_2_sense = client.read_discrete_inputs(PROX_2_ADDR, 1).bits[0]

    # Faster (more than 2x faster) but needs correct wiring (sensors in consecutive addresses)
    data = client.read_discrete_inputs(PROX_1_ADDR, 2)
    prox_1_sense = data.bits[0]
    prox_2_sense = data.bits[1]

    if(prox_1_sense and prox_2_sense):
        print("Both sensors activated.")
    elif(prox_1_sense):
        print("Only sensor 1 activated.")
    elif(prox_2_sense):
        print("Only sensor 2 activated")
    else:
        print("Nothing detected.")
