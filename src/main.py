import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Induct Testbench Control  (v1.0.0-alpha)")
        self.setGeometry(0, 0, 1920, 1080)

        # Waypoint Bank
        
        waypoint_tree = QRadioButton("RadioButton 1")

        # Bank Controls
        waypoint_controls = QRadioButton("Import")

        # Dynamic Controls
        dynamic_controls = QGroupBox("Dynamic Controls")
        accel_label = QLabel("arm acceleration:")
        accel_value = QLabel("344")
        accel_dial = QDial(self)
        x_slider = QSlider(minimum=45, maximum=80, orientation=Qt.Horizontal)
        y_slider = QSlider(minimum=45, maximum=80, orientation=Qt.Horizontal)
        z_slider = QSlider(minimum=45, maximum=80, orientation=Qt.Horizontal)
        x_label = QLabel("x:")
        y_label = QLabel("y:")
        z_label = QLabel("z:")
        x_value = QLabel("x:")
        y_value = QLabel("y:")
        z_value = QLabel("z:")
        submit_name = QLineEdit('Waypoint name')
        submit_start = QPushButton('Source')
        submit_end = QPushButton('Destination')
        verticalSpacer = QSpacerItem(2, 20, QSizePolicy.Minimum)
        horizontalSpacer = QSpacerItem(40, 2, QSizePolicy.Minimum)

        # Static Controls
        static_controls = QGroupBox("Static Controls")
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
        

        sliders = QVBoxLayout()
        sliders.addWidget(x_label)
        sliders.addWidget(x_slider)
        sliders.addWidget(y_label)
        sliders.addWidget(y_slider)
        sliders.addWidget(z_label)
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

        sc = QHBoxLayout()
        sc.addWidget(xyz_pos)
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
