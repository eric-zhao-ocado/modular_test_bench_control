"""
Module for basic control of a SureServo2 drive, through EtherNet/IP
communication.

Functions are designed for use with contolling a conveyor, however
they may not cover all functionality for servo control.

Specific commands not covered by the functions can be sent using the
general purpose send_command function, which can cover all use cases
for the servo (with some difficulty in coding)
"""

import atexit

from cpppo.server.enip import client
from cpppo.server.enip.get_attribute import attribute_operations

import test_bench_constants as tb_const
import sure_servo_2_constants as sv2_const


class BitfieldSec:
    """
    A "bitfield" in this case is a sequence of bits where individual
    "bit sections" of the sequence represent different types of data.
    For example, bits 0-1 may represent "conveyor type", while bits
    2-5 may represent "conveyor length".
    """

    def __init__(self, start_bit, num_bits, value=0, max_value=None):
        """
        Initializes a section of a bitfield.

        Args:
            start_bit: Start index of the section (first bit is 0).
            num_bits: Length of sequence of bits.
            value: The data value to put into the section of bits.
            max_value: The largest value that the section should have.
        """
        self.start_bit = start_bit
        self.num_bits = num_bits
        # Calculate a maximum value from the number of bits available.
        if max_value is None:
            self.max_value = 2 ** num_bits - 1
        else:
            self.max_value = max_value
        if 0 <= value <= self.max_value:
            self.value = value
        else:
            # These checks may need better coding.
            self.value = 0
            print(f"""
                Value out of bounds.\n
                Value: {value}\n
                Max Value: {self.max_value}\n
                """
                )

    def change_value(self, new_value):
        """
        Changes the data value of the bitfield section.

        Args:
            new_value: New value to set the bitfield section to.

        Returns:
            True if successful, False otherwise
        """
        if new_value <= self.max_value:
            self.value = new_value
            return True
        else:
            print(
                f"""
                Value out of bounds.\n
                Value: {new_value}\n
                Max Value: {self.max_value}\n
                """
                )
            return False

    def convert_binary(self):
        """
        Shifts the data according to the specified start bit, such that
        each section maintains its data when combined into a single
        bitfield. Use before combining individual sections to send a
        bitfield in a message.
        """
        return self.value << self.start_bit


class EnipServer:
    """
    A basic class to represent an Ethernet/IP server. Mostly uses cpppo
    to send and receive commands, and can do data type conversion.
    """

    def __init__ (self, ip_addr):
        """
        Initializes an ENIP server given its IP address.

        Args:
            ip_addr: IP address of ENIP server.
        """
        self.ip_addr = ip_addr

    def send_command(
        self, obj_class, instance, attribute, data=None, data_type='(SINT)'
        ):
        """
        Sends specified command using cpppo, given the Common Industrial
        Protocol codes.

        Args:
            obj_class: CIP object class code.
            instance: CIP object instance code.
            attribute: CIP attribute code.
            data: The data to write to the specified attribute.
            data_type: Type of data to be sent. Data is always returned as SINT
                Available types:
                    '(SINT)' (Short Integer, 8-bit).
                    '(INT)' (Integer, 16-bit).
                    '(DINT)' (Double Integer, 32-bit).
                    '(REAL)' (Float, 32-bit).
                    '(BOOL)' (8-bit, bit #0).
                    '(SSTRING)' and '(STRING)' also supported.
        """
        tag = f'@0x{obj_class}/{instance}/{attribute}'
        # Adding the '=' converts the command from a GET to SET command.
        if data is not None:
            tag += f'={data_type}{data}'

        with client.connector(host=self.ip_addr) as conn:
            for _index, descr, _op, _reply, _status, value in conn.synchronous(
                operations=attribute_operations(
                    [tag], route_path=[], send_path='')
                ):
                # Prints command sent.
                print(f": {descr: <20}: {value}")
                # Converts data type to decimal if needed.
                if isinstance(value, list):
                    value = self.data_to_dec(value, '(SINT)')
                return value

    @staticmethod
    def data_to_dec(data_arr, data_type):
        """
        Converts an array of SINTs, INTs, or DINTs to their respective
        decimal values.

        Args:
            data_arr: Data array of specified data type.
            data_type: Type of data
        """
        base = 2 ** sv2_const.CPPPO_DATA_TYPES[data_type]
        total = 0
        for power, val in enumerate(data_arr):
            total += val * (base ** power)
        return total


class Sv2Servo(EnipServer):
    """
    Implements a SureServo2 drive class for use on an ENIP network.
    """

    def __init__(self, ip_addr, max_rpm):
        """
        Initializes the SureServo2 drive.

        Args:
            ip_addr: IP address of servo drive.
            max_rpm: Maximum RPM for the usecase of the drive.
        """
        super().__init__(ip_addr)
        self.max_rpm = max_rpm * 10

    def send_command(
        self, obj_class, instance, attribute, data=None, data_type='(DINT)'
        ):
        """
        Sends specified command using cpppo, given the Common Industrial
        Protocol codes.

        Args:
            obj_class: CIP object class code.
            instance: CIP object instance code.
            attribute: CIP attribute code. Doubled
            data: The data to write to the specified attribute.
            data_type: Type of data to be sent.
                SureServo2 uses DINT (Double Integer):
                    '(DINT)' (32-bit).
        """
        attribute = attribute * 2
        return super().send_command(
            obj_class, instance, attribute, data, data_type,
            )

    def disable_nv_mem_writes(self):
        """
        Disables com writes to non-volatile memory. Should be used
        before any commands are sent, to prevent coms from using up NV
        memory.
        """
        self.send_command(
            sv2_const.SERVO_DATA_OBJ_300,
            sv2_const.EXTENSION_INST_2,
            sv2_const.AUX_FUNC_ATTR_30,
            sv2_const.DISABLE_NV_WRITE
            )

    def read_digital_input(self):
        """
        Returns the digital inputs (may be virtual) to the servo I/O.

        Returns:
            int (decimal) representation of the digital input bitfield.
        """
        return self.send_command(
            sv2_const.SERVO_DATA_OBJ_300,
            sv2_const.DIAGNOSIS_INST_4,
            sv2_const.DIGITAL_INPUT_ATTR
            )

    def enable_servo(self):
        """
        Enables servo control.
        """
        digital_input = self.read_digital_input()
        digital_input |= 1
        self.send_command(
            sv2_const.SERVO_DATA_OBJ_300,
            sv2_const.DIAGNOSIS_INST_4,
            sv2_const.DIGITAL_INPUT_ATTR,
            digital_input
            )

    def disable_servo(self):
        """
        Disables servo control.
        """
        digital_input = self.read_digital_input()
        digital_input &= ~1
        self.send_command(
            sv2_const.SERVO_DATA_OBJ_300,
            sv2_const.DIAGNOSIS_INST_4,
            sv2_const.DIGITAL_INPUT_ATTR,
            digital_input
            )

    def set_home(self):
        """
        Sets the current shaft position as the "home" or to the 0 value
        of absolute positioning.
        """
        # Sets homing method to:
        # "Directly define the current position as the origin".
        self.send_command(
            sv2_const.SERVO_DATA_OBJ_300,
            sv2_const.CONTROL_INST_5,
            sv2_const.HOMING_DEF_ATTR,
            sv2_const.DEFINE_CURR_ORIGIN
            )
        # Triggers homing "path".
        self.send_command(
            sv2_const.SERVO_DATA_OBJ_300,
            sv2_const.CONTROL_INST_5,
            sv2_const.TRIG_POS_ATTR,
            sv2_const.HOMING_ATTR
            )

    def exit_handler(self, decel):
        """
        Starts procedure to stop the servo when program is ended.

        Args:
            decel: Rate of deceleration from servo's rated max speed
        """
        self.send_command(sv2_const.SERVO_DATA_OBJ_300,
                          sv2_const.MONITORING_INST_0,
                          sv2_const.MON_ONE_SELECT_ATTR,)
        exit_path = Sv2ConstSpeed(self, 1, 0)
        # Acceleration is to/from 0rpm to servo's rated max speed, in ms
        # Scales linearly (3s to full speed, 1s to 1/3 rated max speed).
        exit_path.change_acc(decel)
        exit_path.trigger_path()
        speed_monitor = Sv2Monitor(self, 1, sv2_const.MON_SPEED_FEEDBACK_TYPE)
        # Wait until servo is fully stopped, then disable servo.
        while speed_monitor.check_value() != 0:
            pass
        self.disable_servo()


class Sv2Monitor:
    """
    Class for monitoring specified parameters of the servo.
    """
    def __init__(self, servo:Sv2Servo, mon_num, mon_type):
        """
        Initializes the "Select content displayed by status monitoring
        register #".

        Args:
            servo: SureServo2 object
            mon_num: Monitor register number (max value 5)
            mon_type: Type of parameter to be monitored
        """
        self.servo = servo
        self.mon_num = mon_num
        self.mon_type = mon_type
        self.servo.send_command(
            sv2_const.SERVO_DATA_OBJ_300,
            sv2_const.MONITORING_INST_0,
            sv2_const.MON_ONE_SELECT_ATTR + mon_num - 1,
            mon_type
            )

    def check_value(self):
        """
        Checks the value of the parameter being monitored.

        Returns:
            int (decimal) representation of the monitored value.
        """
        return self.servo.send_command(
            sv2_const.SERVO_DATA_OBJ_300,
            sv2_const.MONITORING_INST_0,
            sv2_const.MON_ONE_ATTR + self.mon_num - 1,
            )

    def change_mon_type(self, new_mon_type):
        """
        Changes the type of content being monitored.

        Args:
            new_mon_type: New type of content to be monitored.
        """
        self.servo.send_command(
            sv2_const.SERVO_DATA_OBJ_300,
            sv2_const.MONITORING_INST_0,
            sv2_const.MON_ONE_SELECT_ATTR + self.mon_num - 1,
            new_mon_type
        )


class Sv2Path:
    """
    Class for creating and modifying one "path" or motion of the servo.
    """
    def __init__(self, servo:Sv2Servo, path_num, path_type):
        """
        With this script there can be 16 unique paths, more can be
        added, but they will share the same acceleration values.

        Args:
            servo: SureServo2 object
            path_num: Path index number, also used to index acceleration
            path_type: Path type number
        """
        self.servo = servo
        self.path_num = path_num
        self.bitfield = {
            # First 4 bits define the path type in any path definition.
            "type": BitfieldSec(0, 4, path_type, sv2_const.MAX_TYPE_VALUE)
            }

    def change_property_value(self, prop:str, value):
        """
        Changes the specified property to the specified value
        (in code only).

        Args:
            prop: Name of the property to be changed.
            value: New value to be added.

        Returns:
            bool: True if successful, False if otherwise.

        Examples:
            path_1 = Sv2Path(servo_1, 1, sv2_const.CONST_SPEED_TYPE)
            path_1.change_property_value(
                'type', sv2_const.POINT_POINT_STOP_TYPE
                )
        """
        try:
            return self.bitfield[prop].change_value(value)
        except KeyError:
            print("Invalid property.")
            return False

    def update_definition(self):
        """
        Updates the definition of the path in the servo.
        """
        data = 0
        for item in self.bitfield.values():
            data |= item.convert_binary()
        self.servo.send_command(
            sv2_const.SERVO_DATA_OBJ_300,
            sv2_const.PATH_INST_6,
            # Each path has a definition and data, index is doubled
            self.path_num * 2,
            data
            )

    def change_data(self, data):
        """
        Changes the data field of the path.

        Args:
            data: New data to be written to the data field.
        """
        self.servo.send_command(
            sv2_const.SERVO_DATA_OBJ_300,
            sv2_const.PATH_INST_6,
            # Path data is the path definition index + 1
            self.path_num * 2 + 1,
            data
            )

    def trigger_path(self):
        """
        Triggers the servo to start the path.
        """
        self.servo.send_command(
            sv2_const.SERVO_DATA_OBJ_300,
            sv2_const.CONTROL_INST_5,
            sv2_const.TRIG_POS_ATTR,
            self.path_num
            )


class Sv2MovementPath(Sv2Path):
    """
    Class for movement specific types of paths. Other types of paths
    such as "Jump to specified path" or "Write to Parameters or Data
    Array" are not implemented (and can also be covered in software).
    """
    def __init__(self, servo, path_num, path_type, ins=1):
        """
        Initializes a generic movement path.

        Args:
            servo: SureServo2 object.
            path_num: The path number (max value of 16).
            path_type: Type of movement path.
        """
        super().__init__(servo, path_num, path_type)
        self.bitfield["interrupt"] = BitfieldSec(4, 1, ins)
        # Acceleration and delay indexes start at 0 rather than 1
        self.bitfield["acceleration"] = BitfieldSec(8, 4, path_num - 1)
        self.bitfield["decceleration"] = BitfieldSec(12, 4, path_num - 1)
        self.bitfield["delay"] = BitfieldSec(20, 4, path_num - 1)

    def change_acc(self, new_acc):
        """
        Changes the acceleration value for a movement path. Note that
        this value is stored in a different register, and not in the
        path data or definition.

        Args:
            new_acc: New acceleration value.

        Returns:
            True if acceleration is valid, False otherwise.
        """
        if sv2_const.MIN_ACC <= new_acc <= sv2_const.MAX_ACC:
            self.servo.send_command(
                sv2_const.SERVO_DATA_OBJ_300,
                sv2_const.CONTROL_INST_5,
                sv2_const.ACC_ONE_ATTR + self.path_num - 1,
                new_acc
                )
            return True
        else:
            print("Acceleration out of bounds.")
            return False

    def change_dly(self, servo:Sv2Servo, new_dly):
        """
        Changes the delay value for a movement path. Note that
        this value is stored in a different register, and not in the
        path data or definition.

        Args:
            new_dly: New delay value.

        Returns:
            True if delay is valid, False otherwise.
        """
        if sv2_const.MIN_DLY <= new_dly <= sv2_const.MAX_DLY:
            servo.send_command(
                sv2_const.SERVO_DATA_OBJ_300,
                sv2_const.CONTROL_INST_5,
                sv2_const.DLY_ONE_ATTR + self.path_num - 1,
                new_dly
                )
            return True
        else:
            print("Delay out of bounds.")
            return False


class Sv2ConstSpeed(Sv2MovementPath):
    """
    Constant speed subclass of the Sv2MovementPath. Controls the servo
    to move at a constant speed.
    """
    def __init__(self, servo, path_num, speed=0, ins=1, auto=0, unit=0):
        """
        Initializes a constant speed path.

        Args:
            servo: SureServo2 object.
            path_num: The path number (max value of 16).
            speed: The constant speed, defaults to 0.
            ins: Bool indicating whether the path will interrupt the
                previous path when triggered.
            auto: Bool indicating whether the path will continue to the
                next path when it is finished.
            unit: 0 for unit to be 0.1 rpm, 1 for PPS (PUU per sec).
                NOTE: PPS unit is not implemented, will cause errors
        """
        super().__init__(servo, path_num, sv2_const.CONST_SPEED_TYPE, ins)
        self.bitfield["auto"] = BitfieldSec(5, 1, auto)
        self.bitfield["unit"] = BitfieldSec(6, 1, unit)
        self.update_definition()
        self.change_data(speed)

    def change_speed(self, new_speed):
        """
        Changes the speed data of the constant speed path.

        Args:
            new_speed: New speed (in RPM)
        """
        new_speed = int(new_speed * 10)
        if abs(new_speed) < self.servo.max_rpm:
            self.change_data(new_speed)
            return True
        else:
            print("Too fast.")
            return False


class Sv2PointPoint(Sv2MovementPath):
    """
    Point to point subclass of the Sv2MovementPath. Controls the servo
    to move to a specified position.
    """
    def __init__(
        self, servo, path_num, cmd, proc=False, position=0, speed=0, ins=1,
        ovlp=0
        ):
        """
        Initializes a point to point path.

        Args:
            servo: SureServo2 object.
            path_num: The path number (max value of 16).
            cmd: End of position command.
                - Absolute positions servo from the set home 0 position
                - Relative turns servo from current shaft position
            proc: Bool indicating whether the path will proceed to next
                path when finished.
            position: Specified position data.
            speed: Speed to move to specified position.
            ins: Bool indicating whether the path will interrupt the
                previous path when triggered.
            ovlp: Bool if the path is allowed to overlap the next PR.
        """
        if proc:
            super().__init__(
                servo, path_num, sv2_const.POINT_POINT_PROCEED_TYPE, ins
                )
        else:
            super().__init__(
                servo, path_num, sv2_const.POINT_POINT_STOP_TYPE, ins
                )
        self.bitfield["ovlp"] = BitfieldSec(5, 1, ovlp)
        self.bitfield["cmd"] = BitfieldSec(6, 2, cmd)
        # Speed index is stored here, not the speed value
        self.bitfield["speed"] = BitfieldSec(16, 4, path_num - 1)
        self.update_definition()
        # Make sure to change rotation input into PUU data first.
        self.change_data(position)
        self.change_speed(speed)

    def change_proceed_behaviour(self, proceed:bool):
        """
        Changes whether to proceed to next path after reaching position.

        Args:
            proceed: Bool whether to proceed or not.
        """
        if proceed:
            self.change_property_value(
                "type", sv2_const.POINT_POINT_PROCEED_TYPE
                )
        else:
            self.change_property_value("type", sv2_const.POINT_POINT_STOP_TYPE)
        self.update_definition()

    def change_speed(self, new_speed):
        """
        Changes the maximum speed reached during movement to end point.

        Args:
            new_speed: New speed value in rpm.

        Returns:
            True if speed is valid, False otherwise
        """
        new_speed = int(new_speed * 10)
        if 0 <= new_speed < self.servo.max_rpm:
            self.servo.send_command(
                sv2_const.SERVO_DATA_OBJ_300,
                sv2_const.CONTROL_INST_5,
                sv2_const.SPD_ONE_ATTR + self.path_num - 1,
                new_speed
            )
            return True
        else:
            print("New speed too fast.")
            return False

    def change_position(self, position):
        """
        Changes the end position data.

        Args:
            position: End position data.

        Returns:
            True if position is valid, False otherwise.
        """
        if abs(position) < sv2_const.MAX_PUU:
            self.change_data(position)
            return True
        else:
            print("Position out of bounds.")
            return False

    def change_cmd(self, eop_command):
        """
        Changes the position command (relative, absolute, etc.)

        Args:
            eop_command: Type of end of position command.
        """
        self.change_property_value("cmd", eop_command)
        self.update_definition()

    @staticmethod
    def rotations_to_puu(num_rotations:float):
        """
        Converts an input of rotations to a PUU value.

        Args:
            num_rotations: The number of rotations from specified point.

        Returns:
            integer PUU representation of the rotations input
        """
        return round(num_rotations * sv2_const.E_GEAR_DEN)

if __name__ == "__main__":
    test_servo = Sv2Servo(
        tb_const.SERVO_DRIVE_HOST, sv2_const.DORNER_PRECISION_2200_MAX_RPM
        )
    atexit.register(test_servo.exit_handler, tb_const.SERVO_DRIVE_MAX_RPM)
    test_servo.disable_nv_mem_writes()
    test_servo.enable_servo()

    while True:
        test_position = int(input("Enter rotations: "))
        test_position = Sv2PointPoint.rotations_to_puu(test_position)
        test_speed = int(input("Enter speed: "))

        path_1 = Sv2PointPoint(
            test_servo,
            1,
            sv2_const.CMD_REL,
            position=test_position,
            speed=test_speed
            )
        path_1.trigger_path()
        