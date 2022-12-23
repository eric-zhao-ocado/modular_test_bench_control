"""
Script to test control of vacuum cups through ModbusTCP coupler ProtosX
Setting an output to 1 sets the voltage level to LOW, setting it to 0
sets voltage level to HIGH.
"""

import time

import protos_x_control as px_ctrl

client = px_ctrl.ProtosX('192.168.1.142')

while True:
    try:
        # Open vacuum valves
        client.vacuum(1)
        print("VACUUM")
        time.sleep(3)

        # # Close vacuum valves
        client.blowoff()
        print("BLOW OFF")
        time.sleep(3)

    except KeyboardInterrupt:
        # Close all valves
        client.exit_handler()
        print("Valves OFF. Exiting loop.")
        break
