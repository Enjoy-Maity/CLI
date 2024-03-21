import os
import sys
import logging
import pandas as pd
from pathlib import Path
from Main_application.file_lines_handler import File_lines_handler as flh


def main_func(dataframe: pd.DataFrame, ip_node: str, running_config_backup_file_lines: list) -> dict:
    """
        Performs the Node Checks for VPLS 2
        
        Arguments : (dataframe, ip_node, running_config_backup_file_lines)
            dataframe ===> pandas.DataFrame
                description ======> contains the dataframe(tabular data) for the VPLS-2 Section of given ip_node for running_config checks
                
            ip_node ===> str
                description =====> ip node for which the dataframe is passed
                
            running_config_backup_file_lines ==> list
                description =====> list of lines from running_config_backup_file in which we need to perform checks
                
        return result_dictionary
            result_dictionary ===> dictionary
                description =====> {'Section Name' : [list of 'S.No.' where there is any problem in template checks in any of the section] } 
                                        or
                                    empty dictionary ===> {}
    """

    # from __init__ import nokia_config_check_start
    # nokia_config_check_start()

    # print(f"inside vpls-2 node checks:\n{'\n'.join(sys.path)}")

    # global log_file;
    # log_file = rf"C:/Ericsson_Application_Logs/CLI_Automation_Logs/Running_Config_Checks(Node_Checks).log"
    #
    # logging.basicConfig(filename=log_file,
    #                     filemode='a',
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt="%d-%b-%Y %I:%M:%S %p",
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)

    dataframe = dataframe.where(~dataframe.isna(), "TempNA")
    logging.debug(f"Got the dataframe after getting all the null values replaced with \'TempNA\' ==> {dataframe.to_markdown()}")

    # from file_lines_handler import File_lines_handler as flh
    vpls_add_section_filter_lines_list = flh().file_lines_starter_filter(file_lines_list=running_config_backup_file_lines,
                                                                         start_word="vpls")

    print(vpls_add_section_filter_lines_list)

# main_func(dataframe= pd.read_excel(io= r"C:\Users\emaienj\Downloads\VPLS_CLI_Design_Documents\VPLS_CLI_Design_Documents\Nokia_Input.xlsx",
#                                    sheet_name="172.31.72.93"),
#           ip_node="172.31.72.93",
#           running_config_backup_file_lines= open(r"C:\Users\emaienj\Downloads\VPLS_CLI_Design_Documents\VPLS_CLI_Design_Documents\Switch_1 traditional_backup.txt","r").readlines())
