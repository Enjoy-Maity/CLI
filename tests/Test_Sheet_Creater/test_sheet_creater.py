import pytest
import pandas as pd
# import sys
import os
# sys.path.append(os.path.dirname(__file__))
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),Main-application))

from Main_application.Sheet_creater import main_func

class Testsheetcreater:
    
    def setup_method(self, method):
        self.host_details_1 = r"C:/CLI_Automation/Test_files/Sheet_creater_test_files/"+"Host_Details.xlsx"
        print(os.path.exists(self.host_details_1))
        
        self.host_details_1_excelfile = pd.ExcelFile(self.host_details_1)
        self.host_details_1_df = pd.read_excel(self.host_details_1_excelfile,
                                               engine='openpyxl',
                                               sheet_name='Host Details')
        
        self.host_details_2 = r"C:/CLI_Automation/Test_files/Sheet_create_test_files/"+"Host_Details_1.xlsx"
        self.host_details_2_df = pd.read_excel(self.host_details_2,
                                               engine= 'openpyxl', 
                                               sheet_name= 'Host Details')
        
        self.host_details_3 = r"C:/CLI_Automation/Test_files/Sheet_creater_test_files/Host_Details_2.xlsx"
        self.host_details_3_df = pd.read_excel(io = self.host_details_3,
                                               engine='openpyxl',
                                               sheet_name='Host Details')

    def teardown_method(self,method):
        pass
    
    def testsheet_creater_normal(self):
        result = main_func(file_name = self.host_details_1)
        assert result == "Successful"
    
    def test_sheet_creater_unsuccessful_1(self):
        """
            Test is Unsuccessful for addition of new but same number of details
        """
        result = main_func(file_name = self.host_details_2)
        
    def test_sheet_creater_unsuccessful_2(self):
        result = main_func(file_name=self.host_details_3)
        # Test is Unsuccessful for addition of new details