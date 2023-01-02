#!/usr/bin/env python3

from converter.backend import AudioConverter
from views.onsetDetectorMain import Ui_onsetDetectorMain
from views.mainMenu import Ui_MainMenu
from views.finishWindow import Ui_Form
from views.converterMain import Ui_MainWin
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import sys
import librosa
import numpy as np
from pathlib import Path
import common
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QDialog, QMainWindow,
                             QPushButton, QFileDialog, QVBoxLayout)

DEF_SAMPLERATE = 44100
DEF_FILETYPE = 'wav'
DEF_NR_OF_CHANNELS = 1


class Window(QMainWindow):
    """Main window
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_MainMenu()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)
        self.ui.converter_push.clicked.connect(self.on_converter_btn_clicked)
        self.ui.onset_detector_push.clicked.connect(
            self.on_onset_detector_btn_clicked)

    def on_converter_btn_clicked(self):
        dlg = ConverterDlg()
        dlg.exec()

    def on_onset_detector_btn_clicked(self):
        dlg = OnsetDetectorDlg()
        dlg.setGeometry(0, 0, 1280, 600)
        # dlg.show()
        dlg.exec()
        # sys.exit(dlg.exec())


class ConverterDlg(QDialog):
    """converter dialog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_MainWin()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        print(self.ui.__dict__)
        self.dropdown_populate()
        self.converter = AudioConverter()
        self.controller()

        # self.ui.perform_push.setEnabled(False)

    def dropdown_populate(self):
        self.ui.sr_dropdown.addItems([str(x) for x in common.SR])
        self.ui.format_dropdown.addItems(common.FORMATS)
        self.ui.channels_dropdown.addItems(
            [str(x) for x in common.CHANNELS])
        # self.ui.subtype_dropdown.addItems(view_data.SUBTYPE)

    def controller(self):
        self.ui.input_push_browse.clicked.connect(self.set_input_file)
        self.ui.output_push_browse.clicked.connect(self.set_output_dir)
        self.ui.format_dropdown.currentIndexChanged.connect(
            lambda i: self.set_format_all(common.FORMATS[i]))
        self.ui.perform_push.clicked.connect(self.perform)

    def set_format_all(self, val):
        self.converter.audioformat = val
        old_text = self.ui.output_file_form.text()

        if not old_text:
            self.ui.output_file_form.setText(f'Untitled.{val}')
        else:
            old_text = Path(old_text)
            self.ui.output_file_form.setText(f'{old_text.stem}.{val}')

    def set_input_file(self):
        formats = ' '.join([f"*.{x}" for x in common.FORMATS[1:]])
        f_name = QFileDialog.getOpenFileName(self,
                                             'Open file',
                                             str(Path('.')),
                                             f"Audio files ({formats})")
        filename = Path(f_name[0])
        self.ui.input_file_form.setText(str(filename))

        if self.converter.audioformat:
            str_f = f'{filename.stem}.{self.converter.audioformat}'
        else:
            str_f = str(filename.name)

        self.ui.output_file_form.setText(str_f)

    def set_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                     'Open Directory',
                                                     str(Path('.')))
        self.ui.output_dir_form.setText(directory)

    def set_source_path(self):
        self.converter.sourcepath = self._input_file

    def config_output_file(self):
        output_dir = self.ui.output_dir_form.text()
        output_file = self.ui.output_file_form.text()
        input_file = self.ui.input_file_form.text()

        sr_index = self.ui.sr_dropdown.currentIndex()
        samplerate = common.SR[sr_index] if sr_index > 0 else DEF_SAMPLERATE
        filetype_index = self.ui.format_dropdown.currentIndex()
        filetype = common.FORMATS[filetype_index] if filetype_index > 0 else DEF_FILETYPE
        channels = self.ui.channels_dropdown.currentIndex() or DEF_NR_OF_CHANNELS

        self.converter.clear()
        self.converter.sourcepath = Path(input_file)
        self.converter.destpath = Path(output_dir) / Path(output_file)
        self.converter.samplerate = samplerate
        self.converter.channels = channels
        self.converter.audioformat = filetype

    def perform(self):
        self.config_output_file()
        res = self.converter.export()
        self.finish = FinishWindow()
        if res:
            self.finish.exec()


class FinishWindow(QDialog):
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.ui = Ui_Form()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)
        self.ui.exit_push.clicked.connect(self.close)


class OnsetDetectorDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_onsetDetectorMain()
        self.ui.setupUi(self)

        self.ui.graphWidget = pg.PlotWidget()
        self.ui.layout_for_graph.addWidget(self.ui.graphWidget)

        data, sr = librosa.load(
            '../study/AirSolo_ImpP4Po441.wav', mono=True, sr=44100)
        # onset = librosa.onset.onset_detect(y=data, sr=sr, units='time')

        hour = np.linspace(0, len(data), len(data))
        temperature = data

        self.ui.graphWidget.plot(hour, temperature)

        # self.setLayout(self.ui.layout_for_graph)


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)
    # Create and show the application's main window
    win = Window()
    win.show()
    # Run the application's main loop
    sys.exit(app.exec())
