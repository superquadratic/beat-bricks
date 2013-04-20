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
        success, cv_image = self.capture.read()
        if success:
            self.image.emit(cv_image)


def cv_image_to_qt_image(cv_image):
    cv_image_rgb = cv2.cvtColor(cv_image, cv2.cv.CV_BGR2RGB)
    height, width, channels = cv_image_rgb.shape
    format = QtGui.QImage.Format_RGB888
    return QtGui.QImage(cv_image_rgb.data, width, height, format)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    # main window
    win = QtGui.QMainWindow()
    win.setWindowTitle("Beat Bricks")
    win.show()

    # central widget
    central_widget = QtGui.QWidget()
    win.setCentralWidget(central_widget)

    layout = QtGui.QHBoxLayout()
    central_widget.setLayout(layout)

    # label to display the image
    label = QtGui.QLabel()
    layout.addWidget(label)

    def show_image(cv_image):
        qt_image = cv_image_to_qt_image(cv_image)
        pixmap = QtGui.QPixmap.fromImage(qt_image)
        label.setPixmap(pixmap)

    # connect camera
    cam = Camera()
    cam.image.connect(show_image)

    # start event loop
    sys.exit(app.exec_())
