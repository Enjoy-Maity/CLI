import logging
import traceback
import pandas as pd
import numpy
import os
from datetime import datetime
from Custom_Exception import CustomException
from pathlib import Path
from tkinter import messagebox

flag = ''
log_file = ''


def host_details_pickle_checker() -> str:
    # logging.basicConfig(filename=log_file,
    #                     filemode="a",
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/{'%(module)s'}/hostnames_to_config_backup_file_mapping): {'%(message)s'}",
    #                     datefmt='%d-%b-%Y %I:%M:%S %p',
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)
    # logging.captureWarnings(capture=True)
    try:
        _username = (os.popen(cmd='cmd.exe /C "echo %username%"').read()).strip()
        _host_details_text_file_path = f"C:\\Users\\{_username}\\AppData\\Local\\CLI_Automation\\host_details_file_path.txt"
        with open(_host_details_text_file_path, 'r') as _f:
            host_details_file_path = _f.readline()
            _f.close()

        del _f
        return host_details_file_path

    except Exception as e:
        logging.error(f"Exception Occurred\nTitle=>{type(e)}\n\t{e}")
        messagebox.showerror(title=f"{type(e)}",
                               message=str(e))
        return ""


def hostnames_to_config_backup_file_mapping(list_of_filenames: list, list_of_hostnames: numpy.array,
                                            parent_directory_of_config_backup_files: str) -> dict:
    """
        Takes two arguments and creates a mapping of hostname to its latest config backup file.
        
        Arguments : (list_of_filenames, list_of_hostnames, parent_directory_of_config_backup_files)
            list_of_filenames : list
                description =====> contains the list of config_backup filenames from \'Pre_Running_Config_Backup\'
            
            list_of_hostnames : numpy.array
                description =====> contains an array of all the hostnames of the selected vendor from uploaded \'Host Details\' sheet.
                
            parent_directory_of_config_backup_files : str
                description =====> to create the path for the config_backup_file to be mapped to the hostnames as values in the result dictionary
                
        
        returns result_dictionary
            result_dictionary : dict
                description =====> a dictionary containing all the mappings of hostnames to the filepath of corresponding hostname.

    """

    # logging.basicConfig(filename=log_file,
    #                     filemode="a",
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/{'%(module)s'}/hostnames_to_config_backup_file_mapping): {'%(message)s'}",
    #                     datefmt='%d-%b-%Y %I:%M:%S %p',
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)
    # logging.captureWarnings(capture=True)

    error_file_for_host_name_not_found = []
    result_dictionary = {}
    list_of_filenames = sorted(list_of_filenames)
    list_of_filepaths = [os.path.join(parent_directory_of_config_backup_files, filename) for filename in
                         list_of_filenames]
    logging.info(f"Created the list_of_filepaths ===>\n{'\n'.join(list_of_filepaths)}\n")

    missing_config_backup_files_mapping = []
    i = 0
    while i < list_of_hostnames.size:
        selected_hostname = list_of_hostnames[i]

        j = 0
        while j < len(list_of_filenames):
            if selected_hostname.upper().strip() in list_of_filenames[j].upper().strip():
                result_dictionary[selected_hostname] = list_of_filepaths[j]
            j += 1

        if selected_hostname not in result_dictionary.keys():
            missing_config_backup_files_mapping.append(selected_hostname)

        i += 1

    if len(missing_config_backup_files_mapping) > 0:
        logging.debug("Missing Config Backup Files mapping to hostnames")
        raise CustomException("Config Backup Files Missing",
                              f"Below Config Backup files are missing as per uploaded host details:\n{', '.join(missing_config_backup_files_mapping)}")

    logging.debug(f"Got the result dictionary:==>\n{result_dictionary}")
    return result_dictionary


def running_config_checks(**kwargs) -> str:
    """
        Calls the vendor specific node checks modules
        
        Arguments : (**kwargs) ==> provides a dictionary of arguments.
            kwargs ====> 
                            vendor_selected : str
                                description =====> contains the information related to the vendor selected
        
        return flag
            flag : str
                description =====> contains 'Unsuccessful' or 'Successful' string corresponding the status of execution completion
    """

    global flag
    flag = ''
    log_file_path = "C:/Ericsson_Application_Logs/CLI_Automation_Logs/"
    Path(log_file_path).mkdir(parents=True, exist_ok=True)

    global log_file
    log_file = os.path.join(log_file_path, "Running_Config_Checks(Node_Checks).log")

    today = datetime.now()
    today = today.replace(hour=0, minute=0, second=0)

    # print(today)
    if os.path.exists(log_file):
        # getting the creation time of the log file
        log_file_create_time = datetime.fromtimestamp(os.path.getctime(log_file))
        # print(log_file_create_time)

        if log_file_create_time < today:
            os.remove(log_file)

    # logging.basicConfig(filename=log_file,
    #                     filemode="a",
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt='%d-%b-%Y %I:%M:%S %p',
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)
    # logging.captureWarnings(capture=True)

    vendor_selected = kwargs['vendor_selected']
    print(type(vendor_selected))

    if 'host_details' in kwargs:
        host_details = kwargs['host_details']

    else:
        host_details = host_details_pickle_checker()

    username = (os.popen('cmd.exe /C "echo %username%"').read()).strip()
    path_for_host_details = rf"C:\Users\{username}\AppData\Local\CLI_Automation\Host_details_Pickle_file\Host_details.pkl"

    logging.info("Creating the Pandas ExcelFile object to read the host details file")
    # file_reader     = pd.ExcelFile(host_details)
    # host_details_df = pd.read_excel(file_reader,sheet_name= 'Host Details', engine='openpyxl')

    host_details_df = pd.read_pickle(path_for_host_details)
    # host_details_df.fillna("TempNA",inplace=True)
    host_details_df = host_details_df.where(~host_details_df.isna(), "TempNA")

    logging.debug(
        f"Created the dataframe from \'Host_details.pkl\' uploaded by the user ===>\n{host_details_df.to_markdown()}\n")

    try:
        # logging.debug("Checking the host details file to filter on the basis of vendor and host name details\n")

        # unique_vendor = np.delete((host_details_df['Vendor'].unique()),np.where((host_details_df['Vendor'].unique()) == 'TempNA'))
        # # unique_vendor = host_details_df['Vendor'].unique()
        # print(unique_vendor)
        # unique_vendor = np.where(unique_vendor != 'TempNA', unique_vendor,'')
        # print(host_details_df.unique())
        # print(unique_vendor)

        path_for_node_checks_pre_files_folder = os.path.join(os.path.dirname(host_details), 'Pre_Running_Config_Backup')
        logging.debug(f"Checking for the existence for \'{path_for_node_checks_pre_files_folder}\'\n")

        temp_df = host_details_df[host_details_df['Vendor'] == vendor_selected.strip()]

        if not Path(path_for_node_checks_pre_files_folder).exists():
            logging.debug(f"\'{path_for_node_checks_pre_files_folder}\' not found\n")
            raise CustomException("Folder Not Founded!",
                                  "\'Pre_Running Config Backup\' Folder not Found!")

        list_of_files_in_running_config_backup_folder = os.listdir(path_for_node_checks_pre_files_folder)

        if len(list_of_files_in_running_config_backup_folder) == 0:
            logging.debug(
                "Raising Custom Exception as there are no files in the \'Pre_Running_Config_Backup\' folder\n")
            raise CustomException("Config Backup Files Missing!",
                                  "No Config backup Files Found in \'Pre_Running_Config_Backup\' folder")

        list_of_files_in_running_config_backup_folder = [element for element in
                                                         list_of_files_in_running_config_backup_folder if ((
                                                                                                               os.path.isfile(
                                                                                                                   os.path.join(
                                                                                                                       path_for_node_checks_pre_files_folder,
                                                                                                                       element))) and (
                                                                                                               element.endswith(
                                                                                                                   '.txt')))]

        logging.info(
            f"Files found in \'Pre_Running_Config_Backup\' == \'{path_for_node_checks_pre_files_folder}\' ==>\n{'\n'.join(list_of_files_in_running_config_backup_folder)}\n"
        )

        logging.debug(
            f"Finding the array containing hostnames from the filtered \'Host Details\' file ====>\n{temp_df.to_markdown()}\n"
        )
        array_of_unique_hostnames = temp_df['Host_Name'].unique()

        ip_hostname_mapping = dict(zip(temp_df['Host_IP'], temp_df['Host_Name']))

        if vendor_selected.strip().upper() == 'NOKIA':
            logging.debug(
                "Calling \'hostnames_to_config_backup_file_mapping\' to get the file path mapping to the hostnames\n")

            result_dictionary = hostnames_to_config_backup_file_mapping(
                list_of_filenames=list_of_files_in_running_config_backup_folder,
                list_of_hostnames=array_of_unique_hostnames,
                parent_directory_of_config_backup_files=path_for_node_checks_pre_files_folder)

            logging.debug("Calling the module for Running Configuration Checks for \'Nokia\' Vendor")

            from Nokia.Nokia_Running_Config_Checks import main_func
            flag = main_func(file_mapping_dictionary=result_dictionary,
                             ip_hostname_mapping=ip_hostname_mapping)

        if vendor_selected.strip().upper() == 'ERICSSON':
            logging.debug("Calling the module for Running Configuration Checks for \'Ericsson\' Vendor")

        if vendor_selected.strip().upper() == 'CISCO':
            logging.debug("Calling the module for Running Configuration Checks for \'Cisco\' Vendor")

        if vendor_selected.strip().upper() == 'HUAWEI':
            logging.debug("Calling the module for Running Configuration Checks for \'Huawei\' Vendor")

        if flag != 'Unsuccessful':
            flag = 'Successful'
            # messagebox.showinfo(title="Task Successfully Completed!",
            #                     message=f"Running Config Checks Task Successfully completed for {vendor_selected}")

    except CustomException as e:
        flag = 'Unsuccessful'
        logging.error(
            f"{traceback.format_exc()}\n\nraised CustomException==>\ntitle = {e.title}\nmessage = {e.message}")

    except Exception as e:
        logging.error(
            f"{traceback.format_exc()}\nTitle --> Exception Occurred!\nMessage --> {e}\n"
        )
        flag = 'Unsuccessful'
        messagebox.showerror(title="Exception Occurred!",
                             message=str(e))

    finally:
        del host_details_df
        # file_reader.close()
        # del file_reader

        logging.debug(f"Retuning the flag variable ====> {flag}")
        # logging.shutdown()

        return flag

# running_config_checks(host_details = r"C:\Users\emaienj\Downloads\VPLS_CLI_Design_Documents\VPLS_CLI_Design_Documents\Host_Details.xlsx",vendor_selected = 'Nokia')
