import sys
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QWidget, QFileDialog, QMessageBox

from GUI.ui_main_application_first_window import Ui_CLI_automation_main_application_first_window
import GUI.Application_GUI_rc

import os
import logging
from pathlib import Path

class App_main_application_first_window(QWidget):
    def __init__(self):
        # self.log_file = "C:\\Ericsson_Application_Logs\\CLI_Automation_Logs\\Main_Application.log"
        
        # Path(os.path.dirname(self.log_file)).mkdir(parents=True, exist_ok = True)
            
        # if(os.path.exists(self.log_file)):
        #     os.remove(self.log_file)
            
        #     with open(self.log_file, 'w') as _f:
        #         _f.close()
                
        # logging.basicConfig(filename=self.log_file,
        #                     filemode="a",
        #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({'%(module)s'}): {'%(message)s'}",
        #                     datefmt='%d-%b-%Y %I:%M:%S %p',
        #                     encoding= "UTF-8",
        #                     level=logging.DEBUG)
        
        QWidget.__init__(self)
        
        logging.debug("Creating ui object for Ui_CLI_automation_main_application_first_window")
        self.ui = Ui_CLI_automation_main_application_first_window()
        
        
        # self.setCentralWidget(self.ui.CLI_automation_main_application_first_window)
        logging.debug("Setting Up the Ui")
        self.ui.setupUi(self)
        
        self.host_details_file = ''
        
        self.colors = {'Unsuccessful':'rgb(255,0,0)',
                       'Successful':'rgb(0,255,0)',
                       'In Progress' : 'rgb(255,255,255)'}
        print("Inside __init_ of App_main_application_first_window __init__")
        
        # self.show()
        
    def file_browser(self):
        logging.debug("Opening the Filedialog to select the Host Details file")
        self.host_details_file,_ = QFileDialog.getOpenFileName(self,"Select Host Detail","\\C:\\","Excel File (*.xlsx);;All Files (*.*)","Excel File (*.xlsx)")
        
        logging.debug("Setting the TextlineEdit for the file details with the selected file")
        self.ui.file_browser_path_lineEdit.setText(f" Host Details: - {self.host_details_file}")
        
    def host_details_file_method(self):
        if(len(self.host_details_file) == 0):
            logging.debug("Creating QMessage Object for raising messages for empty self.host_details_file ")
            _message = QMessageBox()
            _message.setWindowIcon(":/Main_Application_window/ericsson-blue-icon-logo.ico")
            _message.setWindowTitle(title= "Host Details Not Selected")
            _message.setText(text= "Kindly Select the \'Host Details\' file first!")
            _message.setIcon(QMessageBox.Critical)
            _message.setStandardButtons(QMessageBox.StandardButton.Ok)
            _message.setDefaultButton(QMessageBox.StandardButton.Ok)
            
            return _message.exec()
        
        else:
            logging.debug(f"returning the self.host_details_file -> {self.host_details_file}")
            return self.host_details_file
    
    def task_method_status_updater(self,status:str) -> None:
        logging.debug("Updating the label of Sheet creater task label and styling it according to status")
        self.ui.sheet_creator_status_label.setText(QCoreApplication.translate("CLI_automation_main_application_first_window", status, None))
        self.ui.sheet_creator_status_label.setStyleSheet(u"#sheet_creator_status_label{\n"
                                                         f"color :{self.colors[status]};\n"
                                                         "padding-bottom:30px;\n"
                                                         "margin-bottom:30px;\n"
                                                         "	font: 700 16pt \"Ericsson Hilda\";\n"
                                                         "}\n"
                                                         "\n")
# import sys
# import time
# from PySide6.QtWidgets import QApplication
# app = QApplication(sys.argv)
# window = App_main_application_first_window()
# window.show()

# # i = 0
# # while(i <= 100):
# #     if(i == 50):
# #         i+=10
# #     window.message(counter=i, label_text= f"Checking {i}")
# #     time.sleep(1.5)
# #     i+=10

# # window.close()
# # sys.exit()
# app.exec()