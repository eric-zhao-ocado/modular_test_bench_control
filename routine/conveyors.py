import sure_servo_2_control as sv2_c
from pymodbus.client import ModbusTcpClient as mb_tcp_c

import constants as c

class Conveyor:
    def __init__(self, top_length, max_speed, turn_circum):
        self.top_length = top_length
        self.max_rpm = int(max_speed/turn_circum/2) * 10
        self.turns_per_length = top_length/turn_circum
        print (self.turns_per_length)
    
    def __str__(self):
        return f'Servo Motor Conveyor.\
            \nConveyor Length[mm]: {self.top_length}\
            \nMax Speed [RPM]: {self.max_rpm}'


class EnipServoConveyor(Conveyor):
    def __init__(self, top_length, max_speed, turn_circum, servo_addr):
        super().__init__(top_length, max_speed, turn_circum)
        self.servo = sv2_c.Sv2Servo(servo_addr, self.max_rpm)
        print(f"tpl {self.turns_per_length}")
        self.backwards_one_length = sv2_c.Sv2PointPoint(self.servo, 1, c.CMD_REL, -self.turns_per_length, self.max_rpm)
        self.backwards_one_length.change_property_value("type", 3)
        self.backwards_one_length.update_definition()
        self.forward_constant = sv2_c.Sv2ConstSpeed(self.servo, 2, self.max_rpm, 0)
        self.forward_two_third_length = sv2_c.Sv2PointPoint(self.servo, 3, c.CMD_REL, self.turns_per_length / 3.0 * 2, self.max_rpm)
        self.backwards_one_third_length = sv2_c.Sv2PointPoint(self.servo, 4, c.CMD_REL, -self.turns_per_length / 3.0, self.max_rpm)
        self.go_home = sv2_c.Sv2PointPoint(self.servo, 5, c.CMD_ABS, 0, self.max_rpm)
        self.stop = sv2_c.Sv2ConstSpeed(self.servo, 6, 0)
        self.set_home = self.servo.set_home()
        print(f"rpm: {self.max_rpm}")
        

        

class ModbusVfdConveyor(Conveyor):
    def __init__(self, top_length, max_speed, turn_circum, vfd_addr):
        super().__init__(top_length, max_speed, turn_circum)
        self.vfd = mb_tcp_c(vfd_addr)
