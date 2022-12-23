import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from resources.styles import *


"""
Automated gripper testing routine.
"""

import atexit
import multiprocessing as mp
import time
import tkinter
import sys
import csv

from fanucpy import Robot
from resources.import_functions import *

import servo_conveyor
import protos_x_control as px_ctrl
import sure_servo_2_control as sv2_ctrl
import sure_servo_2_constants as sv2_cnst
import yaskawa_vfd_control as vfd_ctrl
import test_bench_constants as tb_cnst


class MainWindow(QWidget):
    def __init__(
        self,
        # conveyor_paths,
        next_stage_event,
        arm_mover,
        paths,
        height,
        coord_sliders,
        jog_conveyor_event,
        compress_gripr_len,
        vel,
        acc,
        min_arm_x,
        max_arm_x,
        reset_parcel_event,
        parcel,
        width,
        length,
        gripr_len,
        gripr_rad,
        *args,
        **kwargs
    ):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Induct Testbench Control  (v1.0.0-alpha)")
        self.setGeometry(0, 0, 1300, 800)
        
        # design 
        title=QFont()
        title.setBold(True)
        title.setPixelSize(16)

    
        unbold=QFont()
        unbold.setBold(False)
        #title.setPixelSize()
        
        # allow only integers
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 180)
        onlyInt.setBottom(0)
        
        tw = QTreeWidget()
        tw.setColumnCount(4)
        tw.setHeaderLabels(["Name", "Waypoint", "Acceleration", "Velocity"])
        tw.setStyleSheet(TREE)
        
        sandbox_tree = QTreeWidget()
        sandbox_tree.setColumnCount(1)
        sandbox_tree.setHeaderLabel("Sandbox")
        sandbox_tree.setStyleSheet(TREE)

        tw_submit = QPushButton("Select")
        tw_submit.setStyleSheet(FORWARD_BUTTON)

        
        drag = DragWidget(orientation=Qt.Orientation.Vertical)

        ROUTINE_MODULES = []
        def refresh_sandbox(button_type):
            nonlocal ROUTINE_MODULES
            
            if button_type == 'submit':
                format_list = []
                for ix in tw.selectedIndexes():
                    text = ix.data(Qt.DisplayRole) # or ix.data()
                    format_list.append(text)
                format_string = format_list[0] + r' ' + format_list[1] + r' ' +  format_list[2] + r' '  + format_list[3]
                ROUTINE_MODULES.append(format_string)
            elif button_type == 'kill':
                ROUTINE_MODULES = []
            elif button_type == 'blowoff':
                ROUTINE_MODULES.append('Blowoff')
            elif button_type == 'pressure':
                ROUTINE_MODULES.append('Vacuum 1')
            elif button_type == 'delay':
                ROUTINE_MODULES.append('Delay 5')
            
            
            for n, l in enumerate(ROUTINE_MODULES):
                item = DragItem(l)
                item.set_data(n)  # Store the data.
                drag.add_item(item)
            
            return ROUTINE_MODULES
            
        
        tw_submit.clicked.connect(lambda: refresh_sandbox('submit'))

        activate_vacuum = QPushButton("Vacuum")
        activate_vacuum.setStyleSheet(BASIC_BUTTON)
        activate_vacuum.clicked.connect(lambda: refresh_sandbox('pressure'))

        deactivate_vacuum = QPushButton("Blow off")
        deactivate_vacuum.setStyleSheet(BASIC_BUTTON)
        deactivate_vacuum.clicked.connect(lambda: refresh_sandbox('blowoff'))

        delay = QPushButton("Delay")
        delay.setStyleSheet(BASIC_BUTTON)
        delay.clicked.connect(lambda: refresh_sandbox('delay'))


        run = QPushButton("Run")
        run.setStyleSheet(FORWARD_BUTTON)
        run_value = QLineEdit()
        run_value.setStyleSheet(LINE_EDIT)

        stop = QPushButton("KILL")
        stop.setStyleSheet(BACKWARD_BUTTON)

        stop.clicked.connect(lambda: refresh_sandbox('kill'))

        # design 
        title=QFont()
        title.setBold(True)
        title.setPixelSize(16)
    
        unbold=QFont()
        unbold.setBold(False)
        #title.setPixelSize()
        
        # allow only integers
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 180)
        onlyInt.setBottom(0)
        
        # Waypoint Bank
        waypoint_tree = QRadioButton("RadioButton 1")

        # Bank Controls
        waypoint_controls = QRadioButton("Import")

        # Dynamic Controls
        dynamic_controls = QGroupBox("Dynamic Controls")
        dynamic_controls.setFont(title)
        dynamic_controls.setEnabled(False)
    
        accel_dial = QDial(self)
        accel_dial.setStyleSheet(DIAL)
        accel_dial.setMinimum(1)
        accel_dial.setMaximum(100)
        accel_dial.setValue(70)
        accel_dial.setNotchesVisible(False)
    
        accel_label = QLabel("acceleration")
        accel_label.setFont(unbold)
        accel_value = QLabel("{}%".format(accel_dial.value()))
        accel_dial.valueChanged.connect(lambda value: accel_value.setText("{}%".format(accel_dial.value())))
        def update_accel(acc, new_acc):
            acc.value = new_acc
        accel_dial.valueChanged.connect(lambda: update_accel(acc, accel_dial.value()))

        velocity_dial = QDial(self)
        velocity_dial.setStyleSheet(DIAL)
        velocity_dial.setMinimum(1)
        velocity_dial.setMaximum(100)
        velocity_dial.setValue(70)
        velocity_dial.setNotchesVisible(False)
    
    
        velocity_label = QLabel("velocity")
        velocity_label.setFont(unbold)
        velocity_value = QLabel("{}%".format(velocity_dial.value()))
        velocity_dial.valueChanged.connect(lambda value: velocity_value.setText("{}%".format(velocity_dial.value())))
        def update_vel(vel, new_vel):
            vel.value = new_vel
        velocity_dial.valueChanged.connect(lambda: update_vel(vel, velocity_dial.value()))
        
        x_slider = QSlider(minimum=0, maximum=360, orientation=Qt.Horizontal)
        y_slider = QSlider(minimum=0, maximum=900, orientation=Qt.Horizontal)
        z_slider = QSlider(minimum=0, maximum=tb_cnst.MAX_Z, orientation=Qt.Horizontal)
        x_label = QLabel("x:")
        y_label = QLabel("y:")
        z_label = QLabel("z:")

        def update_coords(slider, index, value):
            slider[index] = value
        
        x_value = QLabel("{}".format(x_slider.value()))
        x_slider.valueChanged.connect(lambda value: x_value.setText("{}".format(x_slider.value())))
        x_slider.valueChanged.connect(lambda: update_coords(coord_sliders, 0, x_slider.value()))
        x_slider.setStyleSheet(SLIDER)
        x_value.setFont(title)
        x_value.setStyleSheet('color: deeppink')
        y_value = QLabel("{}".format(y_slider.value()))
        y_slider.valueChanged.connect(lambda value: y_value.setText("{}".format(y_slider.value())))
        y_slider.valueChanged.connect(lambda: update_coords(coord_sliders, 1, y_slider.value()))
        y_slider.setStyleSheet(SLIDER)
        y_value.setFont(title)
        y_value.setStyleSheet('color: deeppink')
        z_value = QLabel("{}".format(z_slider.value()))
        z_slider.valueChanged.connect(lambda value: z_value.setText("{}".format(z_slider.value())))
        z_slider.valueChanged.connect(lambda: update_coords(coord_sliders, 2, z_slider.value()))
        z_slider.setStyleSheet(SLIDER)
        z_value.setFont(title)
        z_value.setStyleSheet('color: deeppink')

        submit_name = QLineEdit('waypoint_name')
        submit_name.setStyleSheet(LINE_EDIT)
        submit_start = QPushButton('Source')
        submit_start.setStyleSheet(BASIC_BUTTON)
        def bank_update():
            name = submit_name.text()
            wp = '(' + x_value.text() + ',' + y_value.text() + ',' + z_value.text() + ')'
            accel = str(accel_dial.value())
            velocity = str(velocity_dial.value())
            if accel == '0':
                accel = '50'
            if velocity == '0':
                velocity = '50'

            row = QTreeWidgetItem([name, wp, accel, velocity])
            tw.addTopLevelItem(row)
            
        submit_start.clicked.connect(bank_update)
        ##
        # l1 = QTreeWidgetItem([ "String sldkfjslkdfjsklfjA",  "String B",  "String C" ])
        # l2 = QTreeWidgetItem([ "String AA", "String BB", "String CC" ])
        # tw.addTopLevelItem(l1)
        # tw.addTopLevelItem(l2)


        submit_end = QPushButton('Destination')
        submit_end.setStyleSheet(BASIC_BUTTON)
        verticalSpacer = QSpacerItem(2, 20, QSizePolicy.Minimum)
        micro_verticalSpacer = QSpacerItem(2, 10, QSizePolicy.Minimum)
        horizontalSpacer = QSpacerItem(40, 2, QSizePolicy.Minimum)
        micro_horizontalSpacer = QSpacerItem(15, 2, QSizePolicy.Minimum)
        nano_horizontalSpacer = QSpacerItem(5, 2, QSizePolicy.Minimum)


        # Static Controls
        static_controls = QGroupBox("Static Controls")
        static_controls.setFont(title)
        static_controls.setEnabled(False)

        sc_x_label = QLabel("x:")
        sc_y_label = QLabel("y:")
        sc_z_label = QLabel("z:")

        x_static_label = QLabel("x:")
        y_static_label = QLabel("y:")
        z_static_label = QLabel("z:")

        x_static = QLineEdit('')
        x_static.setStyleSheet(LINE_EDIT)
        x_static.setValidator(onlyInt)
        x_static.setAlignment(Qt.AlignCenter)
        y_static = QLineEdit('')
        y_static.setStyleSheet(LINE_EDIT)
        y_static.setValidator(onlyInt)
        y_static.setAlignment(Qt.AlignCenter)
        z_static = QLineEdit('')
        z_static.setStyleSheet(LINE_EDIT)
        z_static.setValidator(onlyInt)
        z_static.setAlignment(Qt.AlignCenter)

        wp_name_sc = QLineEdit('waypoint name')
        wp_name_sc.setStyleSheet(LINE_EDIT)
    
        submit_start_sc = QPushButton('Source')
        submit_start_sc.setStyleSheet(BASIC_BUTTON)
        submit_end_sc = QPushButton('Destination')
        submit_end_sc.setStyleSheet(BASIC_BUTTON)
        check_joint_limits = QPushButton('Send Waypoint')
        check_joint_limits.setStyleSheet(FORWARD_BUTTON)
        check_joint_limits.setFont(QFont('Arial', 16))
        check_joint_limits.setFont(QFont(unbold))


        sc_x_val = QLabel(str('0'))
        sc_x_val.setFont(title)
        sc_x_val.setStyleSheet('color: deeppink')
        sc_y_val = QLabel(str('0'))
        sc_y_val.setFont(title)
        sc_y_val.setStyleSheet('color: deeppink')
        sc_z_val = QLabel(str('0'))
        sc_z_val.setFont(title)
        sc_z_val.setStyleSheet('color: deeppink')

        def joint_limits():
            x_slider.setValue(int(x_static.text()))
            y_slider.setValue(int(y_static.text()))
            z_slider.setValue(int(z_static.text()))
            sc_x_val.setText("{}".format(x_slider.value()))
            sc_y_val.setText("{}".format(y_slider.value()))
            sc_z_val.setText("{}".format(z_slider.value()))
            x_static.setText(str(x_slider.value()))
            y_static.setText(str(y_slider.value()))
            z_static.setText(str(z_slider.value()))

        check_joint_limits.clicked.connect(joint_limits)

        # Conveyor Controls
        conveyor_controls = QGroupBox("Conveyor Controls")
        conveyor_controls.setFont(title)
        conveyor_controls.setEnabled(False)

        # Calibration
        calibration = QGroupBox("Calibration Settings")
        calibration.setFont(title)

        forward_btn = QPushButton('Forward')
        forward_btn.setStyleSheet(FORWARD_BUTTON)
        # forward_btn.pressed.connect(lambda: jog_servo("Forward", conveyor_paths["jog_path"], 50, jog_conveyor_event))
        # forward_btn.released.connect(lambda: conveyor_paths["fast_stop"].trigger_path())
        
        backward_btn = QPushButton('Backward')
        backward_btn.setStyleSheet(BACKWARD_BUTTON)
        # backward_btn.pressed.connect(lambda: jog_servo("Backward", conveyor_paths["jog_path"], 50, jog_conveyor_event))
        # backward_btn.released.connect(lambda: conveyor_paths["fast_stop"].trigger_path())

        reset_btn = QPushButton('Reset')
        reset_btn.setStyleSheet(BASIC_BUTTON)
        reset_btn.clicked.connect(lambda: reset_parcel_event.set())

        set_btn = QPushButton('Set')
        set_btn.setStyleSheet(BASIC_BUTTON)
        def set_conveyor():
            x_slider.setMaximum(max_arm_x.value)
            x_slider.setMinimum(min_arm_x.value)
            z_slider.setMinimum(tb_cnst.MIN_Z + compress_gripr_len.value + height.value)
            x_slider.setValue((arm_mover[1] + arm_mover[0]) / (2.0 ** 0.5) + tb_cnst.X_OFFSET)
            y_slider.setValue((arm_mover[1] - arm_mover[0]) / (2.0 ** 0.5) + tb_cnst.Y_OFFSET)
            z_slider.setValue(arm_mover[2])
            sc_x_val.setText("{}".format(x_slider.value()))
            sc_y_val.setText("{}".format(y_slider.value()))
            sc_z_val.setText("{}".format(z_slider.value()))
            x_static.setText(str(x_slider.value()))
            y_static.setText(str(y_slider.value()))
            z_static.setText(str(z_slider.value()))
            conveyor_controls.setEnabled(False)
            top_row.setEnabled(True)
            static_controls.setEnabled(True)
            dynamic_controls.setEnabled(True)
            next_stage_event.set()
        set_btn.clicked.connect(lambda: set_conveyor())
        
        configure_btn = QPushButton('Configure')
        configure_btn.setStyleSheet(BASIC_BUTTON)

        def init_complete():
            calibration.setEnabled(False)
            # NOTE COMMENTED OUT FOR OFFLINE
            # next_stage_event.set()
            # next_stage_event.clear()
            # next_stage_event.wait()
            conveyor_controls.setEnabled(True)

        configure_btn.clicked.connect(init_complete)
        
        dimensions_label = QLabel("Item Dimensions (mm)")
        dimensions_label.setFont(unbold)

        width_label = QLabel("w: ")
        width_label.setFont(unbold)
        length_label = QLabel("l:")
        length_label.setFont(unbold)
        height_label = QLabel("h:")
        height_label.setFont(unbold)

        width_entry = QLineEdit('')
        width_entry.setStyleSheet(LINE_EDIT)
        width_entry.setAlignment(Qt.AlignCenter)
        width_entry.setValidator(onlyInt)
        length_entry = QLineEdit('')
        length_entry.setStyleSheet(LINE_EDIT)
        length_entry.setAlignment(Qt.AlignCenter)
        length_entry.setValidator(onlyInt)
        height_entry = QLineEdit('')
        height_entry.setStyleSheet(LINE_EDIT)
        height_entry.setAlignment(Qt.AlignCenter)
        height_entry.setValidator(onlyInt)

        griper_label = QLabel("Gripper Limits (mm) :")

        item_label = QLabel("Item Dimensions (mm) :")
        extended_label = QLabel("Extended: ")
        extended_label.setFont(unbold)
        compressed_label = QLabel("Compressed:")
        compressed_label.setFont(unbold)
        max_width_label = QLabel("Max:")
        max_width_label.setFont(unbold)

        extended_entry = QLineEdit('')
        extended_entry.setStyleSheet(LINE_EDIT)
        extended_entry.setAlignment(Qt.AlignCenter)
        extended_entry.setValidator(onlyInt)
        compressed_entry = QLineEdit('')
        compressed_entry.setStyleSheet(LINE_EDIT)
        compressed_entry.setAlignment(Qt.AlignCenter)
        compressed_entry.setValidator(onlyInt)
        max_width_entry = QLineEdit('')
        max_width_entry.setStyleSheet(LINE_EDIT)
        max_width_entry.setAlignment(Qt.AlignCenter)
        max_width_entry.setValidator(onlyInt)

        box = QRadioButton("Box")
        box.setStyleSheet(SWITCH_BUTTON)
        box.setEnabled(True)
        def box_bag_handler(parcel, box, bag):
            if box.isChecked():
                parcel.value = 0
            elif bag.isChecked():
                parcel.value = 1
        bag = QRadioButton("Bag")
        bag.setStyleSheet(SWITCH_BUTTON)
        box.toggled.connect(lambda: box_bag_handler(parcel, box, bag))

        item_type_label = QLabel("Item Type:")

        list_of_edits = [width_entry, length_entry, height_entry, extended_entry, compressed_entry, max_width_entry]
        
        def edit_text_changed(self):
            for input in list_of_edits:
                if input.text() == '':
                    configure_btn.setEnabled(False)
                    return
                else:
                    configure_btn.setEnabled(True)

        configure_btn.setEnabled(False)
        for input in list_of_edits:
            input.textChanged.connect(edit_text_changed)
        def update_int(num, new_value):
            if new_value != '':
                num.value = int(new_value)
        width_entry.textChanged.connect(lambda: update_int(width, width_entry.text()))
        length_entry.textChanged.connect(lambda: update_int(length, length_entry.text()))
        height_entry.textChanged.connect(lambda: update_int(height, height_entry.text()))
        extended_entry.textChanged.connect(lambda: update_int(gripr_len, extended_entry.text()))
        compressed_entry.textChanged.connect(lambda: update_int(compress_gripr_len, compressed_entry.text()))
        max_width_entry.textChanged.connect(lambda: update_int(gripr_rad, max_width_entry.text()))

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(drag)
        
        

        # Joint Limits
        joint_limits = QGroupBox("Joint Limits")

        # Logo
        placeholder = QSlider(minimum=45, maximum=80, orientation=Qt.Horizontal)
        placeholder.setStyleSheet(SLIDER)

        # layout 
        top_row = QGroupBox("Routine")
        top_row.setFont(title)
        top_row.setEnabled(False)
        
        dials = QHBoxLayout()
        dials.addWidget(accel_dial)
        dials.addItem(micro_horizontalSpacer)
        dials.addWidget(accel_label)
        dials.addWidget(accel_value)
        dials.addWidget(velocity_dial)
        dials.addItem(micro_horizontalSpacer)
        dials.addWidget(velocity_label)
        dials.addWidget(velocity_value)
        

        slider_value_x = QHBoxLayout()
        slider_value_x.addWidget(x_label)
        slider_value_x.addWidget(x_value)

        slider_value_y = QHBoxLayout()
        slider_value_y.addWidget(y_label)
        slider_value_y.addWidget(y_value)

        slider_value_z = QHBoxLayout()
        slider_value_z.addWidget(z_label)
        slider_value_z.addWidget(z_value)


        sliders = QVBoxLayout()
        sliders.addLayout(slider_value_x)
        sliders.addWidget(x_slider)
        sliders.addItem(micro_verticalSpacer)
        sliders.addLayout(slider_value_y)
        sliders.addWidget(y_slider)
        sliders.addItem(micro_verticalSpacer)
        sliders.addLayout(slider_value_z)
        sliders.addWidget(z_slider)
        
        dc_submit = QHBoxLayout()
        dc_submit.addWidget(submit_name, stretch=2)
        dc_submit.addWidget(submit_start, stretch=1)

        dc = QVBoxLayout()
        dc.addLayout(dials)
        dc.addLayout(sliders)
        dc.addItem(verticalSpacer)
        dc.addLayout(dc_submit)
        dynamic_controls.setLayout(dc)

        dynamic_conveyor = QVBoxLayout()
        dynamic_conveyor.addWidget(static_controls)
        dynamic_conveyor.addItem(verticalSpacer)
        dynamic_conveyor.addWidget(dynamic_controls)
    


        # xyz_header = QHBoxLayout()
        # # xyz_header.addItem(horizontalSpacer)
        # xyz_header.addWidget(sc_x_label)
        # xyz_header.addItem(nano_horizontalSpacer)
        # xyz_header.addWidget(sc_x_val)
        # xyz_header.addItem(micro_horizontalSpacer)
        # xyz_header.addWidget(sc_y_label)
        # xyz_header.addItem(nano_horizontalSpacer)
        # xyz_header.addWidget(sc_y_val)
        # xyz_header.addItem(micro_horizontalSpacer)
        # xyz_header.addWidget(sc_z_label)
        # xyz_header.addItem(nano_horizontalSpacer)
        # xyz_header.addWidget(sc_z_val)
        # xyz_header.addItem(horizontalSpacer)

        x_entry = QHBoxLayout()
        x_entry.addWidget(x_static_label)
        x_entry.addWidget(x_static)

        y_entry = QHBoxLayout()
        y_entry.addWidget(y_static_label)
        y_entry.addWidget(y_static)
        

        z_entry = QHBoxLayout()
        z_entry.addWidget(z_static_label)
        z_entry.addWidget(z_static)

        src_dest = QHBoxLayout()
        src_dest.addWidget(submit_start_sc)


        sc_top = QHBoxLayout()
        sc_top.addLayout(x_entry)
        sc_top.addLayout(y_entry)
        sc_top.addLayout(z_entry)
        sc_top.addWidget(check_joint_limits)

        sc = QVBoxLayout()
        sc.addLayout(sc_top)

        static_controls.setLayout(sc)
        

        box_width = QHBoxLayout()
        box_width.addWidget(width_label)
        box_width.addWidget(width_entry)
        box_length = QHBoxLayout()
        box_length.addWidget(length_label)
        box_length.addWidget(length_entry)
        box_height = QHBoxLayout()
        box_height.addWidget(height_label)
        box_height.addWidget(height_entry)

        extended = QHBoxLayout()
        extended.addWidget(extended_label)
        extended.addItem(micro_horizontalSpacer)
        extended.addWidget(extended_entry)
        extended.addWidget(compressed_label)
        extended.addItem(micro_horizontalSpacer)
        extended.addWidget(compressed_entry)
        extended.addWidget(max_width_label)
        extended.addItem(micro_horizontalSpacer)
        extended.addWidget(max_width_entry)
        

        cc_bot = QHBoxLayout()
        cc_bot.addLayout(box_width)
        cc_bot.addItem(micro_horizontalSpacer)
        cc_bot.addLayout(box_length)
        cc_bot.addItem(micro_horizontalSpacer)
        cc_bot.addLayout(box_height)

        item_type = QHBoxLayout()
        item_type.addWidget(box)
        item_type.addWidget(bag)

        cc = QVBoxLayout()
        cc.addItem(micro_verticalSpacer)
        cc.addWidget(griper_label)
        
        cc.addLayout(extended)
        cc.addItem(micro_verticalSpacer)
        cc.addWidget(item_type_label)
        cc.addLayout(item_type)
        cc.addItem(micro_verticalSpacer)
        cc.addItem(micro_verticalSpacer)
        cc.addWidget(item_label)
        cc.addLayout(cc_bot)
        cc.addItem(micro_verticalSpacer)
        cc.addItem(micro_verticalSpacer)
        cc.addItem(micro_verticalSpacer)
        
        cc.addWidget(configure_btn)
    
        calibration.setLayout(cc)

        conveyor = QHBoxLayout()
        conveyor.addWidget(forward_btn)
        conveyor.addWidget(backward_btn)
        conveyor.addWidget(set_btn)
        conveyor.addWidget(reset_btn)
        
        
        conveyor_controls.setLayout(conveyor)

        bank = QVBoxLayout()
        bank.addWidget(tw)
        bank.addWidget(tw_submit)
        # bank.addWidget(tw2)

        sandbox = QVBoxLayout()
        sandbox.addWidget(scroll)


        finite_runs = QHBoxLayout()
        finite_runs.addWidget(run, stretch=2)
        finite_runs.addWidget(run_value, stretch=0)

        bank_controls = QVBoxLayout()
        bank_controls.addWidget(activate_vacuum)
        bank_controls.addWidget(deactivate_vacuum)
        bank_controls.addWidget(delay)
        bank_controls.addLayout(finite_runs)
        bank_controls.addWidget(stop)



        tr = QHBoxLayout()
        tr.addLayout(bank, stretch=3)
        tr.addLayout(sandbox, stretch=3)
        tr.addLayout(bank_controls, stretch=1)
        # tr.addLayout(bank_controls, stretch=1)
        top_row.setLayout(tr)

        static_calibrate = QVBoxLayout()
        static_calibrate.addWidget(calibration)
        static_calibrate.addItem(verticalSpacer)
        static_calibrate.addWidget(conveyor_controls)

        bottom_row = QHBoxLayout()
        bottom_row.addLayout(dynamic_conveyor, stretch=3)
        bottom_row.addItem(micro_horizontalSpacer)
        bottom_row.addLayout(static_calibrate, stretch=2)

        main_layout = QVBoxLayout()
        main_layout.addWidget(top_row)
        main_layout.addItem(verticalSpacer)
        main_layout.addLayout(bottom_row)

        self.setLayout(main_layout)


def exit_routine(
    protos_x: px_ctrl.ProtosX,
    servo: sv2_ctrl.Sv2Servo,
    vfd: vfd_ctrl.YaskawaVfd,
    paths,
    pick_speed_mon,
    quit_event,
):
    """
    Exit routine to stop conveyors and vacuums on exit.

    Args:
        protos_x: ProtosX ModbusTCP client.
        servo: Sv2Servo object for pick conveyor.
        vfd: YaskawaVfd object for place conveyor.
        paths: Conveyor servo path dictionary
        pick_speed_mon: Servo speed monitor
        quit_event: Event to quit all processes.
    """
    quit_event.set()
    print("Exiting...")
    print("Disconnecting from ProtosX...")
    protos_x.exit_handler()
    paths["forwards_one_length"].trigger_path()
    while pick_speed_mon.check_value() != 0:
        pass
    print("Stopping servo...")
    servo.exit_handler()
    print("Stopping vfd...")
    vfd.exit_handler()
    sys.exit(0)

def check_ready():
    """
    Gets the required input and checks if user is ready.
    PLACEHOLDER FUNCTION, for testing purposes only.

    Returns:
        width: Width of box in mm
        height: Height of box in mm
    """
    parcel = int(input("Box or Bag (x/g): "))
    width = int(input("Width (mm): "))
    length = int(input("Length (mm): "))
    height = int(input("Height (mm): "))
    grippr_len = int(input("Gripper length (mm): "))
    compress_gripr_len = int(input("Gripper compressed length (mm): "))
    gripr_rad = int(input("Gripper radius (mm): "))
    while input('Input "Y" to start: ') != 'Y':
        pass
    return parcel, width, length, height, grippr_len, compress_gripr_len, gripr_rad

def jog_servo(
    move_direction: str,
    path: sv2_ctrl.Sv2ConstSpeed,
    speed,
    jog_conveyor_event,
):
    """
    Function for jogging the pick conveyor servo forwards and backwards.

    Args:
        move_direction: String indicating direction of movement.
        path: Sv2ConstSpeed path for constant speed servo control.
        speed: Speed at which to jog the motor at in rpm.
    """
    if jog_conveyor_event.is_set():
        print(f"Starting motor...{move_direction}")
        if move_direction == "Forward":
            path.change_speed(speed)
        else:
            path.change_speed(-speed)
        path.trigger_path()

def save_end_point(
    path: sv2_ctrl.Sv2PointPoint,
    position: int,
    next_stage_event: mp.Event,
):
    """
    Saves the current servo position as the end position for the box.

    Args:
        path: Sv2PointPoint point to point position movement path.
        position: Current position of servo.
        move_arm_event: Event to move onto the next GUI window.
    """
    path.change_position(position)
    next_stage_event.set()

def move_arm(
    quit_event: mp.Event,
    move_arm_event: mp.Event,
    pos: mp.Array,
    vel: mp.Value,
    accel: mp.Value,
    min_y: mp.Value,
):
    """
    Process to move the arm. Monitors the move_arm_event and signals
    the arm to move whenever the event is set.

    Args:
        quit_event: Event to signal the end of the routine.
        move_arm_event: Event to signal the arm to move.
        pos: Position to move arm to.
        vel: Velocity to move arm at.
        accel: Acceleration to move arm at.
    """
    robot = Robot(
        robot_model="Fanuc",
        host=tb_cnst.ROBOT_HOST,
        port=18735,
        ee_DO_type="RDO",
        ee_DO_num=7,
    )
    robot.connect()

    while not quit_event.is_set():
        # Wait for event telling arm to move to be set.
        move_arm_event.wait()
        # Check if the movement command is within the bounds of the testbench.
        if (
            tb_cnst.MIN_X < pos[0] < tb_cnst.MAX_X
            and min_y.value < pos[1] < tb_cnst.MAX_Y
        ):
            try:
                robot.move(
                    "pose",
                    vals=pos,
                    velocity=vel.value,
                    acceleration=accel.value,
                    cnt_val=0,
                    linear=False,
                )
            # Except the generic exception raised "position-is-not-reachable"
            except Exception as exception:
                print(repr(exception))
        # Clear the move arm event.
        move_arm_event.clear()
    print("arm")
    quit_event.set()
    robot.disconnect()
    quit()

def pick_conveyor_init():
    """
    Initializes the servo attached to the pick conveyor.

    Returns:
        pick_conveyor: conveyors.EnipServoConveyor for the servo.
        pick_speed_mon: sv2_ctrl.Sv2Monitor to monitor speed.
        pick_pos_mon: sv2_ctrl.Sv2Monitor to monitor position of servo.
    """
    pick_conveyor = servo_conveyor.EnipServoConveyor(
        top_length=1400,
        max_speed=113000,
        turn_circum=121,
        servo_addr=tb_cnst.SERVO_DRIVE_HOST,
    )
    pick_conveyor.servo.clear_alarms()
    pick_conveyor.servo.enable_servo()

    pick_speed_mon = sv2_ctrl.Sv2Monitor(
        servo=pick_conveyor.servo,
        mon_num=1,
        mon_type=sv2_cnst.MON_SPEED_FEEDBACK_TYPE,
    )
    pick_pos_mon = sv2_ctrl.Sv2Monitor(
        servo=pick_conveyor.servo,
        mon_num=2,
        mon_type=sv2_cnst.MON_POS_FEEDBACK_TYPE,
    )

    pick_conveyor.add_const_speed_path(
        path_name="backwards_constant",
        speed=-5000,
        acc=100,
    )
    pick_conveyor.add_point_point_path(
        path_name="forwards_one_length",
        cmd=sv2_cnst.CMD_REL,
        position=pick_conveyor.puu_per_length,
        speed=500,
        acc=100,
    )
    pick_conveyor.add_point_point_path(
        path_name="forwards_one_length_fast",
        cmd=sv2_cnst.CMD_REL,
        position=pick_conveyor.puu_per_length,
        speed=900,
        acc=100,
    )
    pick_conveyor.add_point_point_path(
        path_name="backwards_one_third_length",
        cmd=sv2_cnst.CMD_REL,
        position=-round(pick_conveyor.puu_per_length / 3),
        speed=900,
        acc=100,
    )
    # Path used to move the parcel a set distance.
    # Specific position to be updated later in the script.
    pick_conveyor.add_point_point_path(
        path_name="forwards_distance",
        cmd=sv2_cnst.CMD_REL,
        position=0,
        speed=100,
        acc=4000,
    )
    pick_conveyor.add_const_speed_path(
        path_name="slow_stop",
        speed=0,
        acc=4000,
    )
    pick_conveyor.add_const_speed_path(
        path_name="fast_stop",
        speed=0,
        acc=100,
    )
    pick_conveyor.add_const_speed_path(
        path_name="jog_path",
        speed=100,
        acc=1000,
    )

    return pick_conveyor, pick_speed_mon, pick_pos_mon

def feed_conveyor_init():
    """
    Initialize the VFD on the feed conveyor.

    Returns:
        Initialized vfd_ctrl.YaskawaVfd object
    """
    feed_conveyor = vfd_ctrl.YaskawaVfd(ip_addr=tb_cnst.VFD_HOST)
    feed_conveyor.change_freq(percentage=100)
    return feed_conveyor

def add_point(paths, arm_mover, vel, acc):
    """
    Adds the current position as a waypoint to the given array.

    Args:
        paths: Array containing waypoints
        arm_mover: Array containing coordinates of arm.
    """
    paths.append(["WAYPOINT", arm_mover[:], vel.value, acc.value])

def add_vacuum(paths, index):
    """
    Adds a vacuum ON point to the array.

    Args:
        paths: Array containing waypoints
        index: Valve index
    """
    paths.append(["VACUUM", index])

def add_blowoff(paths):
    """
    Adds a blowoff point to the array.

    Args:
        paths: Array containing waypoints
    """
    paths.append(["BLOWOFF"])
    
def add_delay(paths, dly_time):
    """
    Adds a delay point to the array.
    
    Args:
        paths: Array containing waypoints
        dly_time: Delay time in seconds
    """
    paths.append(["DELAY", dly_time])

def reset_parcel(
    conveyor_paths: dict,
    protos_x: px_ctrl.ProtosX,
    pick_speed_mon: sv2_ctrl.Sv2Monitor,
):
    """
    Resets the parcel orientation on the pick conveyor.

    Args:
        conveyor_paths: Dictionary containing conveyor paths.
        protos_x: ProtosX object for reading proximity sensors.
        pick_speed_mon: Speed monitor for pick conveyor servo.
    """
    start_time = time.perf_counter()
    conveyor_paths["backwards_constant"].trigger_path()
    counter = 0

    while True:
        # Wait for package to be detected.
        if protos_x.check_prox_sensors():
            conveyor_paths["slow_stop"].trigger_path()
            # Wait for conveyor to stop moving
            while pick_speed_mon.check_value() != 0:
                pass
            return
        # Perform parcel orientation reset every 2 seconds.
        if time.perf_counter()-start_time < 2:
            pass
        elif counter < 1:
            conveyor_paths["forwards_one_length"].trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            conveyor_paths["backwards_constant"].trigger_path()
            counter += 1
            start_time = time.perf_counter()
        else:
            conveyor_paths["forwards_one_length"].trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            conveyor_paths["backwards_one_third_length"].trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            conveyor_paths["forwards_one_length_fast"].trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            conveyor_paths["backwards_constant"].trigger_path()
            start_time = time.perf_counter()

def rotate_45_deg(old_x, old_y):
    """
    Function for rotating and offsetting a coordinate point.

    Args:
        old_x: Original x value.
        old_y: Original y value.

    Returns:
        new_x, new_y: New values after rotation and translation.
    """
    # Rotation matrix to rotate points CW by 45 degrees
    rtn_mtrx = [[2**0.5 / 2, -2**0.5 / 2], [2**0.5 / 2, 2**0.5 / 2]]
    new_x = rtn_mtrx[0][0] * (old_x - tb_cnst.X_OFFSET) \
            + rtn_mtrx[0][1] * (old_y - tb_cnst.Y_OFFSET)
    new_y = rtn_mtrx[1][0] * (old_x - tb_cnst.X_OFFSET) \
            + rtn_mtrx[1][1] * (old_y - tb_cnst.Y_OFFSET)
    return new_x, new_y

def gui_app(
    # conveyor_paths,
    next_stage_event,
    arm_mover,
    paths,
    height,
    coord_sliders,
    jog_conveyor_event,
    compress_gripr_len,
    vel,
    accel,
    min_arm_x,
    max_arm_x,
    reset_parcel_event,
    parcel,
    width,
    length,
    gripr_len,
    gripr_rad,
    quit_event,
):
    """
    Process for running the GUI.
    """
    app = QApplication(sys.argv)  # event loop
    font = QFont('Tahoma')
    app.setFont(font)
    window = MainWindow(
        # conveyor_paths,
        next_stage_event,
        arm_mover,
        paths,
        height,
        coord_sliders,
        jog_conveyor_event,
        compress_gripr_len,
        vel,
        accel,
        min_arm_x,
        max_arm_x,
        reset_parcel_event,
        parcel,
        width,
        length,
        gripr_len,
        gripr_rad,
    )
    window.show()
    code=app.exec_()
    quit_event.set()
    next_stage_event.set()
    sys.exit(code)


def automated_routine():
    """
    Routine for automating the testing of grippers on parcels.
    """
    # Initial initialization
    
    # protos_x = px_ctrl.ProtosX(tb_cnst.PROTOS_X_HOST)
    # pick_conveyor, pick_speed_mon, pick_pos_mon = pick_conveyor_init()
    # conveyor_paths = pick_conveyor.path_dict
    # feed_conveyor = feed_conveyor_init()


    # Initialize events.
    next_stage_event = mp.Event()
    move_arm_event = mp.Event()
    quit_event = mp.Event()
    jog_conveyor_event = mp.Event()
    jog_conveyor_event.set()
    reset_parcel_event = mp.Event()
    
    # Create multiprocessing variables to share between processes.
    arm_mover = mp.Array('d', range(6))
    vel = mp.Value('d', 25)
    accel = mp.Value('d', 1)
    parcel = mp.Value('i', 0)
    width = mp.Value('i', 0)
    length = mp.Value('i', 0)
    height = mp.Value('i', 0)
    gripr_len =mp.Value('i', 0)
    compress_gripr_len = mp.Value('i', 0)
    gripr_rad = mp.Value('i', 0)
    min_arm_x = mp.Value('d', 0)
    max_arm_x = mp.Value('d', 0)
    manager = mp.Manager()
    paths = manager.list()
    coord_sliders = mp.Array('d', range(3))

    # atexit.register(
    #     exit_routine,
    #     protos_x=protos_x,
    #     servo=pick_conveyor.servo,
    #     vfd=feed_conveyor,
    #     paths=conveyor_paths,
    #     pick_speed_mon=pick_speed_mon,
    #     quit_event=quit_event,
    # )
    
    gui_process = mp.Process(
        target=gui_app,
        args=(
            # conveyor_paths,
            next_stage_event,
            arm_mover,
            paths,
            height,
            coord_sliders,
            jog_conveyor_event,
            compress_gripr_len,
            vel,
            accel,
            min_arm_x,
            max_arm_x,
            reset_parcel_event,
            parcel,
            width,
            length,
            gripr_len,
            gripr_rad,
            quit_event,
        )
    )
    gui_process.start()
    # NOTE FOR OFFLINE TESTING ONLY \/\/\/\/
    quit_event.wait()
    sys.exit(0)
    # OFFLINE ONLY ^^
    next_stage_event.wait()

    # NOTE: TESTING PURPOSES ONLY, need dynamic value
    gripr_len.value = 335
    compress_gripr_len.value = 265
    gripr_rad.value = 74

    # Calculate the origin of the gripper
    # Makes sure the gripper doesn't hit the guards
    arm_origin_x = tb_cnst.DEFAULT_X + (gripr_rad.value-5) / (2 ** 0.5)
    arm_origin_y = tb_cnst.DEFAULT_Y + (gripr_rad.value-5) / (2 ** 0.5)

    min_y = mp.Value('d', arm_origin_y - 1)

    # Set default_origin. The last 3 parameters in the list should not be changed.
    default_origin = [
        tb_cnst.DEFAULT_X, tb_cnst.DEFAULT_Y,
        height.value + tb_cnst.MIN_Z + 15 + gripr_len.value, 180.0, 0.0, 0.0
    ]

    # Initialize arm_mover which holds the coordinates to move the arm to.
    arm_mover[0] = arm_origin_x
    arm_mover[1] = arm_origin_y
    for i in range(4):
        arm_mover[i + 2] = default_origin[i + 2]
    # Initialize the arm mover process.
    arm_process = mp.Process(
        target=move_arm,
        args=(quit_event, move_arm_event, arm_mover, vel, accel, min_y)
    )
    arm_process.start()

    if quit_event.is_set():
        sys.exit(0)
    move_arm_event.set()
    
    # Move package and arm to the starting point
    feed_conveyor.start_motor_forwards()
    reset_parcel(conveyor_paths, protos_x, pick_speed_mon)
    feed_conveyor.stop_motor()
    time.sleep(0.2)
    pick_conveyor.set_home()

    # Calculate center of diagonal of box (offset by 96)
    half_diagonal = (width.value ** 2 * 2) ** 0.5 / 2 - 96
    long_diagonal = width.value / (2 ** 0.5) + length.value / (2 ** 0.5)
    # Calculate maximum conveyor position
    max_conveyor_pos = (tb_cnst.MAX_X - default_origin[0]) * (2 ** 0.5) - half_diagonal
    max_grip_conv_pos = max_conveyor_pos - gripr_rad.value + 61
    # Check to ensure box does not hit conveyor guards
    if long_diagonal > 184 and parcel == 0:
        max_conveyor_pos = max_conveyor_pos - (long_diagonal - 183 / 2) / 2 \
            - ((length - width) / (2 ** 0.5)) * 2.6
    # Check to ensure gripper does not hit conveyor guards.
    max_conveyor_pos = min(max_grip_conv_pos, max_conveyor_pos)
    # Calculate PUU position
    max_conveyor_pos = round((max_conveyor_pos / pick_conveyor.turn_circum) * sv2_cnst.E_GEAR_DEN)

    pick_conveyor.add_point_point_path(
        "reset_path",
        sv2_cnst.CMD_ABS,
        max_conveyor_pos-1,
        50,
        4000,
    )
    max_arm_x.value = pick_conveyor.turn_circum * max_conveyor_pos / sv2_cnst.E_GEAR_DEN + half_diagonal
    min_arm_x.value = (arm_origin_x + arm_origin_y) / (2.0 ** 0.5) + tb_cnst.X_OFFSET
    vel.value = 100
    accel.value = 100
    
    min_conveyor_pos = round(sv2_cnst.E_GEAR_DEN * (2 ** 0.5 * (arm_origin_x - default_origin[0])-half_diagonal) / pick_conveyor.turn_circum) + 1000
    pick_conveyor.add_point_point_path(
        "min_location",
        sv2_cnst.CMD_ABS, min_conveyor_pos + 100, 50, 4000)
    next_stage_event.set()
    next_stage_event.clear()
    # Loop to jog the conveyor.
    while not next_stage_event.is_set():
        if quit_event.is_set():
            sys.exit(0)
        # Move arm to current set position
        move_arm_event.set()
        # Get conveyor position
        position = pick_pos_mon.check_value()
        # Calculate distance the box has travelled.
        distance = pick_conveyor.turn_circum * position / sv2_cnst.E_GEAR_DEN

        # Check if conveyor has been jogged too far backwards, and reset if so.
        if reset_parcel_event.is_set():
            reset_parcel(conveyor_paths, protos_x, pick_speed_mon)
            time.sleep(0.2)
            pick_conveyor.set_home()
            reset_parcel_event.clear()
        elif position >= 4000000000 or position < min_conveyor_pos:
            jog_conveyor_event.clear()
            conveyor_paths["min_location"].trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            time.sleep(0.2)
            jog_conveyor_event.set()
        # Check if conveyor position is too far forwards, reset position if so.
        elif 4000000000 >= position >= max_conveyor_pos:
            jog_conveyor_event.clear()
            # conveyor_paths["fast_stop"].trigger_path()
            # position = max_conveyor_pos
            conveyor_paths["reset_path"].trigger_path()
            while pick_speed_mon.check_value() != 0:
                pass
            time.sleep(0.2)
            jog_conveyor_event.set()
        # Move arm to above the center of the diagonal of the box.
        if max_conveyor_pos >= position >= 0:
            arm_mover[0] = default_origin[0] + (distance + half_diagonal) / 2 ** 0.5
            arm_mover[1] = default_origin[1] + (distance + half_diagonal) / 2 ** 0.5
    next_stage_event.clear()
    
    vel.value = 1
    accel.value = 1
    while not next_stage_event.is_set():
        if quit_event.is_set():
            sys.exit(0)
        arm_mover[0], arm_mover[1] = rotate_45_deg(coord_sliders[0], coord_sliders[1])
        arm_mover[2] = coord_sliders[2]
        move_arm_event.set()

    cycles = int(input('Number of cycles: '))
    feed_conveyor.start_motor_forwards()

    # reset data file
    with open('data.csv', "w+", encoding='UTF8', newline='') as file:
        headings = ['Cycle number', 'Time (s)', 'Type', 'Value', 'Velocity (%)', 'Acceleration (%)']
        # create the csv writer
        writer = csv.writer(file)
        writer.writerow(headings)
    start_time = time.perf_counter()
    cycle_num = 1
    while cycle_num <= cycles:
        if quit_event.is_set():
            sys.exit(0)
        # Wait for package to be detected.
        reset_parcel(conveyor_paths, protos_x, pick_speed_mon)
        time.sleep(0.2)
        pick_conveyor.set_home()
        # Move parcel to preset location
        conveyor_paths["forwards_distance"].trigger_path()
        while pick_speed_mon.check_value() != 0:
            pass
        for path in paths[:]:
            # open the file in the write mode
            with open('data.csv', 'a', encoding='UTF8', newline='') as file:
                info = path.copy()
                info.insert(0, time.perf_counter()-start_time)
                info.insert(0, cycle_num)
                # create the csv writer
                writer = csv.writer(file)
                # write a row to the csv file
                writer.writerow(info)
            if path[0] == "VACUUM":
                protos_x.vacuum(path[1])
            elif path[0] == "BLOWOFF":
                protos_x.blowoff()
            elif path[0] == "DELAY":
                time.sleep(path[1])
            elif path[0] == "WAYPOINT":
                for i in range(6):
                    arm_mover[i] = path[1][i]
                    vel.value = path[2]
                    accel.value = path[3]
                move_arm_event.set()
                while move_arm_event.is_set():
                    pass
        cycle_num += 1
    print("Automated routine finished.")
    quit_event.set()
    move_arm_event.set()
    conveyor_paths["forwards_one_length"].trigger_path()
    while pick_speed_mon.check_value() > 0:
        pass



if __name__ == '__main__':
    automated_routine()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)  # event loop
#     font = QFont('Tahoma')
#     app.setFont(font)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
