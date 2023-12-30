import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QMainWindow,QFileDialog

from GUI.ui_main_application_first_window import Ui_CLI_automation_main_application_first_window

class App_main_application_first_window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_CLI_automation_main_application_first_window()
        self.ui.__init__()
        
        
        # self.setCentralWidget(self.ui.CLI_automation_main_application_first_window)
        self.ui.setupUi(self)
        
        self.host_details_file = ''
        
        self.colors = {'Unsuccessful':'red',
                       'Successful':'green',
                       'In Progress' : 'white'}
        
    def file_browser(self):
        self.host_details_file = QFileDialog.getOpenFileName(self,
                                                             "Select Host Detail",
                                                             "C:\\",
                                                             "Excel File (*.xlsx);;All Files (*.*)")
        self.host_details_file = f" Host Details :- {self.host_details_file}"
    
    def task_method_status_updater(self,status:str) -> None:
        self.ui.sheet_creator_status_label_text = status
        self.ui.sheet_creator_status_label_color = self.colors[status]
        
    def task_status(self,status:str ):
        self.ui.sheet_creator_status_label_text = status
        
        self.ui.sheet_creator_status_label_color = self.colors[status]
        

