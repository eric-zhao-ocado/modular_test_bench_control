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
    
        accel_dial = QDial(self)
        accel_dial.setStyleSheet(DIAL)
        accel_dial.setMinimum(0)
        accel_dial.setMaximum(100)
        accel_dial.setValue(0)
        accel_dial.setNotchesVisible(True)
    
        accel_label = QLabel("acceleration")
        accel_label.setFont(unbold)
        accel_value = QLabel("{}%".format(accel_dial.value()))
        accel_dial.valueChanged.connect(lambda value: accel_value.setText("{}%".format(accel_dial.value())))

        velocity_dial = QDial(self)
        velocity_dial.setStyleSheet(DIAL)
        velocity_dial.setMinimum(0)
        velocity_dial.setMaximum(100)
        velocity_dial.setValue(0)
        velocity_dial.setNotchesVisible(True)
    
    
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
        submit_name.setStyleSheet('color: darkgray')
        submit_name.setFont(unbold)
        submit_name.setAlignment(Qt.AlignCenter)
        submit_name.setFont(QFont('Arial', 15))
        submit_start = QPushButton('Source')
        submit_end = QPushButton('Destination')
        verticalSpacer = QSpacerItem(2, 20, QSizePolicy.Minimum)
        micro_verticalSpacer = QSpacerItem(2, 10, QSizePolicy.Minimum)
        horizontalSpacer = QSpacerItem(40, 2, QSizePolicy.Minimum)
        micro_horizontalSpacer = QSpacerItem(15, 2, QSizePolicy.Minimum)


        # Static Controls
        static_controls = QGroupBox("Static Controls")
        static_controls.setFont(title)

        sc_x_label = QLabel("x:")
        sc_y_label = QLabel("y:")
        sc_z_label = QLabel("z:")

        x_static_label = QLabel("x:")
        y_static_label = QLabel("y:")
        z_static_label = QLabel("z:")

        x_static = QLineEdit('')
        x_static.setFont(unbold)
        x_static.setStyleSheet('color: darkgray')
        x_static.setAlignment(Qt.AlignCenter)
        x_static.setValidator(onlyInt)
        x_static.setFont(QFont('Arial', 15))
        y_static = QLineEdit('')
        y_static.setFont(unbold)
        y_static.setStyleSheet('color: darkgray')
        y_static.setAlignment(Qt.AlignCenter)
        y_static.setValidator(onlyInt)
        y_static.setFont(QFont('Arial', 15))
        z_static = QLineEdit('')
        z_static.setFont(unbold)
        z_static.setStyleSheet('color: darkgray')
        z_static.setAlignment(Qt.AlignCenter)
        z_static.setValidator(onlyInt)
        z_static.setFont(QFont('Arial', 15))

        wp_name_sc = QLineEdit('waypoint name')
        wp_name_sc.setAlignment(Qt.AlignCenter)
        wp_name_sc.setStyleSheet('color: darkgray')
        wp_name_sc.setFont(unbold)
        wp_name_sc.setFont(QFont('Arial', 15))
    
        submit_start_sc = QPushButton('Source')
        # submit_start_sc.setFont(QFont(unbold))
        submit_end_sc = QPushButton('Destination')
        # submit_end_sc.setFont(QFont(unbold))
        check_joint_limits = QPushButton('Check Joint Limits')
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
            sc_x_val.setText("{}".format(x_static.text()))
            sc_y_val.setText("{}".format(y_static.text()))
            sc_z_val.setText("{}".format(z_static.text()))
            x_slider.setValue(int(x_static.text()))
            y_slider.setValue(int(y_static.text()))
            z_slider.setValue(int(z_static.text()))

        check_joint_limits.clicked.connect(joint_limits)


        # Conveyor Controls
        conveyor_controls = QGroupBox("Conveyor Controls")
        conveyor_controls.setFont(title)

        forward_btn = QPushButton('Forward')
        forward_btn.setStyleSheet(FORWARD_BUTTON)
        # forward_btn.setFont(unbold)
        
        backward_btn = QPushButton('Backward')
        backward_btn.setStyleSheet(BACKWARD_BUTTON)
        # backward_btn.setFont(unbold)
        set_btn = QPushButton('Set Position')
        set_btn.setStyleSheet(BASIC_BUTTON)

        # set_btn.setFont(unbold)

        dimensions_label = QLabel("Item Dimensions (cm)")
        dimensions_label.setFont(unbold)

        width_label = QLabel("width :")
        length_label = QLabel("length :")
        height_label = QLabel("height :")

        width_entry = QLineEdit('')
        width_entry.setFont(unbold)
        width_entry.setStyleSheet('color: darkgray')
        width_entry.setAlignment(Qt.AlignCenter)
        width_entry.setValidator(onlyInt)
        width_entry.setFont(QFont('Arial', 15))
        length_entry = QLineEdit('')
        length_entry.setFont(unbold)
        length_entry.setStyleSheet('color: darkgray')
        length_entry.setFont(QFont('Arial', 15))
        length_entry.setAlignment(Qt.AlignCenter)
        length_entry.setValidator(onlyInt)
        height_entry = QLineEdit('')
        height_entry.setFont(unbold)
        height_entry.setStyleSheet('color: darkgray')
        height_entry.setFont(QFont('Arial', 15))
        height_entry.setAlignment(Qt.AlignCenter)
        height_entry.setValidator(onlyInt)

      


        # Joint Limits
        joint_limits = QGroupBox("Joint Limits")

        # Logo
        placeholder = QSlider(minimum=45, maximum=80, orientation=Qt.Horizontal)
        placeholder.setStyleSheet(SLIDER)



        # layout 
        top_row = QGroupBox("Routine")
        top_row.setFont(title)
        
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
        dc_submit.addWidget(submit_end, stretch=1)

        dc = QVBoxLayout()
        dc.addLayout(dials)
        dc.addLayout(sliders)
        dc.addItem(verticalSpacer)
        dc.addLayout(dc_submit)
        dynamic_controls.setLayout(dc)


        xyz_header = QHBoxLayout()
        xyz_header.addWidget(sc_x_label)
        xyz_header.addWidget(sc_x_val)
        xyz_header.addWidget(sc_y_label)
        xyz_header.addWidget(sc_y_val)
        xyz_header.addWidget(sc_z_label)
        xyz_header.addWidget(sc_z_val)

        x_entry = QHBoxLayout()
        x_entry.addWidget(x_static_label)
        x_entry.addItem(micro_horizontalSpacer)
        x_entry.addWidget(x_static)

        y_entry = QHBoxLayout()
        y_entry.addWidget(y_static_label)
        y_entry.addItem(micro_horizontalSpacer)
        y_entry.addWidget(y_static)

        z_entry = QHBoxLayout()
        z_entry.addWidget(z_static_label)
        z_entry.addItem(micro_horizontalSpacer)
        z_entry.addWidget(z_static)

        src_dest = QHBoxLayout()
        src_dest.addWidget(submit_start_sc)
        src_dest.addWidget(submit_end_sc)

        sc = QVBoxLayout()
        sc.addLayout(x_entry)
        sc.addItem(verticalSpacer)
        sc.addLayout(y_entry)
        sc.addItem(verticalSpacer)
        sc.addLayout(z_entry)

        sc.addItem(verticalSpacer)
        sc.addItem(verticalSpacer)
        sc.addLayout(xyz_header)
        sc.addWidget(check_joint_limits)
        
        
        sc.addItem(verticalSpacer)
        sc.addItem(verticalSpacer)
        sc.addWidget(wp_name_sc)
        sc.addLayout(src_dest)
        static_controls.setLayout(sc)
        

        box_width = QHBoxLayout()
        box_width.addWidget(width_label)
        box_width.addItem(micro_horizontalSpacer)
        box_width.addWidget(width_entry)
        box_length = QHBoxLayout()
        box_length.addWidget(length_label)
        box_length.addItem(micro_horizontalSpacer)
        box_length.addWidget(length_entry)
        box_height = QHBoxLayout()
        box_height.addWidget(height_label)
        box_height.addItem(micro_horizontalSpacer)
        box_height.addWidget(height_entry)

        cc = QVBoxLayout()
        cc.addItem(verticalSpacer)
        cc.addWidget(forward_btn)
        cc.addItem(verticalSpacer)
        cc.addWidget(backward_btn)
        cc.addItem(verticalSpacer)
        cc.addWidget(dimensions_label)
        cc.addLayout(box_width)
        cc.addLayout(box_length)
        cc.addLayout(box_height)
        cc.addItem(verticalSpacer)
        cc.addWidget(set_btn)
        conveyor_controls.setLayout(cc)

        bank = QHBoxLayout()
        bank.addWidget(waypoint_tree)

        bank_controls = QVBoxLayout()
        bank_controls.addWidget(waypoint_controls)


        tr = QHBoxLayout()
        tr.addLayout(bank, stretch=3)
        tr.addLayout(bank_controls, stretch=1)
        top_row.setLayout(tr)


        bottom_row = QHBoxLayout()
        bottom_row.addWidget(dynamic_controls,  stretch=2)
        bottom_row.addItem(micro_horizontalSpacer)
        bottom_row.addWidget(static_controls, stretch=1)
        bottom_row.addItem(micro_horizontalSpacer)
        bottom_row.addWidget(conveyor_controls, stretch=0)

        lhs = QVBoxLayout()
        lhs.addWidget(top_row)
        lhs.addItem(verticalSpacer)
        lhs.addLayout(bottom_row)

        rhs = QVBoxLayout()
        rhs.addWidget(placeholder)
        rhs.addWidget(placeholder)

        main_layout = QHBoxLayout()
        main_layout.addLayout(lhs, stretch=5)
        main_layout.addLayout(rhs, stretch=2)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # event loop
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
