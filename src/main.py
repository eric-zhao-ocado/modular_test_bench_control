from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
import time

class RotatableContainer(QGraphicsView):
    def __init__(self, widget: QWidget, rotation: float):
        super(QGraphicsView, self).__init__()

        scene = QGraphicsScene(self)
        self.setScene(scene)

        self.proxy = QGraphicsProxyWidget()
        self.proxy.setWidget(widget)
        self.proxy.setTransformOriginPoint(self.proxy.boundingRect().center())
        self.proxy.setRotation(rotation)
        scene.addItem(self.proxy)

    def rotate(self, rotation: float):
        self.proxy.setRotation(rotation)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Induct Testbench Control  (v1.0.0-alpha)")
        self.setGeometry(0, 0, 1920, 1080)  #posX, posY, w, h

        # Widget you want to rotate
        label = QLabel("Stack Overflow", alignment=Qt.AlignCenter)
        # Container you place the widget in
        container = RotatableContainer(widget=label, rotation=0)

        # Create slider and connect to the rotate method in the container
        slider = QSlider(minimum=45, maximum=359, orientation=Qt.Horizontal)
        slider.valueChanged.connect(container.rotate)
        container3 = RotatableContainer(widget=slider, rotation=45)

        label_text = QLabel("{}°".format(slider.value()), alignment=Qt.AlignCenter)
        slider.valueChanged.connect(lambda value: label_text.setText("{}°".format(slider.value())))
        slider.setValue(45)

        label2 = QLabel("Jordan", alignment=Qt.AlignCenter)
        container2 = RotatableContainer(widget=label2, rotation=45)

        # Display the widgets
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(container)
        lay.addWidget(container2)
        lay.addWidget(container3)
        lay.addWidget(slider)
        lay.addWidget(label_text)
        w.resize(1920, 1080)

        self.setCentralWidget(w)
        self.show()


app = QApplication([])  # Holds the event loop
window = MainWindow()
app.exec_()
