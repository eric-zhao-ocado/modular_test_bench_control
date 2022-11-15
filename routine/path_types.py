# Implementing an easier version where each path will have their own acc, dec, etc indexes
from cpppo.server.enip import client
from cpppo.server.enip.get_attribute import attribute_operations
import common_helpers
import constants as c
import atexit

class Enip_Server:
    def __init__ (self, ip_addr):
        self.ip_addr = ip_addr

    def send_command(self, obj_class, instance, attribute, data = None, data_type = '(DINT)'):
        tag = '@0x' + str(obj_class) + '/' + str(instance) + '/' + str(attribute * 2)
        if (data is not None):
            tag += '=' + data_type + str(data)
        with client.connector(host=self.ip_addr) as conn:
            for index, descr, op, reply, status, value in conn.synchronous(
                operations=attribute_operations(
                    [tag], route_path=[], send_path='')):
                print(": %20s: %s" % (descr, value))
                return value
    
    def sint_to_dec(sint_arr):
        sum = 0
        for val_pow, val in enumerate(sint_arr):
            sum += val * (256**val_pow)
        return sum

class Param_Bits:
    def __init__(self, start_bit, num_bits, value):
        self.start_bit = start_bit
        self.num_bits = num_bits
        self.value = value
    
    def change_value(self, new_value):
        if (2 ** self.num_bits - 1 >= new_value):
            self.value = new_value
        else:
            print("Invalid new value.")

    def convert_binary(self):
        return self.value << self.start_bit

class SV2_PATH:
    def __init__(self, path_num, type):
        self.path_num = path_num
        self.bitfield = {"type": Param_Bits(0, 4, type)}

    def change_attr_value(self, attr, value):
        pass
    
    def update_definition(self, servo):
        data = 0
        for item in self.bitfield.values():
            data |= item.convert_binary()
        servo.send_command(c.SERVO_DATA_OBJ, c.PATH_INST, self.path_num * 2, data)

    def trigger_path(self, servo):
        servo.send_command(c.SERVO_DATA_OBJ, c.CONTROL_INST, c.TRIG_POS_CMD, self.path_num)
        

class SV2_Const_Speed(SV2_PATH):
    def __init__(self, servo, path_num, ins=1, auto=0, unit=0):
        super().__init__(path_num, c.CONST_SPEED_TYPE)
        self.bitfield["interrupt"] = Param_Bits(4, 1, ins)
        self.bitfield["auto"] = Param_Bits(5, 1, auto)
        self.bitfield["unit"] = Param_Bits(6, 1, unit)
        self.bitfield["acceleration"] = Param_Bits(8, 4, path_num - 1)
        self.bitfield["decceleration"] = Param_Bits(12, 8, path_num - 1)
        self.bitfield["delay"] = Param_Bits(20, 8, path_num - 1)
        super().update_attributes(servo)

    # SPEED IS 0.1 RPM IN PARAMETERS
    def change_speed(self, servo, new_speed):
        if (abs(new_speed) < 9330):
            servo.send_command(
                c.SERVO_DATA_OBJ, 
                c.PATH_START_INDEX[0], 
                c.PATH_START_INDEX[1] + 2 * (self.path_num - 1) + 1,
                new_speed
                )
            return True
        else:
           print("TOO FAST!!!!!!!") 
           return False

    def change_acc(self, servo, new_acc):
        pass

    def change_dly(self, servo, new_dly):
        pass

# Need procedure to stop motors when testing is finished
def exit_handler():
    print("stopping motor")
    servo = Enip_Server("192.168.1.152")
    path_1 = SV2_Const_Speed(servo, 1)
    path_1.change_speed(servo, 0)
    path_1.trigger_path(servo)
    servo.send_command(300, 4, 7, 0)

atexit.register(exit_handler)

servo = Enip_Server("192.168.1.152")
while True:
    speed = int(input("Enter speed: "))
    
    path_1 = SV2_Const_Speed(servo, 1)
    if(path_1.change_speed(servo, speed)):
        print("New speed updated.")
        path_1.trigger_path(servo)
    else:
        print("fail")
        pass
    
