#!/usr/bin/env python3

import sys
from pathlib import Path
import common
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QFileDialog
from views.converterMain import Ui_MainWindow
from converter.backend import AudioConverter

DEF_SAMPLERATE = 44100
DEF_FILETYPE = 'wav'
DEF_NR_OF_CHANNELS = 1


class Window(QMainWindow):
    """Main window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        # Use a QPushButton for the central widget
        self.central_widget = QPushButton("CONVERTER")
        # Connect the .clicked() signal with the .onEmployeeBtnClicked() slot
        self.central_widget.clicked.connect(self.on_converter_btn_clicked)
        self.setCentralWidget(self.central_widget)

    # Create a slot for launching the employee dialog
    def on_converter_btn_clicked(self):
        """Launch the converter dialog."""
        dlg = ConverterDlg(self)
        dlg.exec()


class ConverterDlg(QDialog):
    """converter dialog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_MainWindow()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)
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
        # self.converter.set_format(val)
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
        self.converter.export()


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)
    # Create and show the application's main window
    win = Window()
    win.show()
    # Run the application's main loop
    sys.exit(app.exec())
