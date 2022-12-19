import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Induct Testbench Control  (v1.0.0-alpha)")
        self.setGeometry(0, 0, 1160, 640)

        # design 
        title=QFont()
        title.setBold(True)
        #title.setPixelSize()

        unbold=QFont()
        unbold.setBold(False)
        #title.setPixelSize()


        
        
        # Waypoint Bank
        
        waypoint_tree = QRadioButton("RadioButton 1")

        # Bank Controls
        waypoint_controls = QRadioButton("Import")

        # Dynamic Controls
        dynamic_controls = QGroupBox("Dynamic Controls")
        dynamic_controls.setFont(title)
    
        accel_dial = QDial(self)
        accel_dial.setMinimum(0)
        accel_dial.setMaximum(100)
        accel_dial.setValue(75)
    
        accel_label = QLabel("acceleration limiter:")
        accel_label.setFont(unbold)
        accel_value = QLabel("{}%".format(accel_dial.value()))
        accel_dial.valueChanged.connect(lambda value: accel_value.setText("{}%".format(accel_dial.value())))
        
        x_slider = QSlider(minimum=0, maximum=80, orientation=Qt.Horizontal)
        y_slider = QSlider(minimum=0, maximum=80, orientation=Qt.Horizontal)
        z_slider = QSlider(minimum=0, maximum=80, orientation=Qt.Horizontal)
        x_label = QLabel("x:")
        y_label = QLabel("y:")
        z_label = QLabel("z:")

        x_value = QLabel("{}".format(x_slider.value()))
        x_slider.valueChanged.connect(lambda value: x_value.setText("{}".format(x_slider.value())))
        x_value.setFont(title)
        x_value.setStyleSheet('color: deeppink')
        y_value = QLabel("{}".format(y_slider.value()))
        y_slider.valueChanged.connect(lambda value: y_value.setText("{}".format(y_slider.value())))
        y_value.setFont(title)
        y_value.setStyleSheet('color: deeppink')
        z_value = QLabel("{}".format(z_slider.value()))
        z_slider.valueChanged.connect(lambda value: z_value.setText("{}".format(z_slider.value())))
        z_value.setFont(title)
        z_value.setStyleSheet('color: deeppink')

        submit_name = QLineEdit('waypoint name')
        submit_name.setStyleSheet('color: darkgray')
        submit_name.setFont(unbold)
        submit_start = QPushButton('Source')
        submit_end = QPushButton('Destination')
        verticalSpacer = QSpacerItem(2, 20, QSizePolicy.Minimum)
        horizontalSpacer = QSpacerItem(40, 2, QSizePolicy.Minimum)


        # Static Controls
        static_controls = QGroupBox("Static Controls")
        static_controls.setFont(title)

        sc_x_label = QLabel("x:")
        sc_y_label = QLabel("y:")
        sc_z_label = QLabel("z:")

        x_static_label = QLabel("x:")
        y_static_label = QLabel("y:")
        z_static_label = QLabel("z:")

        x_static = QLineEdit('int')
        y_static = QLineEdit('int')
        z_static = QLineEdit('int')

        wp_name_sc = QLineEdit('waypoint name')
        wp_name_sc.setStyleSheet('color: darkgray')
        wp_name_sc.setFont(unbold)
        submit_start_sc = QPushButton('Source')
        submit_end_sc = QPushButton('Destination')
        check_joint_limits = QPushButton('Check Joint Limits')



        xyz_pos = QRadioButton("Static Controls")

        # Conveyor Controls
        conveyor_controls = QGroupBox("Conveyor Controls")
        stop_conveyor = QRadioButton("Conveyor_controls")

        # Joint Limits
        joint_limits = QGroupBox("Joint Limits")

        # Logo
        placeholder = QSlider(minimum=45, maximum=80, orientation=Qt.Horizontal)



        # layout 
        top_row = QGroupBox("Top Row")
        
        acceleration = QHBoxLayout()
        acceleration.addWidget(accel_dial)
        acceleration.addItem(horizontalSpacer)
        acceleration.addWidget(accel_label)
        acceleration.addWidget(accel_value)
        

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
        sliders.addLayout(slider_value_y)
        sliders.addWidget(y_slider)
        sliders.addLayout(slider_value_z)
        sliders.addWidget(z_slider)
        
        dc_submit = QHBoxLayout()
        dc_submit.addWidget(submit_name)
        dc_submit.addWidget(submit_start)
        dc_submit.addWidget(submit_end)

        dc = QVBoxLayout()
        dc.addLayout(acceleration)
        dc.addLayout(sliders)
        dc.addItem(verticalSpacer)
        dc.addLayout(dc_submit)
        dynamic_controls.setLayout(dc)


        xyz_header = QHBoxLayout()
        xyz_header.addWidget(sc_x_label)
        xyz_header.addWidget(sc_y_label)
        xyz_header.addWidget(sc_z_label)

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
        src_dest.addWidget(submit_end_sc)

        sc = QVBoxLayout()
        sc.addLayout(xyz_header)
        sc.addLayout(x_entry)
        sc.addLayout(y_entry)
        sc.addLayout(z_entry)
        sc.addWidget(check_joint_limits)
        sc.addWidget(wp_name_sc)
        sc.addLayout(src_dest)
        static_controls.setLayout(sc)
        

        cc = QHBoxLayout()
        cc.addWidget(stop_conveyor)
        conveyor_controls.setLayout(cc)

        tr = QHBoxLayout()
        tr.addWidget(waypoint_tree)
        tr.addWidget(waypoint_controls)
        top_row.setLayout(tr)


        bottom_row = QHBoxLayout()
        bottom_row.addWidget(dynamic_controls,  stretch=2)
        bottom_row.addWidget(static_controls, stretch=1)
        bottom_row.addWidget(conveyor_controls, stretch=0)

        lhs = QVBoxLayout()
        lhs.addWidget(top_row)
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
