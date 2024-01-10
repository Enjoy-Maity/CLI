import os
import sys
import time
import pickle
import sqlite3
import logging
import traceback
import pandas
import openpyxl
from datetime import datetime
from pathlib import Path
from abc import ABC, abstractmethod

# Importing from PySide6
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon, QShortcut, QKeySequence
from PySide6.QtCore import Qt

# Importing the GUI Classes
from Database_manager import Database_manager
from GUI.temp_splash_screen import Splash_screen
from GUI.app_main_application_first_window import App_main_application_first_window
from GUI.app_Main_Window import App_Main_Window
from GUI.app_new_session_surity_check import App_new_session_surity_check
from GUI.app_start_dialog import App_start_dialog
import GUI.Application_GUI_rc
from GUI.database_model import DataModel

# Importing Ui components
from GUI.ui_app_start_dialog_box import Ui_application_start_dialog
from GUI.ui_main_application_first_window import Ui_CLI_automation_main_application_first_window
from GUI.ui_Main_Application import Ui_Main_Application_Window
from GUI.ui_new_session_surity_check import Ui_surity_Dialog

# Importing the custom exception
from Custom_Exception import CustomException


class Abstract_Main_GUI(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def log_file_checker(self):
        pass

    @abstractmethod
    def critical_message(self, title: str, message: str) -> None:
        pass

    @abstractmethod
    def warning_message(self, title: str, message: str) -> None:
        pass

    @abstractmethod
    def information_message(self, title: str, message: str) -> None:
        pass

    @abstractmethod
    def database_checker(self) -> bool:
        pass

    @abstractmethod
    def isdatabase_same_session(self) -> bool:
        pass

    @abstractmethod
    def label_and_database_updater(self, task: str, status: str):
        pass

    @abstractmethod
    def submit_button_method(self):
        pass

    @abstractmethod
    def existing_session_table_loader(self):
        pass

    @abstractmethod
    def sheet_creater_task(self):
        pass

    @abstractmethod
    def template_checks_task(self):
        pass

    @abstractmethod
    def running_config_pre_checks_task(self):
        pass

    @abstractmethod
    def cli_preparation_task(self):
        pass

    @abstractmethod
    def running_config_post_checks_task(self):
        pass

    @abstractmethod
    def pre_run_checks(self):
        pass

    @abstractmethod
    def vendor_list_grabber(self):
        pass

    @abstractmethod
    def vendor_selected(self):
        pass

    @abstractmethod
    def new_session_starter_method(self):
        pass

    @abstractmethod
    def new_session(self):
        pass

    @abstractmethod
    def start_dialog(self):
        pass

    @abstractmethod
    def new_session_surity_checker_method(self):
        pass

    @abstractmethod
    def new_session_surity_check(self):
        pass

    @abstractmethod
    def host_details_pickle_file_checker(self) -> bool:
        pass

    @abstractmethod
    def existing_session(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def new_session_main_window_method(self):
        pass

    @abstractmethod
    def main(self):
        pass


class Main_Gui(Abstract_Main_GUI, ABC):
    def __init__(self):
        self.start_dialog_window = None
        self.app_main_window = None
        self.app = None
        self.splash_screen_window = None
        self.shortcut = None
        self.escape_shortcut = None
        self.dialog_window = None
        self.vendor = None
        self.app_first_window = None
        self.log_file = None
        self.log_file_checker()

        logging.basicConfig(filename=self.log_file,
                            filemode="a",
                            format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({'%(module)s'}/{'%(funcName)s'}): [[Line No. - {'%(lineno)d'}]] {'%(message)s'}",
                            datefmt='%d-%b-%Y %I:%M:%S %p',
                            encoding="UTF-8",
                            level=logging.DEBUG)

        logging.debug("Creating necessary variables")
        # Database Manager class object
        self._database_manager = Database_manager()

        # Checking the database and then removing the database of older period
        if self._database_manager.database_table_checker():
            # Running the auto-remover for removing old data
            self._database_manager.auto_database_remover()

        # Getting the username
        username = (os.popen('cmd.exe /C "echo %username%"').read()).strip()
        # path for database
        self.db_path = f"C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\Database\\CLI_Automation_Database.db"

        # Variable for keeping account of which task is running currently.
        self.task_running = ''

        # Variable for host details
        self.host_details_path = ''

        # Variable for checking the sheet creator task being successfully completed or not
        self.sheet_creater_task_successfully_completed = False

        # Variable for vendor list
        self.vendor_list = []

        # Variable for getting the current user in windows
        self.username = (os.popen(r'cmd.exe /C "echo %username%"').read()).strip()

        # Variable for path existing pickle for data
        self.host_details_pickle_file = f"C:\\Users\\{self.username}\\AppData\\Local\\CLI_Automation\\Host_details_Pickle_file\\Host_details.pkl"

        username = (os.popen(r'cmd.exe /C "echo %username%"').read()).strip()

        # Variable for existing host details path
        self.existing_host_details_file_path = f"C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\host_details_file_path.txt"

    # Method for checking the log file to be auto-removed
    def log_file_checker(self) -> None:
        self.log_file = "C:\\Ericsson_Application_Logs\\CLI_Automation_Logs\\Main_Application.log"

        Path(os.path.dirname(self.log_file)).mkdir(parents=True, exist_ok=True)

        if os.path.exists(self.log_file):
            _log_file_getmtime = datetime.fromtimestamp(os.path.getmtime(self.log_file))

            _log_file_getmtime_timedelta_var = datetime.now() - _log_file_getmtime
            _log_file_getmtime_timedelta_var_hour = int(_log_file_getmtime_timedelta_var.days*24 + (_log_file_getmtime_timedelta_var.seconds//3600))
            _current_hour = int(datetime.now().strftime("%H"))
            if _current_hour > 12:
                if (int(_log_file_getmtime_timedelta_var.days) >= 1) or (_log_file_getmtime_timedelta_var_hour >= 20):
                    os.remove(self.log_file)

                    with open(self.log_file, 'w') as _f:
                        _f.close()

    # Method for raising error messages
    def critical_message(self, title: str, message: str) -> None:
        """Creates Error Messages

        Args:
            title (str): _description_ : Sets the message Title
            message (str): _description_ : Sets the Message Text
        """
        message = str(message)

        _message = QMessageBox()
        _message.setText(message)
        _message.setWindowIcon(QIcon(":/Main_Application_window/ericsson-blue-icon-logo.ico"))
        _message.setWindowTitle(title)
        _message.setIcon(QMessageBox.Icon.Critical)
        _message.setStandardButtons(QMessageBox.StandardButton.Ok)
        _message.setDefaultButton(QMessageBox.StandardButton.Ok)
        # _message.buttonClicked.connect(_message.close)

        _message.exec()

    # Method for raising Warning Messages
    def warning_message(self, title: str, message: str) -> None:
        """Creates Error Messages

        Args:
            title (str): _description_ : Sets the message Title
            message (str): _description_ : Sets the Message Text
        """
        message = str(message)
        _message = QMessageBox()
        _message.setText(str(message))
        _message.setWindowIcon(QIcon(":/Main_Application_window/ericsson-blue-icon-logo.ico"))
        _message.setWindowTitle(title)
        _message.setIcon(QMessageBox.Icon.Warning)
        _message.setStandardButtons(QMessageBox.StandardButton.Ok)
        _message.setDefaultButton(QMessageBox.StandardButton.Ok)
        # _message.buttonClicked.connect(_message.close)

        _message.exec()

    # Method for raising information messages
    def information_message(self, title: str, message: str) -> None:
        """Creates Error Messages

        Args:
            title (str): _description_ : Sets the message Title
            message (str): _description_ : Sets the Message Text
        """
        message = str(message)
        _message = QMessageBox()
        _message.setText(str(message))
        _message.setWindowIcon(QIcon(":/Main_Application_window/ericsson-blue-icon-logo.ico"))
        _message.setWindowTitle(title)
        _message.setIcon(QMessageBox.Icon.Information)
        _message.setStandardButtons(QMessageBox.StandardButton.Ok)
        _message.setDefaultButton(QMessageBox.StandardButton.Ok)
        # _message.buttonClicked.connect(_message.close)

        _message.exec()

    # Method for checking the database
    def database_checker(self) -> bool:
        """Checking of the database exists or not or needs to be auto removed to be created again

        Returns:
            database_exists(bool): _description_ : boolean result
        """

        _database_exists = False

        _db_file_existence = os.path.exists(path=self.db_path)
        if not _db_file_existence:
            self._database_manager.table_creater()
            logging.debug("Created the Database")

        if _db_file_existence:
            logging.debug("Database Found")
            _database_exists = True

        return _database_exists

    # Method for checking if database is of same session
    def isdatabase_same_session(self) -> bool:
        """Checks for the existing database and getting the mtime to get the timedelta() to check for day >=1 or hours >= 20
           and getting the bool result

        Returns:
            bool: _description_ : Boolean result in True/False
        """

        _db_getmtime = datetime.fromtimestamp(os.path.getmtime(filename=self.db_path))
        _timedelta_var = datetime.now()-_db_getmtime
        _timedelta_var_hour = (_timedelta_var.days*24 + _timedelta_var.seconds)//3600
        logging.debug(f"db getmtime =>{_timedelta_var =}\n\
                        {_timedelta_var_hour = } Hours\n")

        if (int(_timedelta_var.days) >= 1) or (int(_timedelta_var_hour) >= 20):
            logging.debug(
                f"Returning false as the database modified time is either greater than 1 day or 20 hours => \n" +
                f"{_db_getmtime = }\n\
                           {_timedelta_var_hour} hour and \n\
                            {_timedelta_var.days = }days\n")
            self._database_manager.auto_database_remover()
            return False

        else:
            return True

    # Method for updating the labels and updating the database to be loaded
    def label_and_database_updater(self, task: str, status: str) -> None:
        """Updates the label and database

        Args:
            task (str): _description_ : task for which the status needs to be updated
            status (str): _description_ : status which needed to be put
        """
        try:
            # If the parent is App_main_application_first_window, then taking steps accordingly.
            if task == 'Sheet Creater':
                logging.debug(f"Setting Sheet Creater task status -> {status}")
                self.app_first_window.task_method_status_updater(status=status)

            # If the parent is App_Main_Window, then taking steps accordingly.
            if task == 'Template Checks':
                logging.debug(f"Setting Template Checks task status -> {status}")
                self.app_main_window.task_method_status_updater(task='Template Checks',
                                                                status=status)

                if status != "In Progress":
                    logging.info(
                        f"Updating the database for {self.vendor_selected()} for \n\ttask =>{task}\n\t\twith status => {status}")
                    self._database_manager.database_updater(vendor=self.vendor_selected(),
                                                            task='Template_Checks',
                                                            status=status)

                logging.info("Reloading the database")
                self.app_main_window.table_view_data_loader(data=self._database_manager.data_fetcher())

            if task == 'Running Config Pre Checks':
                logging.debug(f"Setting Running Config Pre Checks task status -> {status}")
                self.app_main_window.task_method_status_updater(task='Running Config Pre Checks',
                                                                status=status)

                if status != "In Progress":
                    logging.info(
                        f"Updating the database for {self.vendor_selected()} for \n\ttask =>{task}\n\t\twith status => {status}")
                    self._database_manager.database_updater(vendor=self.vendor_selected(),
                                                            task='Running_Config_Pre_Checks',
                                                            status=status)

                logging.info("Reloading the database")
                self.app_main_window.table_view_data_loader(data=self._database_manager.data_fetcher())

            if task == 'CLI Preparation':
                logging.debug(f"Setting CLI Preparation task status -> {status}")
                self.app_main_window.task_method_status_updater(task='CLI Preparation',
                                                                status=status)

                if status != "In Progress":
                    logging.info(
                        f"Updating the database for {self.vendor_selected()} for \n\ttask =>{task}\n\t\twith status => {status}")
                    self._database_manager.database_updater(vendor=self.vendor_selected(),
                                                            task='CLI_Preparation',
                                                            status=status)

                logging.info("Reloading the database")
                self.app_main_window.table_view_data_loader(data=self._database_manager.data_fetcher())

        except Exception as e:
            logging.error(f"{traceback.format_exc()}\n\tException Occurred!\n\t\t{e}")
            self.critical_message(title="Exception Occurred!",
                                  message=str(e))

    # Method for submit button of first window
    def submit_button_method(self):
        self.host_details_path = self.app_first_window.host_details_file
        print(self.host_details_path)
        if not self.host_details_path.strip().endswith(".xlsx"):
            logging.error(
                f"raised QMessageBox critical message title= Host Details Not Selected!,\nhost_details = {self.host_details_path}")

            self.critical_message(title="Host Details Not Selected!",
                                  message="Kindly Select the Host Details file via \'Browse\' Button")
            return None

        if len(self.app_first_window.ui.sheet_creator_status_label.text()) == 0:
            logging.error(f"raised QMessageBox critical message title= Sheet Creater Task Not Completed!")

            self.critical_message(title="Sheet Creater Task Not Completed!",
                                  message="Kindly! Complete the Sheet Creater task successfully via \'Sheet Creater\' Button")
            return None

        if self.app_first_window.ui.sheet_creator_status_label.text() != "Successful":
            logging.error(f"raised QMessageBox critical message title= Sheet Creator Task Not Successfully Completed!")

            self.critical_message(title="Sheet Creator Task Not Successfully Completed!",
                                  message="Kindly! Complete the Sheet Creater task successfully first and then click " +
                                          "on \'Submit\' Button")
            return None

        else:
            if self.host_details_path.strip().endswith(".xlsx"):
                _file_reader = pandas.ExcelFile(path_or_buffer=self.host_details_path,
                                                engine='openpyxl')
                _excel_file = pandas.read_excel(_file_reader,
                                                sheet_name="Host Details")

                _file_reader.close()
                del _file_reader

                if len(_excel_file) == 0:
                    self.critical_message(title="Empty Host File Uploaded!",
                                          message="The uploaded host details file do not contain any data! Kindly " +
                                                  "Check!")
                    return None

                else:
                    logging.info(f"Calling the vendor list grabber along with data -->\n {_excel_file.to_markdown()}")
                    self.vendor_list_grabber(data=_excel_file)

                    if len(self.vendor_list) == 0:
                        self.critical_message(title="Empty Vendor List!",
                                              message="Kindly Check the uploaded Host Details, there's no vendor " +
                                                      "present in the uploaded \'Host Details\'")

                        return None

                    else:
                        self.app_first_window.close()
                        self._database_manager.data_adder(vendor_list=self.vendor_list)
                        self.new_session_main_window_method()

    # Method for loading existing session database 
    def existing_session_table_loader(self):
        """Loads the Table for existing session
        """
        _data = self._database_manager.data_fetcher()
        if ((self.app_main_window.isVisible()) or (
                (self.app_main_window.isHidden()) or (self.app_main_window.isActiveWindow()))):
            self.app_main_window.data = _data
            self.app_main_window.table_view_data_loader(data=_data)

    # Method for Sheet Creator Task
    def sheet_creater_task(self) -> None:
        if self.task_running == '':
            _sheet_creator_task_status = ''

            logging.debug("Setting the Task_Running variable to \'Sheet Creater\'")
            self.task_running = 'Sheet Creater'

            logging.debug(f"Setting the status of the Sheet Creater Task Label to \'In Progress\'")
            self.label_and_database_updater(task='Sheet Creater',
                                            status="In Progress")
            try:
                self.host_details_path = self.app_first_window.host_details_file
                if len(self.app_first_window.host_details_file) == 0:
                    logging.debug("Raising Error Message as there is no path given in the self.host_details_path")
                    self.critical_message(title="Host Details File Not Selected!",
                                          message="Kindly select the \'Host Details\' file first and then try again!")
                    _sheet_creator_task_status = "Unsuccessful"

                else:
                    from Sheet_creater import main_func
                    _sheet_creator_task_status = main_func(file_name=self.app_first_window.host_details_file)

                    logging.debug(f"Got the Status for Sheet Creater task as {_sheet_creator_task_status} ")

            except PermissionError as e:
                logging.error(f"{traceback.format_exc()}\nTitle --> Exception Occurred!\nMessage --> {e}\n")
                _sheet_creator_task_status = 'Unsuccessful'

            except Exception as e:
                logging.error(f"{traceback.format_exc()}\nTitle --> Exception Occurred!\nMessage --> {e}\n")
                _sheet_creator_task_status = 'Unsuccessful'

            finally:
                self.task_running = ''
                self.label_and_database_updater(task='Sheet Creater',
                                                status=_sheet_creator_task_status)

        else:
            self.warning_message(title="Task Already Running!",
                                 message=f"{self.task_running} is already running! Please Wait for the completion of "
                                         f"task execution!")

    # Method for Template Checks Task
    def template_checks_task(self) -> None:
        if self.task_running == '':
            _template_checks_task_status = self.app_main_window.main_window_ui.template_checks_label.text()

            if _template_checks_task_status == 'Successful':
                logging.debug(
                    f"User clicked on the Template Checks Button even though it was successfully completed for {self.app_main_window.current_vendor('')}"
                )
                self.warning_message(title="Task Already Successfully Completed!",
                                     message="Template Checks Task is already successfully completed!")
            else:
                _template_checks_task_status = ''
                logging.debug("Setting the template task status to In Progress")
                self.label_and_database_updater(task="Template Checks",
                                                status="In Progress")
                try:
                    _username = (os.popen(cmd=r'cmd.exe /C "echo %username%"').read()).strip()

                    _app_data_local_saved_host_details_path = f"C:\\Users\\{_username}\\AppData\\Local\\CLI_Automation\\host_details_file_path.txt"
                    _filename = ''

                    logging.debug(f"Got the path for _app_data_local_saved_host_details_path=>\n\t{_app_data_local_saved_host_details_path}")
                    if not os.path.exists(_app_data_local_saved_host_details_path):
                        logging.debug(f"{os.path.exists(_app_data_local_saved_host_details_path)= }")
                        logging.debug("Raising exception as the file for _app_data_local_saved_host_details_path not found")
                        raise CustomException("File Not Found",
                                              "File for the selected host details not found kindly start the new session to start over!")

                    with open(file=_app_data_local_saved_host_details_path, mode="r") as _f:
                        logging.debug("Reading the file to get the file path")
                        _filename = _f.readline()
                        _f.close()

                    del _f

                    from Template_checks import main_func
                    _template_checks_task_status = main_func(filename=_filename.strip(),
                                                             vendor_selected=self.vendor_selected())

                    if _template_checks_task_status == 'Successful':
                        self.information_message(title="Task Successfully Completed!",
                                                 message=f" Template Checks Task successfully completed {self.vendor_selected()}")

                except CustomException as e:
                    logging.error(f"Raised CustomException =>\n\tTitle ==> {e.title}\n\tMessage ==> {e.message}")
                    _template_checks_task_status = 'Unsuccessful'

                except FileNotFoundError as e:
                    logging.error(f"{traceback.format_exc()}\nTitle --> File Not Found")
                    self.critical_message(title="FileNotFound Error!", message=str(e))
                    _template_checks_task_status = 'Unsuccessful'

                except Exception as e:
                    logging.error(f"{traceback.format_exc()}\nTitle --> Exception Occurred!\nMessage --> {e}\n")
                    self.critical_message(title="Exception Occurred!", message=str(e))
                    _template_checks_task_status = 'Unsuccessful'

                finally:
                    self.label_and_database_updater(task='Template Checks',
                                                    status=_template_checks_task_status)

        else:
            self.warning_message(title="Task Already Running!",
                                 message=f"{self.task_running} is already running! Please Wait for the completion of "
                                         f"task execution!")

    # Method for Running Config Pre Checks Task
    def running_config_pre_checks_task(self) -> None:
        if self.task_running == '':
            _running_config_pre_checks_task = ''

            try:
                from Running_Config_Checks import running_config_checks
                _running_config_pre_checks_task = running_config_checks(vendor_selected=self.vendor_selected())

            except Exception as e:
                logging.debug(f"{traceback.format_exc()}\nTitle --> Exception Occurred!\nMessage --> {e}\n")
                self.critical_message(title="Exception Occurred!",
                                      message=str(e))
                _running_config_pre_checks_task = 'Unsuccessful'

            finally:
                logging.debug(
                    f"Got the running_config_pre_checks task status as {_running_config_pre_checks_task} for vendor {self.vendor_selected()}"
                )
                self.label_and_database_updater(task='Running Config Pre Checks',
                                                status=_running_config_pre_checks_task)

        else:
            self.warning_message(title="Task Already Running!",
                                 message=f"{self.task_running} is already running! Please Wait for the completion of task execution!")

    # Method for CLI Preparation
    def cli_preparation_task(self) -> None:
        if self.task_running == '':
            self.vendor = self.app_main_window.current_vendor("")
            if ((isinstance(self.vendor, str)) and (len(self.vendor) > 0)) and (self.vendor.strip() != 'Select Vendor'):
                _cli_preparation_task_status = ''

                try:
                    if self.vendor is not None:
                        pass
                    else:
                        from .CLI_preparation import main_func
                        _cli_preparation_task_status = main_func(file_name=self.app_first_window)

                except Exception as e:
                    logging.debug(f"{traceback.format_exc()}\nTitle --> Exception Occurred!\nMessage --> {e}\n")
                    _cli_preparation_task_status = 'Unsuccessful'

                finally:
                    logging.debug(f"Updating the label for vendor() _cli_preparation_status ==> ")
                    self.label_and_database_updater(task='CLI Preparation',
                                                    status=_cli_preparation_task_status)

            else:
                self.critical_message(title="")

        else:
            self.warning_message(title="Task Already Running!",
                                 message=f"{self.task_running} is already running! Please Wait for the completion of task execution!")

    # Method for Running Config Post Checks Task
    def running_config_post_checks_task(self):
        pass

    # Method for pre-session checks
    def pre_run_checks(self) -> str:
        """Performs the task necessary before starting the application.
        """
        _result = self.database_checker()

        if not _result:
            logging.debug("Inside ->temp_Main_Gui.Main_Gui.pre_run_checks, returning new session needed")
            return "new session needed"

        if _result:
            logging.debug(
                f"Got the result for existence of database as \'{_result}\' now checking for the is the database is "
                f"for the same session or not")
            _database_session_result = self.isdatabase_same_session()

            if not _database_session_result:
                logging.debug(
                    f"Inside -> Main_Gui.Main_Gui.pre-main, Setting the self.new_session_needed to True after getting "
                    f"self.database_session_result as {_database_session_result}")
                return "new session needed"

            if _database_session_result:
                logging.info("Checking if there is any data present inside the database\n")
                if len(self._database_manager.data_fetcher()) == 0:
                    return "new session needed"

                else:
                    logging.debug(
                        f"Inside -> Main_Gui.Main_Gui.pre-main, Setting the self.new_session_needed to True after "
                        f"getting database_session_result as \'{_database_session_result}\'")
                    return "existing session detected"

    # Method for getting the list of vendor list
    def vendor_list_grabber(self, data: pandas.DataFrame) -> list:
        """returns the list with unique vendors 

        Args:
            data (pandas.DataFrame): _description_ : dataframe containing the details for vendors

        Returns:
            vendor_list(list): _description_ : list containing the unique list of vendors
        """

        self.vendor_list = list(data['Vendor'].dropna().unique())

        return self.vendor_list

    # Method for setting Vendor
    def vendor_selected(self) -> str:
        """Returns the current vendor selected

        Returns:
            vendor(str): _description_ : vendor selected by the user
        """
        self.vendor = self.app_main_window.main_window_ui.vendor_details_selection_combobox.currentText()
        return self.vendor

    # Method for Handling New Session startups
    def new_session_starter_method(self):
        logging.info("Resetting all the required variables for new session")
        self.sheet_creater_task_successfully_completed = False
        self.host_details_path = ''
        self.vendor_list = []
        self._database_manager.auto_database_remover()
        self._database_manager.data_remover()

    # Method for Handling New Session
    def new_session(self):
        logging.debug("Creating object of App_main_application_first_window")
        self.app_first_window = App_main_application_first_window()
        self.app_first_window.show()

        # print("Hello")

        self.app_first_window.ui.file_browser_pushButton.clicked.connect(self.app_first_window.file_browser)

        self.app_first_window.ui.sheet_creator_pushButton.clicked.connect(self.sheet_creater_task)

        self.app_first_window.ui.submit_button_pushButton.clicked.connect(self.submit_button_method)

    # Method for creating start dialog
    def start_dialog(self):
        """Creates the start dialog to get the response from the User, whether he wants to continue with existing session or start new session
        """
        self.start_dialog_window = App_start_dialog()
        # self.dialog_window.show()
        self.start_dialog_window.user_response = ""

        self.start_dialog_window.ui.existing_session_push_button.clicked.connect(
            self.start_dialog_window.existing_session)
        self.start_dialog_window.ui.new_session_push_button.clicked.connect(self.start_dialog_window.new_session)

        self.start_dialog_window.exec()

        if self.start_dialog_window.user_response == "Existing Session":
            # self.start_dialog_window.close()
            return "Existing Session"

        if self.start_dialog_window.user_response == "New Session":
            # self.start_dialog_window.close()
            return "New Session"

        else:
            # self.start_dialog_window.close()
            return "Existing Session"

    # Method for checking new session need checker 
    def new_session_surity_checker_method(self):
        if self.app_main_window.isVisible():
            # Hiding the app_main_window
            logging.debug("Hiding the Main Application Window")
            self.app_main_window.hide()

        self.new_session_surity_check()

        if self.dialog_window.user_button_clicked == "Yes":
            self.dialog_window.close()

            logging.debug("User wants New Session")
            self.app_main_window.close()
            self.new_session_starter_method()
            self.new_session()

        else:
            self.dialog_window.close()
            self.app_main_window.show()

    # Method for checking for surity for new session
    def new_session_surity_check(self):
        """Creates the new session dialog to get the response from the User for surity to create new session
        """
        # logging.debug("Starting the database_manager.data_remover()")
        # self._database_manager.data_remover()

        self.dialog_window = App_new_session_surity_check()
        self.dialog_window.user_button_clicked = ''
        # self.dialog_window.show()

        self.dialog_window.app_new_session_surity_check_ui.yes_pushButton.clicked.connect(
            self.dialog_window.yes_button_clicked)
        self.dialog_window.app_new_session_surity_check_ui.no_pushButton.clicked.connect(
            self.dialog_window.no_button_clicked)
        self.dialog_window.exec()

    # Method for checking the host_files pickle
    def host_details_pickle_file_checker(self) -> bool:
        if os.path.exists(self.host_details_pickle_file):
            # _host_details_pickle_getctime = datetime.fromtimestamp(os.path.getctime(self.host_details_pickle_file))

            # if((int((datetime.now() - _host_details_pickle_getctime).days) > 1) or (int((datetime.now() - 
            # _host_details_pickle_getctime).seconds//3600) >= 20)): return False

            _host_details_pickle_getmtime = datetime.fromtimestamp(os.path.getmtime(self.host_details_pickle_file))
            _timedelta_var = datetime.now() - _host_details_pickle_getmtime
            _timedelta_var_hour = (_timedelta_var.days*24 + _timedelta_var.seconds)//3600
            if (int(_timedelta_var.days) >= 1) or (_timedelta_var_hour >= 20):
                return False

            else:
                return True

    # Method for Handling Existing Session
    def existing_session(self):
        # Creating the dialog for asking if the user wants to continue with existing session or wants new session
        logging.debug(
            "Calling the dialog for asking if the user wants to continue with existing session or wants new session")

        _result = self.start_dialog()

        if _result == "New Session":
            self.new_session_surity_check()

            # if(_new_result == "Yes"):
            #     self.new_session_starter_method()
            #     self.new_session()

            if self.dialog_window.user_button_clicked == "Yes":
                self.dialog_window.close()
                self.new_session_starter_method()
                self.new_session()

            else:
                self.dialog_window.close()
                if not self.host_details_pickle_file_checker():
                    logging.debug("Existing Session Host Details pickle not detected so creating \'New Session\'")
                    self.critical_message(title="Host Details Pickle Not Found!",
                                          message="Existing Session Host Details pickle not detected so creating "
                                                  "\'New Session\'")

                    self.new_session_starter_method()
                    self.new_session()

                else:

                    logging.info("Reading the pickle file")
                    with open(file=self.host_details_pickle_file, mode='rb') as _f:
                        _file = pickle.load(file=_f, encoding='UTF-8')
                        _f.close()

                    del _f

                    logging.info("Calling the combobox_data_items_adder to add the vendor list")
                    self.vendor_list_grabber(data=_file)

                    if len(self.vendor_list) == 0:
                        self.critical_message(title="Vendor List Empty",
                                              message="Vendor list is found empty! New Session is required")

                        self.new_session_starter_method()
                        self.new_session()

                    logging.info("Checking for the existing host details file path")
                    if not Path(self.existing_host_details_file_path).exists():
                        logging.error("Raising error message => \'Existing Host Details File Path Not Found!\'")
                        self.critical_message(title="Existing Host Details File Path Not Found!",
                                              message="Existing Host Details File Path Not Found so need New Session!")

                        self.new_session_starter_method()
                        self.new_session()

                    _line_containing_file_path = ''

                    if Path(self.existing_host_details_file_path).exists():
                        with open(self.existing_host_details_file_path, 'r') as _f:
                            _line_containing_file_path = _f.readline()
                            _f.close()

                        del _f

                        if len(_line_containing_file_path) == 0:
                            logging.error("Raising error message => \'Existing Host Details File Path Not Found!\'")
                            self.critical_message(title="Existing Host Details File Path Not Found!",
                                                  message="Existing Host Details File Path Not Found so need New "
                                                          "Session!")

                            self.new_session_starter_method()
                            self.new_session()

                        else:
                            self.app_main_window = App_Main_Window()

                            # Clearing the Combobox
                            self.app_main_window.combobox_clearer()

                            self.app_main_window.combobox_data_items_adder(vendor_list=self.vendor_list)

                            self.existing_session_table_loader()

                            # Showing data to the Database Table
                            self.app_main_window.table_view_data_loader(self._database_manager.data_fetcher())

                            # Creating connection for vendor detail selection
                            self.app_main_window.main_window_ui.vendor_details_selection_combobox.activated.connect(
                                self.vendor_selected)

                            # Creating connection for template checks task
                            self.app_main_window.main_window_ui.template_checks_btn.clicked.connect(
                                self.template_checks_task)

                            # Creating connection for running config pre checks task
                            self.app_main_window.main_window_ui.running_config_pre_checks_btn.clicked.connect(
                                self.running_config_pre_checks_task)

                            # Creating connection for cli preparation task
                            self.app_main_window.main_window_ui.cli_preparation_btn.clicked.connect(
                                self.cli_preparation_task)

                            # Creating connection for new session button
                            self.app_main_window.main_window_ui.new_session_button_3.clicked.connect(
                                self.new_session_surity_checker_method)

                            # Setting the sheet creater task label 'Successful'
                            self.app_main_window.main_window_ui.sheet_creater_task_status_label.setText("Successful")
                            self.app_main_window.main_window_ui.sheet_creater_task_status_label.setStyleSheet(
                                "#sheet_creater_task_status_label{\n"
                                "color: rgb(0,255,0);\n"
                                "text-align:center;\n"
                                "font: 700 14pt 'Ericsson Hilda';\n"
                                "}")

                            self.app_main_window.main_window_ui.vendor_details_selection_combobox.currentTextChanged.connect(
                                self.task_status_label_refresher)
                            self.app_main_window.main_window_ui.selected_host_details_line_edit.setText(
                                f" {_line_containing_file_path} ")

                            logging.debug("Existing Session --> Created the Main Application Window")
                            self.app_main_window.show()

        else:
            if not self.host_details_pickle_file_checker():
                logging.debug("Existing Session Host Details pickle not detected so creating \'New Session\'")
                self.critical_message(title="Host Details Pickle Not Found!",
                                      message="Existing Session Host Details pickle not detected so creating \'New "
                                              "Session\'")

                self.new_session_starter_method()
                self.new_session()

            else:
                logging.info("Reading the pickle file")
                with open(file=self.host_details_pickle_file, mode='rb') as _f:
                    _file = pickle.load(file=_f, encoding='UTF-8')
                    _f.close()

                del _f

                logging.info("Calling the combobox_data_items_adder to add the vendor list")
                self.vendor_list_grabber(data=_file)

                if len(self.vendor_list) == 0:
                    self.critical_message(title="Vendor List Empty",
                                          message="Vendor list is found empty! New Session is required")

                    self.new_session_starter_method()
                    self.new_session()

                logging.info("Checking for the existing host details file path")
                if not Path(self.existing_host_details_file_path).exists():
                    logging.error("Raising error message => \'Existing Host Details File Path Not Found!\'")
                    self.critical_message(title="Existing Host Details File Path Not Found!",
                                          message="Existing Host Details File Path Not Found so need New Session!")

                    self.new_session_starter_method()
                    self.new_session()

                _line_containing_file_path = ''

                if Path(self.existing_host_details_file_path).exists():
                    with open(self.existing_host_details_file_path, 'r') as _f:
                        _line_containing_file_path = _f.readline()
                        _f.close()

                    del _f

                    if len(_line_containing_file_path) == 0:
                        logging.error("Raising error message => \'Existing Host Details File Path Not Found!\'")
                        self.critical_message(title="Existing Host Details File Path Not Found!",
                                              message="Existing Host Details File Path Not Found so need New Session!")

                        self.new_session_starter_method()
                        self.new_session()

                    else:
                        self.app_main_window = App_Main_Window()

                        # Clearing the Combobox
                        self.app_main_window.combobox_clearer()

                        self.app_main_window.combobox_data_items_adder(vendor_list=self.vendor_list)

                        self.existing_session_table_loader()

                        # Showing data to the Database Table
                        self.app_main_window.table_view_data_loader(self._database_manager.data_fetcher())

                        # Creating connection for vendor detail selection
                        self.app_main_window.main_window_ui.vendor_details_selection_combobox.activated.connect(
                            self.vendor_selected)

                        # Creating connection for template checks task
                        self.app_main_window.main_window_ui.template_checks_btn.clicked.connect(
                            self.template_checks_task)

                        # Creating connection for running config pre checks task
                        self.app_main_window.main_window_ui.running_config_pre_checks_btn.clicked.connect(
                            self.running_config_pre_checks_task)

                        # Creating connection for cli preparation task
                        self.app_main_window.main_window_ui.cli_preparation_btn.clicked.connect(
                            self.cli_preparation_task)

                        # Creating connection for new session button
                        self.app_main_window.main_window_ui.new_session_button_3.clicked.connect(
                            self.new_session_surity_checker_method)

                        # Setting the sheet creater task label 'Successful'
                        self.app_main_window.main_window_ui.sheet_creater_task_status_label.setText("Successful")
                        self.app_main_window.main_window_ui.sheet_creater_task_status_label.setStyleSheet(
                            u"#sheet_creater_task_status_label{\n"
                            "color: rgb(0,255,0);\n"
                            "text-align:center;\n"
                            "font: 700 14pt 'Ericsson Hilda';\n"
                            "}")

                        self.app_main_window.main_window_ui.vendor_details_selection_combobox.currentTextChanged.connect(
                            self.task_status_label_refresher)
                        self.app_main_window.main_window_ui.selected_host_details_line_edit.setText(
                            f" {_line_containing_file_path} ")
                        logging.debug("Existing Session --> Created the Main Application Window")
                        self.app_main_window.show()

    # Method for quitting
    def exit(self):
        logging.info("Exiting the app")
        logging.shutdown()
        sys.exit()

    # Method for refreshing the labels for all the task status labels
    def task_status_label_refresher(self) -> None:
        if self.app_main_window.isVisible():
            _combobox_current_text = self.app_main_window.main_window_ui.vendor_details_selection_combobox.currentText()

            _combobox_current_text = _combobox_current_text.strip()

            logging.debug(
                f"Took the current combobox text ==> \n\t{_combobox_current_text}\n"
            )

            if (len(_combobox_current_text) > 0) and (_combobox_current_text != 'Select Vendor'):
                _vendor = self.app_main_window.main_window_ui.vendor_details_selection_combobox.currentText().strip()

                logging.info(f"User changed the selected vendor to {_vendor}")

                _data = self._database_manager.data_fetcher()
                logging.info(f"Got the raw data from the database \n{_data.to_markdown()}")

                if len(_data) > 0:

                    _data = _data[_data['Vendor'] == _vendor]
                    _data = _data.where(~_data.isna(), 'TempNA')

                    logging.info(f"Got the filtered data \n{_data.to_markdown()}")

                    if str(_data.iloc[0, _data.columns.get_loc('Template_Checks')]) != 'TempNA':
                        _value = str(_data.iloc[0, _data.columns.get_loc('Template_Checks')])
                        # self.app_main_window.main_window_ui.template_checks_label.setText(_value)
                        self.app_main_window.task_method_status_updater(task="Template Checks",
                                                                        status=_value)

                        logging.info(f"template_checks_label Text is set to \'{_value}\' for vendor \'{_vendor}\'")

                    if str(_data.iloc[0, _data.columns.get_loc('Running_Config_Pre_Checks')]) != 'TempNA':
                        _value = str(_data.iloc[0, _data.columns.get_loc('Running_Config_Pre_Checks')])
                        # self.app_main_window.main_window_ui.running_config_pre_checks_label.setText(_value)
                        self.app_main_window.task_method_status_updater(task="Running Config Pre Checks",
                                                                        status=_value)

                        logging.info(
                            f"running_config_pre_checks_label Text is set to \'{_value}\' for vendor \'{_vendor}\'")

                    if str(_data.iloc[0, _data.columns.get_loc('CLI_Preparation')]) != 'TempNA':
                        _value = str(_data.iloc[0, _data.columns.get_loc('CLI_Preparation')])
                        # self.app_main_window.main_window_ui.cli_preparation_status_label.setText(_value)
                        self.app_main_window.task_method_status_updater(task="CLI Preparation ",
                                                                        status=_value)

                        logging.info(f"cli_preparation_status_label Text is set to \'{_value}\' for vendor \'{_vendor}\'")

                else:
                    self.critical_message(title="Data not Found",
                                          message="Kindly Start a New Session as Data for the current selected Vendor is not found!")

    # Method for calling Main window from the new session
    def new_session_main_window_method(self):
        logging.info("New Session --> Closing the app first window")
        self.app_first_window.close()

        self.app_main_window = App_Main_Window()

        # Cleaning the combobox
        self.app_main_window.combobox_clearer()

        logging.info("New Session --> Adding the vendor list in the combobox")
        # Setting the vendor list in the main window vendor selection combobox
        self.app_main_window.combobox_data_items_adder(self.vendor_list)

        # Showing data to the Database Table
        self.app_main_window.table_view_data_loader(self._database_manager.data_fetcher())

        # Creating connection for vendor detail selection
        self.app_main_window.main_window_ui.vendor_details_selection_combobox.activated.connect(self.vendor_selected)

        # Creating connection for refreshing the button status labels
        self.app_main_window.main_window_ui.vendor_details_selection_combobox.currentTextChanged.connect(
            self.task_status_label_refresher)

        # Creating connection for template checks task
        self.app_main_window.main_window_ui.template_checks_btn.clicked.connect(self.template_checks_task)

        # Creating connection for running config pre-checks task
        self.app_main_window.main_window_ui.running_config_pre_checks_btn.clicked.connect(
            self.running_config_pre_checks_task)

        # Creating connection for cli preparation task
        self.app_main_window.main_window_ui.cli_preparation_btn.clicked.connect(self.cli_preparation_task)

        # Creating connection for new session button
        self.app_main_window.main_window_ui.new_session_button_3.clicked.connect(self.new_session_surity_checker_method)

        # Setting the sheet creater task label 'Successful'
        self.app_main_window.main_window_ui.sheet_creater_task_status_label.setText("Successful")
        self.app_main_window.main_window_ui.sheet_creater_task_status_label.setStyleSheet(
            "#sheet_creater_task_status_label{\n"
            "color: rgb(0,255,0);\n"
            "text-align:center;\n"
            "font: 700 14pt 'Ericsson Hilda';\n"
            "}")

        self.app_main_window.main_window_ui.selected_host_details_line_edit.setText(f" {self.host_details_path}")

        # Setting the shortcut for closing the app
        _shortcut = QShortcut(QKeySequence("Alt+F4"), self.app_main_window)
        _shortcut.activated.connect(self.exit)

        _escape_shortcut = QShortcut(QKeySequence("Esc"), self.app_main_window)
        _escape_shortcut.activated.connect(self.exit)

        logging.debug("New Session --> Created the Main Application Window")
        self.app_main_window.show()

    # Main Method
    def main(self):
        self.app = QApplication(sys.argv)
        self.splash_screen_window = Splash_screen()

        self.shortcut = QShortcut(QKeySequence("Alt+F4"), self.app)

        self.shortcut.setContext(Qt.ApplicationShortcut)
        self.shortcut.activated.connect(self.exit)

        self.escape_shortcut = QShortcut(QKeySequence("Esc"), self.app)
        self.escape_shortcut.activated.connect(self.exit)

        self.splash_screen_window.show()

        self.splash_screen_window.message(counter=5, label_text="Running Pre Session Checks ....")
        result = self.pre_run_checks()

        i = 10
        while i <= 40:
            time.sleep(0.6)
            self.splash_screen_window.message(counter=i, label_text="Running Pre Session Checks ....")
            i += 5

        self.splash_screen_window.message(counter=45, label_text="Completed Pre Session Checks ....")
        time.sleep(0.4)
        self.splash_screen_window.message(counter=60, label_text="Completed Pre Session Checks ....")

        # Got the result for new session
        if result == "new session needed":
            logging.debug(f"Got the result that we will need a new session")

            i = 65
            while i <= 100:
                time.sleep(0.6)
                self.splash_screen_window.message(counter=i, label_text="Creating a New Session ....")
                i += 5

            # Closing the splash screen
            self.splash_screen_window.finish_()

            logging.debug("Running the new session starter method to clean all the necessary variables for new session")
            self.new_session_starter_method()

            logging.debug("Loading the new session")
            self.new_session()

        # Got the result as existing session detected
        if result == "existing session detected":
            logging.debug("Got the result as existing session is detected!")
            print("Hello")
            i = 65
            while i <= 100:
                time.sleep(0.4)
                self.splash_screen_window.message(counter=i, label_text="Loading Existing Session ....")
                i += 5

            logging.debug("Closing the splash screen to load the existing session\n")
            # Closing the splash screen
            self.splash_screen_window.finish_()
            self.existing_session()

        # i = 65
        # while(i <= 100):
        #     time.sleep(0.6)
        #     self.splash_screen_window.message(counter=i,label_text=f"{i}")
        #     i+=5
        # self.splash_screen_window.finish_()
        # self.exit()
        self.app.exec()


if __name__ == '__main__':
    app = Main_Gui()
    app.main()

# app = QApplication(sys.argv)
# window = App_main_application_first_window()
# window.show()
# # sys.exit()
# app.exec()
