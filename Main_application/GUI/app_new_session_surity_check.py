import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from GUI.ui_new_session_surity_check import Ui_surity_Dialog

class App_new_session_surity_check(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.app_new_session_surity_check_ui = Ui_surity_Dialog()
        # self.setCentralWidget(self.app_new_session_surity_check_ui.surity_Dialog)
        self.app_new_session_surity_check_ui.setupUi(self)