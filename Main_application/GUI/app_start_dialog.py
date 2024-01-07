import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from GUI.ui_app_start_dialog_box import Ui_application_start_dialog

class App_start_dialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # Ui_application_start_dialog.__init__(self)
        self.ui = Ui_application_start_dialog()
        # self.setCentralWidget(self.app_start_dialog_ui.application_start_dialog)
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        self.ui.setupUi(self)
        self.user_response = ''
    
    def existing_session(self):
        self.user_response = "Existing Session"
        self.close()
        
    def new_session(self):
        self.user_response = "New Session"
        self.close()