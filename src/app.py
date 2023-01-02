#!/usr/bin/env python3


import sys
from views.mainMenu import Ui_MainMenu
from converter.converter_dialog import ConverterDlg
from onset_detector.onset_detector_dialog import OnsetDetectorDlg
from PyQt6.QtWidgets import QApplication, QMainWindow


class Window(QMainWindow):
    """Main window"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_ui = Ui_MainMenu()
        self.main_ui.setupUi(self)
        self.main_ui.converter_push.clicked.connect(
            self.on_converter_btn_clicked)
        self.main_ui.onset_detector_push.clicked.connect(
            self.on_onset_detector_btn_clicked)

    def on_converter_btn_clicked(self):
        """create an instance of converter dialog"""
        dlg = ConverterDlg()
        dlg.exec()

    def on_onset_detector_btn_clicked(self):
        """create an instance of onset detector dialog"""
        dlg = OnsetDetectorDlg()
        dlg.setGeometry(0, 0, 1280, 600)
        # dlg.show()
        dlg.exec()
        # sys.exit(dlg.exec())


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)
    # Create and show the application's main window
    win = Window()
    win.show()
    # Run the application's main loop
    sys.exit(app.exec())
