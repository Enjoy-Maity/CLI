from pathlib import Path
import sys
import os
import logging
import inspect
# Getting the parent directory of the folder
# parent_directory = str(Path(__file__).resolve().parents[1])
#or
parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_directory)   #Adding the parent in system path

# sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import Custom_Exception as ce 

log_file_path = "C:/Ericsson_Application_Logs/CLI_Automation_Logs/"
Path(log_file_path).mkdir(parents=True,exist_ok=True)

log_file = os.path.join(log_file_path,"Template_checks.log")

logging.basicConfig(filename=log_file,
                             filemode="a",
                             format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                             datefmt='%d-%b-%Y %I:%M:%S %p',
                             encoding= "UTF-8",
                             level=logging.DEBUG)


def main_func(**kwargs):
    file_name = kwargs['filename']
    logging.info("Created and tested logging")
    

main_func(filename="Test File")