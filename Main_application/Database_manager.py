import os
import logging
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
from abc import ABC,abstractmethod

log_file = "C:\\Ericsson_Application_Logs\\CLI_Automation_Logs\\Database_manager.log"
logging.basicConfig(filename=log_file,
                             filemode="a",
                             format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({'%(module)s'}): {'%(message)s'}",
                             datefmt='%d-%b-%Y %I:%M:%S %p',
                             encoding= "UTF-8",
                             level=logging.DEBUG)

class Abstract_database_manager(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def table_creater(self):
        pass
    
    @abstractmethod
    def database_table_checker(self):
        pass
    
    @abstractmethod
    def data_adder(self):
        pass
    
    @abstractmethod
    def data_remover(self):
        pass
    
    @abstractmethod
    def auto_database_remover(self):
        pass
    
    @abstractmethod
    def database_updater(self):
        pass
    
    @abstractmethod
    def data_fetcher(self):
        pass

class Database_manager(Abstract_database_manager):
    def __init__(self):
        self.db_path = "C:\\Users\\emaienj\\AppData\\Local\\CLI_Automation\\Database\\CLI_Automation_Database.db"
        Path(os.path.dirname(self.db_path)).mkdir(exist_ok=True, parents=True)
        
        self.table_name = "vendor_task_status"
        self.auto_database_remover()
    
    def database_table_checker(self:Self):
        self.conn = sqlite3.connect(self.db_path)
        command = "SELECT name FROM sqlite_master WHERE type = 'table';"
        
        self.cursor = self.conn.cursor()
        self.table_list = self.cursor.execute(command).fetchall()
        
        logging.debug(f"Got the list of tables from \'{self.db_path}\' => \n\'[{'\n'.join(self.table_list)}]\'")
        
        self.status = False
        if(self.table_name in self.cursor.fetchall()):
            self.status = True
            self.conn.close()
            logging.debug(f"Returning True as {self.table_name} found in CLI_Automation_Database.db")
            return self.status

        else:
            logging.debug(f"Returning False as {self.table_name} not found in CLI_Automation_Database.db")
            self.conn.close()
            return self.status

    def auto_database_remover(self:Self):
        """Auto deletes the database after a fixed time period
        """
        logging.debug("Checking the time for the auto database remover")
        self.current_time = datetime.now()
        self.current_hour = int(self.current_time.strftime("%H"))
        
        if(os.path.exists(self.db_path)):
                creation_time = dataetime.fromtimestamp(os.path.getctime(self.db_path))
                
                if(self.current_hour >= 12):
                    if(((datetime.now() - creation_time).days >= 1) or (((datetime.now() - creation_time).seconds//3600) >= 20)):
                        os.remove(self.db_path)
                        self.table_creater()
        
        
    def table_creater(self: Self):
        """Creates the table for Vendor.
        """
        self.table_creater_status = self.database_table_checker()
        
        if(not self.table_creater_status):
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            command = f"CREATE TABLE {self.table_name} (Vendor TEXT, Template_Checks TEXT, Running_Config_Pre_Checks TEXT, CLI_Preparation TEXT ,Running_Config_Post_Checks TEXT);"
            
            logging.debug(f"Creating the table {self.table_name}\n")
            self.cursor.execute(command)
            logging.debug(f"Created the table {self.table_name} \n")
            
            self.conn.commit()
            
            self.conn.close()
            
            
    def data_adder(self:Self,vendor_list: list):
        """Creates the rows for the unique vendors of vendor_list

        Args:
            vendor_list (list): _description_ : contains the list of unique vendors mentioned in the selected host details
        """
        self.table_creater()
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        logging.debug("We are creating empty vendor rows in the vendor database")
        i = 0
        while(i < len(vendor_list)):
            self.cursor.execute(f"INSERT INTO {self.table_name} VALUES ({vendor_list[i]},'','','','');")
            i += 1
        
        self.conn.commit()
        
        logging.debug(f"Created the empty rows for the vendors => {', '.join(vendor_list)}")
        
        self.conn.close()
    
    def database_updater(self:Self, vendor: str, task: str, status: str):
        """Updates the database for vendor with data for given task and status

        Args:
            vendor (str): _description_ : Vendor for which the task status should be updated
            task (str): _description_ : Task column for which the vendor data should be updated
            status (str): _description_ : Status which needs to be entered in the database
        """
        logging.debug("Updating the vendor database")
        
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        command = f"UPDATE {self.table_name} SET {task} = {status} WHERE Vendor = {vendor};"
        
        self.cursor.execute(command)
        self.conn.commit()
        
        logging.debug(f"Updated the vendor database for {vendor} for task => {task} with status => {status}")
        self.conn.close()
    
    def data_remover(self:Self):
        """ Dropping the rows from the entire table
        """
        command = f"DELETE FROM {self.table_name};"
        
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute(command)
        self.conn.commit()
        
        logging.debug(f"Deleted all the rows in the table {self.table_name}")
        
        self.conn.close()
    
    def data_fetcher(self:Self) -> pd.DataFrame:
        """ Fetches all the data and returns the dataframe of all the rows
        
        Returns
            result_dataframe (pd.DataFrame) : _description_ : Getting all the results from the database and retuning all the data in a dataframe
            
        """
        
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        command = f"SELECT * FROM {self.table_name}"
        
        result_data = self.cursor.execute(command).fetchall()
        
        logging.debug(f"Got all the data from the database = > \n [{'\n'.join(result_data)}]\n")
        
        self.conn.close()
        
        result_dataframe = pd.DataFrame.from_records(data=result_data, columns= ["Vendor","Template_Checks","Running_Config_Pre_Checks","CLI_Preparation","Running_Config_Post_Checks"])
        
        logging.debug(f"Created the dataframe from the database records =>\n {result_dataframe.to_markdown()}")
        
        return result_dataframe