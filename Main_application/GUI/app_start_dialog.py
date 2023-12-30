import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from GUI.ui_app_start_dialog_box import Ui_application_start_dialog

class App_start_dialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.app_start_dialog_ui = Ui_application_start_dialog()
        self.app_start_dialog_ui.__init__()
        # self.setCentralWidget(self.app_start_dialog_ui.application_start_dialog)
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        self.app_start_dialog_ui.setupUi(self)
            