import os
import sys
import sqlite3
import logging
import pandas as pd
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from Database_manager import Database_manager
from GUI.ui_app_start_dialog_box import Ui_application_start_dialog
from GUI.ui_main_application_first_window import Ui_CLI_automation_main_application_first_window
from GUI.ui_Main_Application_Window import Ui_Main_Application_Window
from GUI.ui_new_session_surity_check import Ui_surity_Dialog
from GUI.ui_splash_screen import Ui_splash_screen

class Main_Gui():
    def __init__(self):
        self.log_file = "C:\\Ericsson_Application_Logs\\CLI_Automation_Logs\\Main_Application.log"
        logging.basicConfig(filename=log_file,
                            filemode="a",
                            format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({'%(module)s'}): {'%(message)s'}",
                            datefmt='%d-%b-%Y %I:%M:%S %p',
                            encoding= "UTF-8",
                            level=logging.DEBUG)
        self.db_path = "C:\\Users\\emaienj\\AppData\\Local\\CLI_Automation\\Database\\CLI_Automation_Database.db"
        
        
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
        if(((datetime.now() - self.db_getctime).days >= 1) or ((dateime.now() - self.db_getctime).seconds//3600 >= 20)):
            logging.debug("Returning false as the database creation time is either greater than 1 day or 20 hours")
            self._database_manager.auto_database_remover()
            return False
        
        else:
            return True
    
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
    
    def new_session(self):
        pass
    
    def existing_session(self):
        pass
    
    def quit(self):
        self.__del__()
    
    def main(self):
        """Main method for running in Application
        """
        self.app = QApplication(sys.argv)
        
        self.pre_main()
        
        if(not self.new_session_needed):
            self.existing_session()
        
        if(self.new_session_needed):
            self.new_session()
            
        
        self.app.exec()


if __name__ == '__main__':
    Main_Gui.main()