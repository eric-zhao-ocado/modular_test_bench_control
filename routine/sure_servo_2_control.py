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


class Enip_Server:
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


class SV2_Path:
    def __init__(self, servo:Enip_Server, path_num, type):
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

    def trigger_path(self):
        self.servo.send_command(
            c.SERVO_DATA_OBJ, c.CONTROL_INST, c.TRIG_POS_ATTR, self.path_num)


class SV2_Movement_Path(SV2_Path):
    def __init__(self, type, servo, path_num, ins=1):
        super().__init__(servo, path_num, type)
        self.bitfield["interrupt"] = Bitfield(4, 1, ins)
        self.bitfield["acceleration"] = Bitfield(8, 4, path_num - 1)
        self.bitfield["decceleration"] = Bitfield(12, 4, path_num - 1)
        self.bitfield["delay"] = Bitfield(20, 4, path_num - 1)

    def change_acc(self, servo:Enip_Server, new_acc):
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

    def change_dly(self, servo:Enip_Server, new_dly):
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


class SV2_Const_Speed(SV2_Movement_Path):
    def __init__(self, servo, path_num, ins=1, auto=0, unit=0):
        super().__init__(c.CONST_SPEED_TYPE, servo, path_num, ins)
        self.bitfield["auto"] = Bitfield(5, 1, auto)
        self.bitfield["unit"] = Bitfield(6, 1, unit)
        super().update_definition()

    # SPEED IS 0.1 RPM IN PARAMETERS
    def change_speed(self, new_speed):
        if (abs(new_speed) < c.MAX_RPM):
            self.servo.send_command(
                c.SERVO_DATA_OBJ, 
                c.PATH_INST, 
                c.FIRST_PATH_ATTR + 2 * (self.path_num - 1) + 1,
                new_speed
                )
            return True
        else:
           print("TOO FAST!!!!!!!") 
           return False

# still need to add more methods here.
class SV2_Point_Point(SV2_Movement_Path):
    def __init__(self, servo, path_num, ins=1, ovlp=0, cmd=1):
        super().__init__(c.POINT_POINT_TYPE, servo, path_num, ins)
        self.bitfield["ovlp"] = Bitfield(5, 1, ovlp)
        self.bitfield["cmd"] = Bitfield(6, 2, cmd)
        self.bitfield["speed"] = Bitfield(16, 4, path_num - 1)
        super().update_definition()

    def change_speed(self, new_speed):
        if new_speed < c.MAX_RPM:
            self.servo.send_command(
                c.SERVO_DATA_OBJ,
                c.CONTROL_INST,
                c.FIRST_SPD_ATTR + 2 * (self.path_num - 1),
                new_speed
            )
            return True
        else:
            print("too fast")
            return False
    
    def change_position(self, num_rotations:float):
        print("test")
        print(num_rotations)
        puu = round(num_rotations * c.E_GEAR_DEN)
        print(puu)
        if (abs(puu) < c.MAX_PUU):
            self.servo.send_command(
                c.SERVO_DATA_OBJ,
                c.PATH_INST,
                c.FIRST_PATH_ATTR + 2 * (self.path_num - 1) + 1,
                puu
            )
            return True
        else:
            print("PUU out of limit")
            return False


# Need procedure to stop motors when testing is finished
def exit_handler():
    print("stopping motor")
    servo = Enip_Server("192.168.1.152")
    path_1 = SV2_Const_Speed(servo, 1)
    path_1.change_speed(0)
    path_1.trigger_path()
    servo.send_command(300, 4, 7, 0)


if __name__ == "__main__":
    atexit.register(exit_handler)

    servo = Enip_Server(c.SERVO_DRIVE_HOST)
    servo.send_command(300, 4, 7, 1)
    while True:
        position = float(input("Enter rotations: "))
        speed = int(input("Enter speed: "))
        
        path_1 = SV2_Point_Point(servo, 1)
        if(path_1.change_speed(speed)):
            print("New speed updated.")
            if(path_1.change_position(position)):
                print("Position updated.")
                path_1.trigger_path()
        else:
            print("fail")
            pass
    