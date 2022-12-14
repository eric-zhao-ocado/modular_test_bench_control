from pymodbus.client import ModbusTcpClient as mb_tcp_c

import atexit

import test_bench_constants as tb_const
import sure_servo_2_control as sv2_ctrl
import sure_servo_2_constants as sv2_const
import yaskawa_vfd_control as vfd_ctrl

# Conveyor class to represent an individual conveyor
# Ensure that all units are on the same scale (such as mm)
class Conveyor:
    def __init__(self, top_length, max_speed, turn_circum):
        # Top length is the flat length of belt on the conveyor top
        # This can be measured manually or from the CAD models
        self.top_length = top_length
        self.max_rpm = int(max_speed / turn_circum) * 10
        self.turns_per_length = top_length / turn_circum


class EnipServoConveyor(Conveyor):
    def __init__(self, top_length, max_speed, turn_circum, servo_addr):
        super().__init__(top_length, max_speed, turn_circum)
        self.servo = sv2_ctrl.Sv2Servo(servo_addr, self.max_rpm)
        print(f"tpl {self.turns_per_length}")
        self.turns_per_length = sv2_ctrl.Sv2PointPoint.rotations_to_puu(self.turns_per_length)
        print(self.turns_per_length)
        
        self.backwards_one_length = sv2_ctrl.Sv2PointPoint(
            self.servo, 1, sv2_const.CMD_REL, -self.turns_per_length,
            self.max_rpm)
        self.backwards_one_length.change_acc(100)
        self.backwards_one_length.change_speed(500)

        self.backwards_constant = sv2_ctrl.Sv2ConstSpeed(
            self.servo, 2, -8000, 0)
        self.backwards_constant.change_acc(100)

        self.backwards_two_third_length = sv2_ctrl.Sv2PointPoint(
            self.servo, 3, sv2_const.CMD_REL, -round(self.turns_per_length / 3.0 * 2), self.max_rpm)
        self.backwards_two_third_length.change_acc(100)
        self.backwards_two_third_length.change_speed(500)
        
        self.forwards_one_third_length = sv2_ctrl.Sv2PointPoint(
            self.servo, 4, sv2_const.CMD_REL, round(self.turns_per_length / 3.0), self.max_rpm)
        self.forwards_one_third_length.change_acc(100)
        self.forwards_one_third_length.change_speed(500)
        
        self.forwards_one_length = sv2_ctrl.Sv2PointPoint(
            self.servo, 4, sv2_const.CMD_REL, round(self.turns_per_length), self.max_rpm)
        self.forwards_one_third_length.change_acc(100)
        self.forwards_one_third_length.change_speed(500)
        
        self.forwards_distance = sv2_ctrl.Sv2PointPoint(
            self.servo, 5, sv2_const.CMD_REL, round(sv2_ctrl.Sv2PointPoint.rotations_to_puu(1)), self.max_rpm)
        self.forwards_distance.change_acc(500)
        self.forwards_distance.change_speed(100)
        
        self.go_home = sv2_ctrl.Sv2PointPoint(
            self.servo, 6, sv2_const.CMD_ABS, 0, self.max_rpm)
        self.go_home.change_acc(100)
        self.go_home.change_speed(500)

        self.stop = sv2_ctrl.Sv2ConstSpeed(self.servo, 7, 0)

        self.set_home = self.servo.set_home

if __name__ == '__main__':
    pick_conveyor = EnipServoConveyor(1400, 113000, 121, '192.168.1.10')
    feed_conveyor = vfd_ctrl.YaskawaVfd('192.168.1.20')
    atexit.register(pick_conveyor.servo.exit_handler)
    pick_conveyor.servo.enable_servo()
    pick_conveyor.servo.clear_alarms()
    while True:
        command = int(input("Command number: "))
        if command == 1:
            pick_conveyor.backwards_one_length.trigger_path()
        elif command == 2:
            pick_conveyor.backwards_constant.trigger_path()
        elif command == 3:
            pick_conveyor.backwards_two_third_length.trigger_path()
        elif command == 4:
            pick_conveyor.forwards_one_third_length.trigger_path()
        elif command == 5:
            pick_conveyor.go_home.trigger_path()
        elif command == 6:
            pick_conveyor.set_home()
        else:
            pass
