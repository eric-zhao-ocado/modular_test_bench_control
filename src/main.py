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
        dynamic_controls_g = QGroupBox("Dynamic Controls")
        x_slider = QSlider(minimum=45, maximum=80, orientation=Qt.Horizontal)
        y_slider = QSlider(minimum=45, maximum=80, orientation=Qt.Horizontal)
        z_slider = QSlider(minimum=45, maximum=80, orientation=Qt.Horizontal)

        # Static Controls
        static_controls_g = QGroupBox("Static Controls")
        xyz_pos = QRadioButton("Static Controls")

        # Conveyor Controls
        conveyor_controls_g = QGroupBox("Conveyor Controls")
        stop_conveyor = QRadioButton("Conveyor_controls")

        # Joint Limits
        joint_limits = QGroupBox("Joint Limits")

        # Logo
        placeholder = QSlider(minimum=45, maximum=80, orientation=Qt.Horizontal)



        # layout 
        top_row_g = QGroupBox("Top Row")
        

        dynamic_controls = QHBoxLayout()
        dynamic_controls.addWidget(x_slider)
        dynamic_controls_g.setLayout(dynamic_controls)

        static_controls = QHBoxLayout()
        static_controls.addWidget(xyz_pos)
        static_controls_g.setLayout(static_controls)
        

        conveyor_controls = QHBoxLayout()
        conveyor_controls.addWidget(stop_conveyor)
        conveyor_controls_g.setLayout(conveyor_controls)

        top_row = QHBoxLayout()
        top_row.addWidget(waypoint_tree)
        top_row.addWidget(waypoint_controls)
        top_row_g.setLayout(top_row)


        bottom_row = QHBoxLayout()
        bottom_row.addWidget(dynamic_controls_g)
        bottom_row.addWidget(static_controls_g)
        bottom_row.addWidget(conveyor_controls_g)

        lhs = QVBoxLayout()
        lhs.addWidget(top_row_g)
        lhs.addLayout(bottom_row)

        rhs = QVBoxLayout()
        rhs.addWidget(z_slider)
        rhs.addWidget(placeholder)

        main_layout = QHBoxLayout()
        main_layout.addLayout(lhs)
        main_layout.addLayout(rhs)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # event loop
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
