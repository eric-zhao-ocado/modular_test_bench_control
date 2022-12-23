"""
Module for controlling a conveyor using a SureServo2 servo drive.
"""

import sure_servo_2_control as sv2_ctrl

class EnipServoConveyor():
    """
    Basic conveyor class for the characteristics of a servo conveyor.
    """

    def __init__(self, top_length, max_speed, turn_circum, servo_addr):
        """
        Initializes the conveyor. All units should be consistent (such as mm)

        Args:
            top_length: Length of the top surface of the conveyor.
            max_speed: Maximum speed of conveyor.
            turn_circum: Outer circumferance of the conveyor pulley drum.
            servo_addr: IP address of servo motor.
        """
        self.max_rpm = int(max_speed / turn_circum) * 10
        turns_per_length = top_length / turn_circum
        self.turn_circum = turn_circum
        self.servo = sv2_ctrl.Sv2Servo(servo_addr, self.max_rpm)
        self.puu_per_length = round(sv2_ctrl.Sv2PointPoint.rotations_to_puu(turns_per_length))

        self.path_dict = {}
        # Maximum 16 unique paths.
        self.available_paths = set(range(1,17))

        self.set_home = self.servo.set_home

    def add_point_point_path(self, path_name, cmd, position, speed, acc):
        """
        Add a point to point path to the path dictionary.

        Args:
            path_name: Name of the path to be called with.
            cmd: Type of point to point command.
            position: Puu value to move to.
            speed: Speed to move at (rpm).
            acc: Acceleration time to move to maximum servo speed (ms).

        Returns:
            bool: True if path added successfully, false if paths are full.
        """
        try:
            path_num = self.available_paths.pop()
        except KeyError:
            return False
        self.path_dict[path_name] = sv2_ctrl.Sv2PointPoint(
            servo=self.servo,
            path_num=path_num,
            cmd=cmd,
            position=position,
            speed=speed,
            acc=acc,
        )
        return True

    def add_const_speed_path(self, path_name, speed, acc):
        """
        Add a constant speed path to the path dictionary.

        Args:
            path_name: Name of the path to be called with.
            speed: Speed to move at (rpm).
            acc: Acceleration time to move to maximum servo speed (ms).

        Returns:
            bool: True if path added successfully, false if paths are full.
        """
        try:
            path_num = self.available_paths.pop()
        except KeyError:
            return False
        self.path_dict[path_name] = sv2_ctrl.Sv2ConstSpeed(
            self.servo, path_num, speed, acc
        )
        return True

    def remove_path(self, path_name):
        """
        Remove a path from the path dictionary and add its path number
        back into the path num set.

        Args:
            path_name: Name of path to be removed.

        Returns:
            bool: True if removed successfully, False otherwise.
        """
        try:
            path_num = self.path_dict.pop(path_name).path_num
            self.available_paths.add(path_num)
        except KeyError:
            return False
        return True
