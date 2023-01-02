"""onset detector dialog"""

import librosa
import numpy as np

from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QColor
import pyqtgraph as pg
from views.onsetDetectorMain import Ui_onsetDetectorMain

# from pyqtgraph import PlotWidget, plot


class OnsetDetectorDlg(QDialog):
    """onset detector main dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.main_ui = Ui_onsetDetectorMain()
        self.main_ui.setupUi(self)

        self.main_ui.graphWidget = pg.PlotWidget()
        self.main_ui.graphWidget.setBackground(QColor(200, 200, 200))
        self.main_ui.layout_for_graph.addWidget(self.main_ui.graphWidget)

        points = [1000, 5000, 10000, 20000]

        data, _ = librosa.load(
            '../study/AirSolo_ImpP4Po441.wav', mono=True, sr=44100)

        hour = np.linspace(0, len(data), len(data))
        temperature = data

        pen = pg.mkPen(color=(51, 255, 249))
        self.main_ui.graphWidget.plot(hour, temperature, pen=pen)

        pen = pg.mkPen(color=(255, 0, 0))
        for i in points:
            self.main_ui.graphWidget.plot([i, i], [-1, 1], width=3, pen=pen)

            # self.setLayout(self.main_ui.layout_for_graph)
