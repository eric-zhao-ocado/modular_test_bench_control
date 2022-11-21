import atexit

from cpppo.server.enip import client
from cpppo.server.enip.get_attribute import attribute_operations

import common_helpers
import constants as c


class Bitfield:
    def __init__(self, start_bit, num_bits, value=0, max_value=None):
        self.start_bit = start_bit
        self.num_bits = num_bits
        if max_value is None:
            self.max_value = 2 ** num_bits - 1
        else:
            self.max_value = max_value
        if value <= self.max_value:
            self.value = value
        else:
            print("Invalid initial value.")
    
    def change_value(self, new_value):
        if new_value <= self.max_value:
            self.value = new_value
        else:
            print("Invalid new value.")

    def convert_binary(self):
        return self.value << self.start_bit


class EnipServer:
    def __init__ (self, ip_addr):
        self.ip_addr = ip_addr

    def send_command(self, obj_class, instance, attribute, data = None, data_type = '(DINT)'):
        tag = f'@0x{obj_class}/{instance}/{attribute*2}'
        if (data is not None):
            tag += f'={data_type}{data}'
        with client.connector(host=self.ip_addr) as conn:
            for index, descr, op, reply, status, value in conn.synchronous(
                operations=attribute_operations(
                    [tag], route_path=[], send_path='')):
                print(": %20s: %s" % (descr, value))
                return value
    
    def sint_to_dec(sint_arr):
        sum = 0
        for val_pow, val in enumerate(sint_arr):
            sum += val * (256 ** val_pow)
        return sum
        
        
class Sv2Servo(EnipServer):
    def __init__(self, ip_addr, max_rpm):
        super().__init__(ip_addr)
        self.max_rpm = max_rpm * 10
    
    # Defines home (0 position) as the current shaft position
    def set_home(self):
        # Sets homing method to:
        # Directly define the current position as the origin
        self.send_command(
            c.SERVO_DATA_OBJ,
            c.CONTROL_INST, 
            c.HOMING_DEF_ATTR, 
            c.DEFINE_CURR_ORIGIN
            )
        # Triggers homing path
        self.send_command(
            c.SERVO_DATA_OBJ,
            c.CONTROL_INST, 
            c.TRIG_POS_ATTR, 
            c.HOMING_ATTR
            )

class Sv2Path:
    def __init__(self, servo:Sv2Servo, path_num, type):
        self.servo = servo
        self.path_num = path_num
        self.bitfield = {"type": Bitfield(0, 4, type, c.MAX_TYPE_VALUE)}

    def change_property_value(self, prop:str, value):
        try:
            return self.bitfield[prop].change_value(value)
        except KeyError:
            print("Invalid property.")
            return False
    
    def update_definition(self):
        data = 0
        for item in self.bitfield.values():
            data |= item.convert_binary()
        self.servo.send_command(c.SERVO_DATA_OBJ, c.PATH_INST, self.path_num * 2, data)

    def change_data(self, data):
        self.servo.send_command(c.SERVO_DATA_OBJ, c.PATH_INST, self.path_num * 2 + 1, data)

    def trigger_path(self):
        self.servo.send_command(
            c.SERVO_DATA_OBJ, c.CONTROL_INST, c.TRIG_POS_ATTR, self.path_num)


class Sv2MovementPath(Sv2Path):
    def __init__(self, type, servo, path_num, ins=1):
        super().__init__(servo, path_num, type)
        self.bitfield["interrupt"] = Bitfield(4, 1, ins)
        self.bitfield["acceleration"] = Bitfield(8, 4, path_num - 1)
        self.bitfield["decceleration"] = Bitfield(12, 4, path_num - 1)
        self.bitfield["delay"] = Bitfield(20, 4, path_num - 1)

    def change_acc(self, servo:Sv2Servo, new_acc):
        if (c.MIN_ACC <= new_acc and new_acc <= c.MAX_ACC):
            servo.send_command(
                c.SERVO_DATA_OBJ,
                c.CONTROL_INST,
                c.FIRST_ACC_ATTR + self.path_num - 1,
                new_acc
                )
            return True
        else:
            print("Acceleration out of bounds.")
            return False

    def change_dly(self, servo:Sv2Servo, new_dly):
        if (c.MIN_DLY <= new_dly and new_dly <= c.MAX_DLY):
            servo.send_command(
                c.SERVO_DATA_OBJ,
                c.CONTROL_INST,
                c.FIRST_DLY_ATTR + self.path_num - 1,
                new_dly
                )
            return True
        else:
            print("Delay out of bounds.")
            return False


class Sv2ConstSpeed(Sv2MovementPath):
    def __init__(self, servo, path_num, speed=0, ins=1, auto=0, unit=0):
        super().__init__(c.CONST_SPEED_TYPE, servo, path_num, ins)
        self.bitfield["auto"] = Bitfield(5, 1, auto)
        self.bitfield["unit"] = Bitfield(6, 1, unit)
        super().update_definition()
        self.change_data(speed)

    # SPEED IS 0.1 RPM IN PARAMETERS
    def change_speed(self, new_speed):
        if (abs(new_speed) < self.servo.max_rpm):
            self.change_data(new_speed)
            return True
        else:
           print("TOO FAST!!!!!!!") 
           return False


class Sv2PointPoint(Sv2MovementPath):
    def __init__(self, servo, path_num, cmd, position=0, speed=0, ins=1, ovlp=0):
        super().__init__(c.POINT_POINT_TYPE, servo, path_num, ins)
        self.bitfield["ovlp"] = Bitfield(5, 1, ovlp)
        self.bitfield["cmd"] = Bitfield(6, 2, cmd)
        self.bitfield["speed"] = Bitfield(16, 4, path_num - 1)
        super().update_definition()
        if (cmd == c.CMD_REL):
            position = self.rotations_to_puu(position)
        print(position)
        print(speed)
        self.change_data(position)
        self.change_speed(speed)

    def change_speed(self, new_speed):
        if 0 <= new_speed and new_speed < self.servo.max_rpm:
            self.servo.send_command(
                c.SERVO_DATA_OBJ,
                c.CONTROL_INST,
                c.FIRST_SPD_ATTR + self.path_num - 1,
                new_speed
            )
            return True
        else:
            print("too fast")
            return False

    def rotations_to_puu(self, num_rotations:float):
        return round(num_rotations * c.E_GEAR_DEN)
    
    def change_position(self, position:float, cmd):
        if (cmd == c.CMD_REL):
            # Defines end position as number of turns relative to current position
            puu = self.rotations_to_puu(position)
        else:
            # Defines the end position relative to the home position at 0
            puu = position
        if (abs(puu) < c.MAX_PUU):
            self.change_cmd(c.CMD_REL)
            self.change_data(puu)
            return True
        else:
            print("PUU out of limit")
            return False
    
    
    # Changes the position command (relative, absolute, etc.)
    def change_cmd(self, eop_command):
        self.change_property_value("cmd", eop_command)
        self.update_definition()


# Need procedure to stop motors when testing is finished
def exit_handler():
    print("stopping motor")
    servo = Sv2Servo("192.168.1.152", c.DORNER_PRECISION_2200_MAX_RPM)
    path_1 = Sv2ConstSpeed(servo, 1, 9330)
    path_1.change_speed(0)
    path_1.trigger_path()
    servo.send_command(300, 4, 7, 0)


if __name__ == "__main__":
    atexit.register(exit_handler)

    servo = Sv2Servo(c.SERVO_DRIVE_HOST, c.DORNER_PRECISION_2200_MAX_RPM)
    servo.send_command(300, 4, 7, 1)
    while True:
        position = int(input("Enter rotations: "))
        speed = int(input("Enter speed: "))
        
        path_1 = Sv2PointPoint(servo, 1, c.CMD_ABS, position, speed)
        path_1.trigger_path()
    