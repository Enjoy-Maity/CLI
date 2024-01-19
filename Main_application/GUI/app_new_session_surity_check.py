import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
import logging
from GUI.ui_new_session_surity_check import Ui_surity_Dialog


class App_new_session_surity_check(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.app_new_session_surity_check_ui = Ui_surity_Dialog()
        # self.setCentralWidget(self.app_new_session_surity_check_ui.surity_Dialog)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.app_new_session_surity_check_ui.setupUi(self)
        self.user_button_clicked = ''

    def yes_button_clicked(self):
        logging.debug("User Clicked \'Yes\'")
        self.user_button_clicked = 'Yes'

        logging.debug("Closing the new session surity dialog Box")
        self.close()

    def no_button_clicked(self):
        logging.debug("User Clicked \'No\'")
        self.user_button_clicked = 'No'

        logging.debug("Closing the new session surity dialog Box")
        self.close()
