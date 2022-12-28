#!/usr/bin/env python3

import sys
from pathlib import Path
import common
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QFileDialog
from views.converterMain import Ui_MainWindow
from converter.backend import AudioConverter

DEFDROP = ['---']


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

    def dropdown_populate(self):
        self.ui.sr_dropdown.addItems([str(x) for x in common.SR])
        self.ui.format_dropdown.addItems(common.FORMATS)
        self.ui.channels_dropdown.addItems(
            [str(x) for x in common.CHANNELS])
        # self.ui.subtype_dropdown.addItems(view_data.SUBTYPE)

    def controller(self):
        self.ui.input_push_browse.clicked.connect(self.set_file)
        self.ui.output_push_browse.clicked.connect(self.set_output_dir)
        self.ui.sr_dropdown.currentIndexChanged.connect(
            lambda i: self.converter.set_samplerate(common.SR[i]))
        self.ui.channels_dropdown.currentIndexChanged.connect(
            lambda i: self.converter.set_channels(common.CHANNELS[i]))
        self.ui.format_dropdown.currentIndexChanged.connect(
            lambda i: self.set_format_all(common.FORMATS[i]))
        self.ui.subtype_dropdown.currentIndexChanged.connect(
            lambda i: print("subtype", i))
        self.ui.perform_push.clicked.connect(self.converter.export)

    def set_format_all(self, val):
        self.converter.set_format(val)
        old_text = self.ui.output_file_form.text()

        if not old_text:
            self.ui.output_file_form.setText(f'Untitled.{val}')
        else:
            old_text = Path(old_text)
            self.ui.output_file_form.setText(f'{old_text.stem}.{val}')

    def set_file(self):
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
        dir = QFileDialog.getExistingDirectory(self,
                                               'Open Directory',
                                               str(Path('.')))
        # QFileDialog.ShowDirsOnly
        # | QFileDialog.DontResolveSymlinks)
        self.ui.output_dir_form.setText(dir)


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)
    # Create and show the application's main window
    win = Window()
    win.show()
    # Run the application's main loop
    sys.exit(app.exec())
