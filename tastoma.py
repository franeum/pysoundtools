#!/usr/bin/env python3

from PyQt6 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.button = QtWidgets.QPushButton("press me")
        self.button.setObjectName("output_push_browse")
        self.setCentralWidget(self.button)
        self.button.clicked.connect(self.create)

    def create(self):
        win = Dialog()
        win.exec()


class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.graphWidget = pg.PlotWidget()
        # self.setCentralWidget(self.graphWidget)
        self.graphWidget.setGeometry(QtCore.QRect(10, 10, 640, 480))

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        # plot data: x, y values
        self.graphWidget.plot(hour, temperature)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
