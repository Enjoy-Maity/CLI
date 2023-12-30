import pandas
import sys
from PySide6.QtCore import Qt
from GUI.database_model import DataModel
from PySide6.QtWidgets import QWidget,QMainWindow, QApplication
from GUI.ui_Main_Application import Ui_Main_Application_Window

class App_Main_Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.main_window_ui = Ui_Main_Application_Window()
        self.main_window_ui.__init__()
        
        self.main_window_ui.setupUi(self)
        
        self.vendor_selected = ''
        self.task_dictionary = {'Template Checks':self.main_window_ui.template_checks_label_text,
                                'Running Config Pre Checks': self.main_window_ui.running_config_pre_checks_label_text,
                                'CLI Preparation': self.main_window_ui.cli_preparation_status_label_text,
                                'Running Config Post Checks':self.main_window_ui.running_config_post_checks_label_text}
        
        self.task_color_dictionary = {'Template Checks':self.main_window_ui.template_checks_label_color,
                                      'Running Config Pre Checks':self.main_window_ui.running_config_pre_checks_label_color,
                                      'CLI Preparation':self.main_window_ui.cli_preparation_status_label_color,
                                      'Running Config Post Checks':self.main_window_ui.running_config_post_checks_label_color}
        
        self.color_dictionary = {'Unsuccessful' : 'red',
                                 'Successful' : 'green',
                                 'In Progress' : 'white'}
        
        self.data = pandas.DataFrame()
        
        
    def current_vendor(self,_) -> None:
        """Gets Selected Vendor by the User

        Args:
            _ (_type_): _description_ : Empty argument for getting the connection signal
        """
        self.vendor_selected = self.main_window_ui.vendor_details_selection_combobox.currentText()
    
    def combobox_clearer(self) -> None:
        """Clears the combobox
        """
        self.main_window_ui.vendor_details_selection_combobox.clear()
        
    def combobox_data_items_adder(self,vendor_list:list) -> None:
        """Adds the Items in the combobox

        Args:
            vendor_list (list): _description_ : list of items to be added in the combobox
        """
        self.main_window_ui.vendor_list = vendor_list
    
    def status_label_updater_from_table(self, data: pandas.DataFrame) -> None:
        """Updates the label of the tasks based on the data from table in \'Existing Session\'

        Args:
            data (pandas.DataFrame): _description_ : DataFrame containing the data of the existing session
        """
        
        # Running the current_vendor method to get the latest selected vendor
        self.current_vendor(_)
        
        self.filtered_dataframe = data[data["Vendor"] == self.vendor_selected]
        
        if(len((self.filtered_dataframe.iloc[0,self.filtered_dataframe.columns.get_loc('Template_Checks')]).strip()) > 0):
            self.main_window_ui.template_checks_label_text = self.filtered_dataframe.iloc[0,self.filtered_dataframe.columns.get_loc('Template_Checks')]
        
        if(len((self.filtered_dataframe.iloc[0,self.filtered_dataframe.columns.get_loc('Running_Config_Pre_Checks')]).strip()) > 0):
            self.main_window_ui.running_config_pre_checks_label_text = self.filtered_dataframe.iloc[0,self.filtered_dataframe.columns.get_loc('Running_Config_Pre_Checks')]
        
        if(len((self.filtered_dataframe.iloc[0,self.filtered_dataframe.columns.get_loc('CLI_Preparation')]).strip()) > 0):
            self.main_window_ui.cli_preparation_status_label_text = self.filtered_dataframe.iloc[0,self.filtered_dataframe.columns.get_loc('CLI_Preparation')]
            
        if(len((self.filtered_dataframe.iloc[0,self.filtered_dataframe.columns.get_loc('Running_Config_Post_Checks')]).strip()) > 0):
            self.main_window_ui.running_config_post_checks_label_text = self.filtered_dataframe.iloc[0,self.filtered_dataframe.columns.get_loc('Running_Config_Post_Checks')]
        
    
    def task_method_status_updater(self, task:str, status:str) -> None:
        self.task_dictionary[task] = status
        self.task_color_dictionary[task] = self.color_dictionary[status]
    
    def table_view_data_loader(self) -> None:
        self.table_model = DataModel(self.data)
        self.main_window_ui.task_database_tableview.setModel(self.table_model)
        


