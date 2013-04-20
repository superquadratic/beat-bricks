#!/usr/bin/env python

import sys

import cv2
import numpy
from PySide import QtCore, QtGui


class Camera(QtCore.QObject):
    image = QtCore.Signal(numpy.ndarray)

    def __init__(self):
        super(Camera, self).__init__()
        self.capture = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.grabImage)
        self.timer.start()

    def grabImage(self):
        success, frame = self.capture.read()
        if success:
            self.image.emit(frame)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    # main window
    win = QtGui.QMainWindow()
    win.resize(500, 500)
    win.setWindowTitle("Beat Bricks")
    win.show()

    # central widget
    central_widget = QtGui.QWidget()
    win.setCentralWidget(central_widget)

    layout = QtGui.QHBoxLayout()
    central_widget.setLayout(layout)

    label = QtGui.QLabel("Hello")
    layout.addWidget(label)

    # image capture
    cam = Camera()

    sys.exit(app.exec_())
