import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from resources.styles import *
class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Induct Testbench Control  (v1.0.0-alpha)")
        self.setGeometry(0, 0, 1500, 800)
        

        ### TEST ###
        l1 = QTreeWidgetItem([ "String A",  "String B",  "String C" ])
        l2 = QTreeWidgetItem([ "String AA", "String BB", "String CC" ])


        for i in range(3):
            l1_child = QTreeWidgetItem(["Child A" + str(i), "Child B" + str(i), "Child C" + str(i)])
            l1.addChild(l1_child)

        for j in range(2):
            l2_child = QTreeWidgetItem(["Child AA" + str(j), "Child BB" + str(j), "Child CC" + str(j)])
            l2.addChild(l2_child)

        tw = QTreeWidget()
        tw.resize(500,200)
        tw.setColumnCount(3)
        tw.setHeaderLabels(["Column 1", "Column 2", "Column 3"])
        tw.addTopLevelItem(l1)
        tw.addTopLevelItem(l2)
        tw.setStyleSheet(TREE)
        ### TEST ###


        # sliders

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
        accel_dial.setMinimum(0)
        accel_dial.setMaximum(100)
        accel_dial.setValue(0)
        accel_dial.setNotchesVisible(False)
    
        accel_label = QLabel("acceleration")
        accel_label.setFont(unbold)
        accel_value = QLabel("{}%".format(accel_dial.value()))
        accel_dial.valueChanged.connect(lambda value: accel_value.setText("{}%".format(accel_dial.value())))

        velocity_dial = QDial(self)
        velocity_dial.setStyleSheet(DIAL)
        velocity_dial.setMinimum(0)
        velocity_dial.setMaximum(100)
        velocity_dial.setValue(0)
        velocity_dial.setNotchesVisible(False)
    
    
        velocity_label = QLabel("velocity")
        velocity_label.setFont(unbold)
        velocity_value = QLabel("{}%".format(velocity_dial.value()))
        velocity_dial.valueChanged.connect(lambda value: velocity_value.setText("{}%".format(velocity_dial.value())))
        
        x_slider = QSlider(minimum=0, maximum=360, orientation=Qt.Horizontal)
        y_slider = QSlider(minimum=0, maximum=360, orientation=Qt.Horizontal)
        z_slider = QSlider(minimum=0, maximum=360, orientation=Qt.Horizontal)
        x_label = QLabel("x:")
        y_label = QLabel("y:")
        z_label = QLabel("z:")

        x_value = QLabel("{}".format(x_slider.value()))
        x_slider.valueChanged.connect(lambda value: x_value.setText("{}".format(x_slider.value())))
        x_slider.setStyleSheet(SLIDER)
        x_value.setFont(title)
        x_value.setStyleSheet('color: deeppink')
        y_value = QLabel("{}".format(y_slider.value()))
        y_slider.valueChanged.connect(lambda value: y_value.setText("{}".format(y_slider.value())))
        y_slider.setStyleSheet(SLIDER)
        y_value.setFont(title)
        y_value.setStyleSheet('color: deeppink')
        z_value = QLabel("{}".format(z_slider.value()))
        z_slider.valueChanged.connect(lambda value: z_value.setText("{}".format(z_slider.value())))
        z_slider.setStyleSheet(SLIDER)
        z_value.setFont(title)
        z_value.setStyleSheet('color: deeppink')

        submit_name = QLineEdit('waypoint name')
        submit_name.setStyleSheet(LINE_EDIT)
        submit_start = QPushButton('Source')
        submit_start.setStyleSheet(BASIC_BUTTON)
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
        
        backward_btn = QPushButton('Backward')
        backward_btn.setStyleSheet(BACKWARD_BUTTON)

        reset_btn = QPushButton('Reset')
        reset_btn.setStyleSheet(BASIC_BUTTON)

        set_btn = QPushButton('Set')
        set_btn.setStyleSheet(BASIC_BUTTON)
    
        configure_btn = QPushButton('Configure')
        configure_btn.setStyleSheet(BASIC_BUTTON)

        def init_complete():
            conveyor_controls.setEnabled(True)
            top_row.setEnabled(True)
            static_controls.setEnabled(True)
            dynamic_controls.setEnabled(True)
            calibration.setEnabled(False)

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
        item_label = QLabel("Item dimensions (mm) :")
        extended_label = QLabel("Extended Length: ")
        extended_label.setFont(unbold)
        compressed_label = QLabel("Compressed Length")
        compressed_label.setFont(unbold)
        max_width_label = QLabel("Max Width:")
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
        compressed = QHBoxLayout()
        
        compressed.addWidget(compressed_label)
        compressed.addItem(micro_horizontalSpacer)
        compressed.addWidget(compressed_entry)
        max_width = QHBoxLayout()
       
        max_width.addWidget(max_width_label)
        max_width.addItem(micro_horizontalSpacer)
        max_width.addWidget(max_width_entry)

        cc_bot = QHBoxLayout()
        cc_bot.addLayout(box_width)
        cc_bot.addItem(micro_horizontalSpacer)
        cc_bot.addLayout(box_length)
        cc_bot.addItem(micro_horizontalSpacer)
        cc_bot.addLayout(box_height)

        cc = QVBoxLayout()
        cc.addItem(micro_verticalSpacer)
        cc.addWidget(griper_label)
        cc.addItem(micro_verticalSpacer)
        cc.addLayout(extended)
        cc.addLayout(compressed)
        cc.addLayout(max_width)
        cc.addItem(micro_verticalSpacer)
        cc.addItem(micro_verticalSpacer)
        cc.addWidget(item_label)
        cc.addItem(micro_verticalSpacer)
        cc.addLayout(cc_bot)
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

        bank = QHBoxLayout()
        bank.addWidget(tw)

        bank_controls = QVBoxLayout()
        bank_controls.addWidget(waypoint_controls)


        tr = QHBoxLayout()
        tr.addLayout(bank, stretch=2)
        tr.addLayout(bank_controls, stretch=1)
        top_row.setLayout(tr)

        static_calibrate = QVBoxLayout()
        static_calibrate.addWidget(calibration)
        static_calibrate.addItem(verticalSpacer)
        static_calibrate.addWidget(conveyor_controls)

        bottom_row = QHBoxLayout()
        bottom_row.addLayout(dynamic_conveyor, stretch=3)
        bottom_row.addItem(micro_horizontalSpacer)
        bottom_row.addLayout(static_calibrate, stretch=2)
        

        lhs = QVBoxLayout()
        lhs.addWidget(top_row)
        lhs.addItem(verticalSpacer)
        lhs.addLayout(bottom_row)

        rhs = QVBoxLayout()
        rhs.addWidget(placeholder)
        rhs.addWidget(placeholder)

        main_layout = QHBoxLayout()
        main_layout.addLayout(lhs, stretch=2)
        main_layout.addLayout(rhs, stretch=1)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # event loop
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
