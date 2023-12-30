import os
import sys
import time
import sqlite3
import logging
import traceback
import pandas as pd
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt


# Importing the GUI classes
from Database_manager import Database_manager
from GUI.splash_screen_window import Splash_screen
from GUI.app_Main_Window import App_Main_Window
from GUI.app_new_session_surity_check import App_new_session_surity_check
from GUI.app_start_dialog import App_start_dialog
from GUI.app_main_application_first_window import App_main_application_first_window

# Importing all the UI files
from GUI.ui_app_start_dialog_box import Ui_application_start_dialog
from GUI.ui_Main_Application import Ui_Main_Application_Window
from GUI.ui_main_application_first_window import Ui_CLI_automation_main_application_first_window
from GUI.ui_new_session_surity_check import Ui_surity_Dialog
from GUI.ui_splash_screen import Ui_splash_screen
from GUI.database_model import DataModel

# Importing the custom exception
from Custom_Exception import CustomException

class Main_Gui():
    def __init__(self):
        self.log_file = "C:\\Ericsson_Application_Logs\\CLI_Automation_Logs\\Main_Application.log"
        logging.basicConfig(filename=self.log_file,
                            filemode="a",
                            format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({'%(module)s'}): {'%(message)s'}",
                            datefmt='%d-%b-%Y %I:%M:%S %p',
                            encoding= "UTF-8",
                            level=logging.DEBUG)
        self.db_path = "C:\\Users\\emaienj\\AppData\\Local\\CLI_Automation\\Database\\CLI_Automation_Database.db"
        
        self.host_details_path = ''
        
        
        # Checks for the need for new session
        self.new_session_needed = False
        
        # Creating a flag for checking if the user needs a new session
        self.user_induced_new_session = False
        
        # Creating a flag for task-running
        self.task_running = ""
        
        # Creating a flag for vendor selected 
        self.vendor_selected = ""
        
        # Creating a flag for taking the task status
        self.status = ""
        
        # Database Manager class object
        self._database_manager = Database_manager()
        self._database_manager.auto_database_remover()
    
    # Creating the destructor to clean up everything and exit the Gui App
    def __del__(self):
        sys.exit()
        
        
    def database_checker(self) -> bool:
        """Checking of the database exists or not or needs to be autoremoved to be created again
        """
        database_exists = False
        if(not os.path.exists(path= self.db_path)):
            self._database_manager.table_creater()
            logging.debug("Created the Database")
        
        if(os.path.exists(path= self.db_path)):
            logging.debug("Database Found")
            database_exists = True
        
        return database_exists
    
    def isdatabase_same_session(self) -> bool:
        """Checks for the existing database and getting the ctime and mtime to get the timedelta() to check for day >=1 or hours >= 20
           and getting the bool result

        Returns:
            bool: _description_ : getting the result as True or False
        """
        self.db_path_existence = os.path.exists(self.db_path)
        if(not self.db_path_existence):
            return False
        
        self.db_getmtime = datetime.fromtimestamp(os.path.getmtime(self.db_path))
        if(((datetime.now() - self.db_getmtime).days >= 1) or ((datetime.now() - self.db_getmtime).seconds //3600 >= 20)):
            logging.debug("Returning false as the database modified time is either greater than 1 day or 20 hours")
            self._database_manager.auto_database_remover()
            return False
        
        self.db_getctime = datetime.fromtimestamp(os.path.getctime(self.db_path))
        if(((datetime.now() - self.db_getctime).days >= 1) or ((datetime.now() - self.db_getctime).seconds//3600 >= 20)):
            logging.debug("Returning false as the database creation time is either greater than 1 day or 20 hours")
            self._database_manager.auto_database_remover()
            return False
        
        else:
            return True
    
    def sheet_creater_task(self, file_name:str) -> str|None:
        if(task_running == ''):
            self._sheet_creator_task_status = ''
            try:
                self.task_running = 'Sheet Creater'
                from Sheet_creator import main_func
                self._sheet_creator_task_status = main_func(file_name= self.host_details_path)
                
            except Exception as e:
                self._sheet_creator_task_status = 'Unsuccessful'
            
            finally:
                self.task_running = ''
                return self._sheet_creator_task_status
        else:
            self.warning_messagebox(title= "Task Already Running!",text= f"{self.task_running} is already running! Please Wait for the completion of task execution!")
            return None
    
    def template_checks_task(self) -> str|None:
        if(self.task_running == ''):
            self._template_checks_task_status = ''
            try:
                self.task_running = 'Template Checks'
                from Template_checks import main_func
                self._template_checks_task_status = self.main_func()
            except Exception as e:
                self._template_checks_task_status = 'Unsuccessful'
            finally:
                self.task_running = ''
                return self._template_checks_task_status
        
        else:
            self.warning_messagebox(title="Task Already Running!",text=f"{self.task_running} is already running! Please Wait for the completion of task execution!")
            return None
    
    def running_config_pre_checks_task(self) -> str|None:
        if(self.task_running == ''):
            self._running_config_pre_checks_task_status = ''
            self.task_running = 'Running Config Pre Checks'
            
            try:
                self._running_config_pre_checks_task_status = 'Successful'
            except Exception as e:
                self._running_config_pre_checks_task_status = 'Unsuccessful'
            finally:
                self.task_running = ''
                return self._running_config_pre_checks_task_status
        
        else:
            self.warning_messagebox(title="Task Already Running!",text=f"{self.task_running} is already running! Please Wait for the completion of task execution!")
            return None
    
    def cli_preparation_task(self) -> str|None:
        if(self.task_running == ''):
            self._cli_preparation_task_status = ''
            try:
                self.task_running = 'CLI Preparation'
                
                self._cli_preparation_task_status = 'Successful'
            except Exception as e:
                self._cli_preparation_task_status = 'Unsuccessful'
            finally:
                return self._cli_preparation_task_status
        
        else:
            self.warning_messagebox(title="Task Already Running!",text=f"{self.task_running} is already running! Please Wait for the completion of task execution!")
            return None
    
    def running_config_post_checks_task(self) -> str|None:
        if(self.task_running == ''):
            self._running_config_post_checks_task_status = ''
            try:
                pass
            except Exception as e:
                pass
            finally:
                self.task_running = ''
                return self._running_config_post_checks_task_status
        
        else:
            self.warning_messagebox(title="Task Already Running!",text=f"{self.task_running} is already running! Please Wait for the completion of task execution!")
            return None
    
    def button_clicked(self):
        """
            Dummy Method to check button is clicked
        Returns:
            bool: _description_ : return True 
        """
        print("Function Called")
        return "User Clicked"
    
    def database_updater(self,vendor_selected:str ,task_running:str, status:str):
        """Updates the database from the given set of updates.

        Args:
            vendor_selected (str): _description_ : Vendor for which the row in the database needs to be updated
            task_running (str): _description_ : task for which the column needs to be updated
            status (str): _description_ : status which needs to be updated
        """
        self.vendor_selected = vendor_selected
        self.task_running = task_running
        self.status = status
        
        logging.debug(f"Updating the database for {self.vendor_selected} for {self.task_running} task with {self.status} status.")
        self._database_manager.database_updater(vendor=self.vendor_selected,
                                                task = self.task_running,
                                                status=self.vendor_task_status)
        
    def warning_messagebox(self,title:str, text:str) -> None:
        """Warning Messagebox

        Args:
            title (str): _description_ : title of the messagebox window
            text (str): _description_ : message to be shown
        """
        message = QMessageBox()
        message.setWindowTitle(title)
        message.setText(text)
        message.setWindowIcon(QIcon('./GUI/ericsson-blue-icon-logo'))
        message.setIcon(QMessageBox.Warning)
        message.setStandardButtons(QMessageBox.Ok)
        message.setDefaultButton(QMessageBox.Ok)
        
        message.buttonClicked.connect(message.close)
        message.exec()
    
    def information_messagebox(self, title:str, text:str) -> None:
        """Information Messagebox

        Args:
            title (str): _description_ : title of the messagebox window
            text (str): _description_ : message to be shown
        """
        message = QMessageBox()
        message.setWindowTitle(title)
        message.setText(text)
        message.setWindowIcon(QIcon('./GUI/ericsson-blue-icon-logo'))
        message.setIcon(QMessageBox.Information)
        message.setStandardButtons(QMessageBox.Ok)
        message.setDefaultButton(QMessageBox.Ok)
        
        message.buttonClicked.connect(message.close)
        message.exec()
    
    def critical_messagebox(self, title:str, text:str) -> None:
        """Information Messagebox

        Args:
            title (str): _description_ : title of the messagebox window
            text (str): _description_ : message to be shown
        """
        message = QMessageBox()
        message.setWindowTitle(title)
        message.setText(text)
        message.setWindowIcon(QIcon('./GUI/ericsson-blue-icon-logo'))
        message.setIcon(QMessageBox.Critical)
        message.setStandardButtons(QMessageBox.Ok)
        message.setDefaultButton(QMessageBox.Ok)
        
        message.buttonClicked.connect(message.close)
        message.exec()
    
    def pre_main(self):
        """ Performs the task necessary before starting the application.
        """
        self.result = self.database_checker()
        
        if(not self.result):
            logging.debug("Inside -> Main_Gui.Main_Gui.pre-main, Setting the self.new_session_needed to True")
            self.new_session_needed = True
        
        if(self.result):
            logging.debug(f"Got the session_result as \'{self.result}\' now checking for the is the database is for the same session or not")
            self.database_session_result = self.isdatabase_same_session()
            
        if(not self.database_session_result):
            logging.debug(f"Inside -> Main_Gui.Main_Gui.pre-main, Setting the self.new_session_needed to True after getting self.database_session_result as {self.database_session_result}")
            self.new_session_needed = True
        
        if(self.database_session_result):
            logging.debug(f"Inside -> Main_Gui.Main_Gui.pre-main, Setting the self.new_session_needed to True after getting database_session_result as \'{self.database_session_result}\'")
            self.new_session_needed = False
    
    def vendor_list_grabber(self, data: pd.DataFrame) -> list:
        """Gets the list of unique vendors

        Args:
            data (pandas.DataFrame): _description_ :dataframe containing the host details

        Returns:
            vendor_list (list): _description_ : list of unique vendors
        """
        
        return list(data['Vendor'].dropna().unique())
        
    def new_session(self):
        try:
            self.need_for_new_session_first_window_finished = False
            self.new_session_first_window = App_main_application_first_window()
            
            logging.debug("New Session --> Running the database auto remover to remove any older databases")
            self._database_manager.auto_database_remover()
            
            logging.debug("New Session --> Checking if there is any data in the database")
            self.data = self._database_manager.data_fetcher()
            
            if(self.new_session_first_window.ui.file_browser_pushButton.clicked.connect(self.button_clicked) == "User Clicked"):
                print("You clicked the browse button")
                self.new_session_first_window.file_browser()
                logging.debug("New Session --> Got the host details")
                self.host_details_path = self.new_session_first_window.host_details_file
            
            if(self.new_session_first_window.ui.submit_button_pushButton.clicked.connect(self.button_clicked) == "User Clicked"):
                logging.debug("New Session --> The User toggled submit button in first window")
            
                logging.debug("New Session --> Checking if the data is empty or not")
                if(len(self.data) == 0):
                    if(self.host_details_path.strip().endswith('-')):
                        self.warning_messagebox(title = 'File not Selected',text="Kindly select the file containing host details via \'Browse\' button and then retry again!")
                    
                    else:
                        if(not self.host_details_path.strip().endswith('.xlsx')):
                            self.warning_messagebox(title='Wrong File Format',text= 'Kindly select an excel file with \'.xlsx\' format for host details file')
                        
                        else:
                            excel_file = pd.ExcelFile(path_or_buffer=self.host_details_path)
                            excel_file_reader = pd.read_excel(excel_file,
                                                            sheet_name= 'Host Details')
                            excel_file.close()
                            del excel_file
                            
                            if((len(excel_file_reader) == 0) or (excel_file_reader == None)):
                                self.critical_messagebox(title='Empty File Detected',text='The Selected File does not contain any data! Kindly check the file that is selected')
                            else:
                                logging.debug("New Session --> Calling the method to find the vendor list")
                                vendor_list = self.vendor_list_grabber(data = excel_file_reader)
                                
                                if(len(vendor_list) == 0):
                                    self.critical_messagebox(title= "Vendor Details Empty",text= "Kindly enter the Vendor Details for the Node, then retry again!")
                                
                                else:
                                    logging.debug("New Session --> calling the data_adder of the _database_manager to add rows to the newly cleaned database")
                                    self._database_manager.data_adder(vendor_list = vendor_list)
                                    
                                    if(self.new_session_first_window.ui.sheet_creator_pushButton.clicked.connect(self.button_clicked) == "User Clicked"):
                                        logging.debug("New Session --> User clicked the Sheet Creator Task Button")

                                        self.sheet_creater_task_method_result = self.sheet_creater_task(file_name = self.host_details_path)
                                        if(self.sheet_creater_task_method_result != None):
                                            self.new_session_first_window.task_method_status_updater(status=self.sheet_creator_task_method_result)
                                        
                                    if(self.sheet_creator_task_method_result != 'Successful'):
                                        self.critical_messagebox(title= "Sheet Creater Not Successfully Completed!",text= "Kindly Click the \'Submit\' button only after successful completion of Sheet Creater Task")
                                    
                                    else:
                                        self.need_for_new_session_first_window_finished = True
                                        self.new_session_first_window.close()
                
            self.new_session_first_window.show()

            if(self.need_for_new_session_first_window_finished):
                self.main_application_window = App_Main_Window()
                logging.debug("Checking the self.host_details_path to be non-empty")
                self.host_details_file_path = rf"C:\Users\{username}\AppData\Local\CLI_Automation\Host_details_Pickle_file\Host_details_Path.txt"
                if(not os.path.exists(path=self.host_details_path)):
                    logging.debug("File path for checking \'Host Details\' file is non-existent, so needed new sesion\n")
                    
                    self.warning_messagebox(title="Host Details Not Found",text = "\'Host Details\' file details are not found, So need to create a New Session")
                    self.new_session()
                    
                with open(file=self.host_details_file_path, mode='r' ) as f:
                    self.host_details_path = f.readline().strip()
                    f.close()
                
                if(len(self.host_details_path) == 0):
                    logging.debug("File path for checking \'Host Details\' file is empty, so needed new sesion\n")
                    
                    self.warning_messagebox(title="Host Details Not Found",text = "\'Host Details\' file details are not found, So need to create a New Session")
                    
                    self.new_session()
                    
                if(self.session_selected_by_user == 'Existing Session'):
                    self.data = self._database_manager.data_fetcher()
                    self.main_application_window = App_Main_Window()
                    
                    self.data = self._database_manager.data_fetcher()
                    self.main_application_window.table_view_data_loader(data=self.data)
                    logging.debug(f"New Session --> Loading the existing data in the table_view ==>\n{self.data}")
                    
                    self.main_application_window.main_window_ui.selected_host_details_line_edit.setText(f" Host Details: - {self.host_details_path}")
                    
                    # Setting the vendor selected to be changed when the user clicks on the combobox
                    self.main_application_window.main_window_ui.vendor_details_selection_combobox.activated.connect(self.main_application_window.current_vendor)
                    self.vendor_selected = self.main_application_window.vendor_selected
                    
                        
                    if(self.main_application_window.main_window_ui.new_session_button_3.clicked.connect(self.button_clicked) == "User Clicked"):
                        logging.debug("New Session --> User selected to start New Session")
                        self.new_session_surity_check_window = App_new_session_surity_check()
                        self.new_session_surity_check_window.show()
                        
                        if(self.new_session_surity_check_window.app_new_session_surity_check_ui.yes_pushButton.clicked.connect(self.button_clicked) == "User Clicked"):
                            logging.debug("New Session --> User Selected Yes in new_session_surity_check_window")
                            self.new_session_surity_check_window.close()
                            self.new_session()
                        
                        if(self.new_session_surity_check_window.app_new_session_surity_check_ui.no_pushButton.clicked.connect(self.button_clicked) == "User Clicked"):
                            logging.debug("New Session --> User Selected No in new_session_surity_check_window")
                            self.new_session_surity_check_window.close()
                    
                    if(self.main_application_window.main_window_ui.template_checks_btn.clicked.connect(self.button_clicked) == "User Clicked"):
                        logging.debug("New Session --> User Clicked the Template Checks Button")
                        
                        if((len(self.main_application_window.main_window_ui.vendor_selected) > 0) and (self.main_application_window.main_window_ui.vendor_details_selection_combobox.currentText().strip() != 'Select Vendor')):
                            logging.debug("New Session --> The user didn't select any vendor")
                            self.warning_messagebox(title="Vendor Not Selected",text="Kindly Select a Vendor!")
                        
                        
                        if(len(self.main_application_window.main_window_ui.template_checks_label_text) == 'Successful'):
                            self.information_messagebox(title= "Task Successfully Completed!",text= "Task is already successfully completed!!")
                        
                        else:
                            logging.debug("New Session --> Starting the task")
                            self.template_checks_task_method_result = self.template_checks_task()
                            
                            if(self.template_checks_task_method_result != None):
                                logging.debug("New Session --> Got the result from the method execution of template_checks_task")
                                self.main_application_window.task_method_status_updater(task= 'Template Checks',
                                                                                        status = self.template_checks_task_method_result)
                                
                                self.database_updater(vendor_selected= self.vendor_selected,
                                                    task_running='Template_Checks',
                                                    status=self.template_checks_task_method_result)
                                
                                self.main_application_window.task_method_status_updater(task='Template_Checks',
                                                                                        status=self.template_checks_task_method_result)
                                
                                self.main_application_window.data = self._database_manager.data_fetcher()
                                self.main_application_window.table_view_data_loader()
                    
                    if(self.main_application_window.main_window_ui.running_config_pre_checks_btn.clicked.connect(self.button_clicked) == "User Clicked"):
                        logging.debug("New Session --> User Clicked the Running Config Pre Checks Button")
                        
                        if((len(self.main_application_window.main_window_ui.vendor_selected) > 0) and (self.main_application_window.main_window_ui.vendor_details_selection_combobox.currentText().strip() != 'Select Vendor')):
                            logging.debug("Existing Session --> The user didn't select any vendor")
                            self.warning_messagebox(title="Vendor Not Selected",text="Kindly Select a Vendor!")
                        
                        if(len(self.main_application_window.main_window_ui.running_config_pre_checks_label_text) == 'Successful'):
                            self.information_messagebox(title= "Task Successfully Completed!",text= "Task is already successfully completed!!")
                        
                        else:
                            logging.debug("New Session --> Starting the task")
                            self.running_config_pre_checks_task_method_result = self.running_config_pre_checks_task()
                            
                            if(self.running_config_pre_checks_task_method_result != None):
                                logging.debug("New Session --> Got the result from the method execution of template_checks_task")
                                self.main_application_window.task_method_status_updater(task= 'Running Config Pre Checks',
                                                                                        status = self.running_config_pre_checks_task_method_result)
                                
                                self.database_updater(vendor_selected= self.vendor_selected,
                                                    task_running='Running_Config_Pre_Checks',
                                                    status=self.running_config_pre_checks_task_method_result)
                                
                                self.main_application_window.task_method_status_updater(task='Running_Config_Pre_Checks',
                                                                                        status=self.running_config_pre_checks_task_method_result)
                                
                                self.main_application_window.data = self._database_manager.data_fetcher()
                                self.main_application_window.table_view_data_loader()
                    
                    if(self.main_application_window.main_window_ui.cli_preparation_btn.clicked.connect(self.button_clicked) == "User Clicked"):
                        logging.debug("New Session --> User Clicked the CLI Preparation Checks Button")
                        
                        if((len(self.main_application_window.main_window_ui.vendor_selected) > 0) and (self.main_application_window.main_window_ui.vendor_details_selection_combobox.currentText().strip() != 'Select Vendor')):
                            logging.debug("New Session --> The user didn't select any vendor")
                            self.warning_messagebox(title="Vendor Not Selected",text="Kindly Select a Vendor!")
                        
                        if(len(self.main_application_window.main_window_ui.cli_preparation_status_label_text) == 'Successful'):
                            self.information_messagebox(title= "Task Successfully Completed!",text= "Task is already successfully completed!!")
                        
                        else:
                            logging.debug("New Session --> Starting the task")
                            self.cli_preparation_task_method_result = self.cli_preparation_task()
                            
                            if(self.cli_preparation_task_method_result != None):
                                logging.debug("New Session --> Got the result from the method execution of template_checks_task")
                                self.main_application_window.task_method_status_updater(task= 'CLI Preparation',
                                                                                        status = self.cli_preparation_task_method_result)
                                
                                self.database_updater(vendor_selected= self.vendor_selected,
                                                    task_running='CLI_Preparation',
                                                    status=self.cli_preparation_task_method_result)
                                
                                self.main_application_window.task_method_status_updater(task='CLI_Preparation',
                                                                                        status=self.cli_preparation_task_method_result)
                                
                                self.main_application_window.data = self._database_manager.data_fetcher()
                                self.main_application_window.table_view_data_loader()
                    
                    self.main_application_window.show()
        
        except Exception as e:
            logging.error(f"{traceback.format_exc()}\nException ===> {e}")
            self.critical_messagebox(title= "Exception Occurred!",text= str(e))
            self.quit()
    
    def existing_session(self):
        try:
            self.first_window = App_start_dialog()
            self.first_window.show()
            self.session_selected_by_user = ''
            
            if(self.first_window.app_start_dialog_ui.existing_session_push_button.clicked() == "User Clicked"):
                self.first_window.close()
                self.session_selected_by_user = 'Existing Session'
                
            if(self.first_window.app_start_dialog_ui.new_session_push_button.clicked.connect(self.button_clicked) == "User Clicked"):
                self.first_window.close()
                self.session_selected_by_user = 'New Session'
            
            if(self.session_selected_by_user == 'New Session'):
                self.new_session_surity_check_window = App_new_session_surity_check()
                self.new_session_surity_check_window.show()
                
                if(self.new_session_surity_check_window.app_new_session_surity_check_ui.yes_pushButton.clicked.connect(self.button_clicked) == "User Clicked"):
                    self.new_session_surity_check_window.close()
                    self.new_session()
                
                if(self.new_session_surity_check_window.app_new_session_surity_check_ui.no_pushButton.clicked.connect(self.button_clicked) == "User Clicked"):
                    self.new_session_surity_check_window.close()
                    self.session_selected_by_user = 'Existing Session'
            
            logging.debug("Checking the self.host_details_path to be non-empty")
            
            username = (os.popen('cmd.exe /C "echo %username%"').read()).strip()
            self.host_details_file_path = rf"C:\Users\{username}\AppData\Local\CLI_Automation\Host_details_Pickle_file\Host_details_Path.txt"
            
            if(not os.path.exists(path=self.host_details_path)):
                logging.debug("File path for checking \'Host Details\' file is non-existent, so needed new sesion\n")
                self.warning_messagebox(title="Host Details Not Found", text = "\'Host Details\' file details are not found, So need to create a New Session")
                self.new_session()
            
            if(os.path.exists(path=self.host_details_path)):
                with open(file=self.host_details_file_path, mode='r') as f:
                    self.host_details_path = f.readline().strip()
                    f.close()
            
            if(len(self.host_details_path) == 0):
                logging.debug("File path for checking \'Host Details\' file is empty, so needed new sesion\n")
                
                self.warning_messagebox(title="Host Details Not Found",text = "\'Host Details\' file details are not found, So need to create a New Session")
                
                self.new_session()
                
            if(self.session_selected_by_user == 'Existing Session'):
                self.data = self._database_manager.data_fetcher()
                self.main_application_window = App_Main_Window()
                
                self.data = self._database_manager.data_fetcher()
                self.main_application_window.table_view_data_loader(data=self.data)
                logging.debug(f"Existing Session --> Loading the existing data in the table_view ==>\n{self.data}")
                
                self.main_application_window.main_window_ui.selected_host_details_line_edit.setText(f" Host Details: - {self.host_details_path}")
                
                # Setting the vendor selected to be changed when the user clicks on the combobox
                self.main_application_window.main_window_ui.vendor_details_selection_combobox.activated.connect(self.main_application_window.current_vendor)
                self.vendor_selected = self.main_application_window.vendor_selected
                
                    
                if(self.main_application_window.main_window_ui.new_session_button_3.clicked.connect(self.button_clicked) == "User Clicked"):
                    logging.debug("Existing Session --> User selected to start New Session")
                    self.new_session_surity_check_window = App_new_session_surity_check()
                    self.new_session_surity_check_window.show()
                    
                    if(self.new_session_surity_check_window.app_new_session_surity_check_ui.yes_pushButton.clicked.connect(self.button_clicked) == "User Clicked"):
                        logging.debug("Existing Session --> User Selected Yes in new_session_surity_check_window")
                        self.new_session_surity_check_window.close()
                        self.new_session()
                    
                    if(self.new_session_surity_check_window.app_new_session_surity_check_ui.no_pushButton.clicked.connect(self.button_clicked) == "User Clicked"):
                        logging.debug("Existing Session --> User Selected No in new_session_surity_check_window")
                        self.new_session_surity_check_window.close()
                
                if(self.main_application_window.main_window_ui.template_checks_btn.clicked.connect(self.button_clicked) == "User Clicked"):
                    logging.debug("Existing Session --> User Clicked the Template Checks Button")
                    
                    if((len(self.main_application_window.main_window_ui.vendor_selected) > 0) and (self.main_application_window.main_window_ui.vendor_details_selection_combobox.currentText().strip() != 'Select Vendor')):
                        logging.debug("Existing Session --> The user didn't select any vendor")
                        self.warning_messagebox(title="Vendor Not Selected",text="Kindly Select a Vendor!")
                    
                    
                    if(len(self.main_application_window.main_window_ui.template_checks_label_text) == 'Successful'):
                        self.information_messagebox(title= "Task Successfully Completed!",text= "Task is already successfully completed!!")
                    
                    else:
                        logging.debug("Existing Session --> Starting the task")
                        self.template_checks_task_method_result = self.template_checks_task()
                        
                        if(self.template_checks_task_method_result != None):
                            logging.debug("Existing Session --> Got the result from the method execution of template_checks_task")
                            self.main_application_window.task_method_status_updater(task= 'Template Checks',
                                                                                    status = self.template_checks_task_method_result)
                            
                            self.database_updater(vendor_selected= self.vendor_selected,
                                                  task_running='Template_Checks',
                                                  status=self.template_checks_task_method_result)
                            
                            self.main_application_window.task_method_status_updater(task='Template_Checks',
                                                                                    status=self.template_checks_task_method_result)
                            
                            self.main_application_window.data = self._database_manager.data_fetcher()
                            self.main_application_window.table_view_data_loader()
                
                if(self.main_application_window.main_window_ui.running_config_pre_checks_btn.clicked.connect(self.button_clicked) == "User Clicked"):
                    logging.debug("Existing Session --> User Clicked the Running Config Pre Checks Button")
                    
                    if((len(self.main_application_window.main_window_ui.vendor_selected) > 0) and (self.main_application_window.main_window_ui.vendor_details_selection_combobox.currentText().strip() != 'Select Vendor')):
                        logging.debug("Existing Session --> The user didn't select any vendor")
                        self.warning_messagebox(title="Vendor Not Selected",text="Kindly Select a Vendor!")
                    
                    if(len(self.main_application_window.main_window_ui.running_config_pre_checks_label_text) == 'Successful'):
                        self.information_messagebox(title= "Task Successfully Completed!",text= "Task is already successfully completed!!")
                    
                    else:
                        logging.debug("Existing Session --> Starting the task")
                        self.running_config_pre_checks_task_method_result = self.running_config_pre_checks_task()
                        
                        if(self.running_config_pre_checks_task_method_result != None):
                            logging.debug("Existing Session --> Got the result from the method execution of template_checks_task")
                            self.main_application_window.task_method_status_updater(task= 'Running Config Pre Checks',
                                                                                    status = self.running_config_pre_checks_task_method_result)
                            
                            self.database_updater(vendor_selected= self.vendor_selected,
                                                  task_running='Running_Config_Pre_Checks',
                                                  status=self.running_config_pre_checks_task_method_result)
                            
                            self.main_application_window.task_method_status_updater(task='Running_Config_Pre_Checks',
                                                                                    status=self.running_config_pre_checks_task_method_result)
                            
                            self.main_application_window.data = self._database_manager.data_fetcher()
                            self.main_application_window.table_view_data_loader()
                
                if(self.main_application_window.main_window_ui.cli_preparation_btn.clicked.connect(self.button_clicked) == "User Clicked"):
                    logging.debug("Existing Session --> User Clicked the CLI Preparation Checks Button")
                    
                    if((len(self.main_application_window.main_window_ui.vendor_selected) > 0) and (self.main_application_window.main_window_ui.vendor_details_selection_combobox.currentText().strip() != 'Select Vendor')):
                        logging.debug("Existing Session --> The user didn't select any vendor")
                        self.warning_messagebox(title="Vendor Not Selected",text="Kindly Select a Vendor!")
                    
                    if(len(self.main_application_window.main_window_ui.cli_preparation_status_label_text) == 'Successful'):
                        self.information_messagebox(title= "Task Successfully Completed!",text= "Task is already successfully completed!!")
                    
                    else:
                        logging.debug("Existing Session --> Starting the task")
                        self.cli_preparation_task_method_result = self.cli_preparation_task()
                        
                        if(self.cli_preparation_task_method_result != None):
                            logging.debug("Existing Session --> Got the result from the method execution of template_checks_task")
                            self.main_application_window.task_method_status_updater(task= 'CLI Preparation',
                                                                                    status = self.cli_preparation_task_method_result)
                            
                            self.database_updater(vendor_selected= self.vendor_selected,
                                                  task_running='CLI_Preparation',
                                                  status=self.cli_preparation_task_method_result)
                            
                            self.main_application_window.task_method_status_updater(task='CLI_Preparation',
                                                                                    status=self.cli_preparation_task_method_result)
                            
                            self.main_application_window.data = self._database_manager.data_fetcher()
                            self.main_application_window.table_view_data_loader()
                
                self.main_application_window.show()
        
        except CustomException as e:
            logging.error(f"Custom Exception ==>\n{traceback.format_exc()}\n\nTitle ===> {e.title}\n\nMessage ==> {e.message}")
            self.critical_messagebox(title= e.title,text= e.message)
            self.quit()
        
        except Exception as e:
            logging.error(f"Exception Occured ===>\n{traceback.format_exc()}\n{e}")
            self.critical_messagebox(title= "Exception Occured!",text= str(e))
            self.quit()
    
    def quit(self):
        self.__del__()
    
    def main(self):
        """Main method for running in Application
        """
        self.app = QApplication(sys.argv)
        try:
            
            self.splash_screen_window = Splash_screen()
            self.splash_screen_window.show()
            self.splash_screen_window.counter = 10
            
            
            # self.splash_screen_window.ui.label_3.setText(u"Checking for Existing Session....")
            self.splash_screen_window.progress()
            
            self.pre_main()
            
            i = 10
            while(i < 50):
                self.splash_screen_window.counter = i+10
                time.sleep(1.5)
                self.splash_screen_window.progress()
                i+=10
            
            # self.splash_screen_window.ui.label_3.setText(u"Checking the need for New Session...")
            self.splash_screen_window.progress()
            
            if(not self.new_session_needed):
                i = 50
                while(i <= 90):
                    self.splash_screen_window.counter = i+10
                    time.sleep(1.5)
                    self.splash_screen_window.progress()
                    i+=10
                
                # self.splash_screen_window.ui.label_3.setText("Existing Session Found For User....")
                self.splash_screen_window.progress()
                
                self.splash_screen_window.counter=100
                self.splash_screen_window.progress()
                
                if(self.splash_screen_window.isVisible()):
                    self.splash_screen_window.progress()
                self.existing_session()
            
            if(self.new_session_needed):
                i = 50
                while(i <= 90):
                    self.splash_screen_window.counter = i+10
                    time.sleep(1.5)
                    self.splash_screen_window.progress()
                    i+=10
                
                # self.splash_screen_window.ui.label_3.setText(u"Creating New Session For User....")
                self.splash_screen_window.progress()
                
                self.splash_screen_window.counter=100
                self.splash_screen_window.progress()
                self.splash_screen_window.counter = 110
                self.splash_screen_window.progress()
                
                # Closing the splash_screen if it's still visible
                if(self.splash_screen_window.isVisible()):
                    self.splash_screen_window.close()
                self.new_session()
                
        
        except CustomException as e:
            logging.error(f"{traceback.format_exc()}\n\nTitle ==> {e.title}\n\n{e.message}")
            self.critical_messagebox(title=e.title,text=e.message)
            
        except Exception as e:
            logging.error(f"{traceback.format_exc()}\n\n{e}")
            self.critical_messagebox(title = "Exception Occurred!",text = str(e))
        
        sys.exit(self.app.exec())


if __name__ == '__main__':
    Main_Gui().main()