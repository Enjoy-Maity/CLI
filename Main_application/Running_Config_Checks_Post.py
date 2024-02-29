import os
import numpy
import logging
import traceback
from tkinter import messagebox

import pandas

from Main_application.Custom_Exception import CustomException

flag = ''


def host_details_pickle_checker() -> str:
    try:
        _username = os.popen(cmd=r'cmd.exe /C "echo %username%"').read().strip()
        _host_details_text_file_path = f"C:\\Users\\{_username}\\AppData\\Local\\CLI_Automation\\host_details_file_path.txt"
        with open(_host_details_text_file_path, 'r') as _f:
            _host_details_file_path = _f.readline()
            _f.close()

        del _f
        logging.info(f"Got the Host_details_file_path as {_host_details_file_path}")
        return _host_details_file_path

    except Exception as e:
        logging.error(f"Exception Occurred\nTitle=>{type(e)}\n\t{e}")
        messagebox.showerror(title=f"{type(e)}",
                             message=str(e))
        return ""


def hostnames_to_config_backup_file_mapping(list_of_filenames: list, list_of_hostnames: numpy.array,
                                            parent_directory_of_config_backup_files: str) -> dict:
    """
    Takes two arguments and creates a mapping of hostname to its latest config backup file.
    :param list_of_filenames(list): contains the list of config_backup filenames from \'Post_Running_Config_Backup\'
    :param list_of_hostnames(numpy.array): contains an array of all the hostnames of the selected vendor from uploaded \'Host Details\' sheet.
    :param parent_directory_of_config_backup_files(str): to create the path for the config_backup_file to be mapped to the hostnames as values in the result dictionary
    :return result_dictionary(dict):  a dictionary containing all the mappings of hostnames to the filepath of corresponding hostname.
    """
    result_dictionary = {}
    missing_config_backup_files_mapping = []
    list_of_filenames = numpy.array(sorted(list_of_filenames))
    list_of_filepaths = numpy.array([os.path.join(parent_directory_of_config_backup_files, filename) for filename in list_of_filenames])

    logging.info(f"Created the list_of_filepaths ===>\n{'\n'.join(list_of_filepaths)}\n")

    i = 0
    while i < len(list_of_hostnames):
        selected_hostname = list_of_hostnames[i]
        temp_array = list_of_filepaths[numpy.char.find(list_of_filenames, selected_hostname) >= 0].tolist()
        if len(temp_array) != 0:
            if len(temp_array) > 1:
                # '1. first, sort the temp-array of filepaths according to modified time,'
                # '2. second, get the first element'
                temp_array.sort(key=os.path.getmtime, reverse=True)
                result_dictionary[selected_hostname] = temp_array[0]

            else:
                result_dictionary[selected_hostname] = temp_array[0]
        else:
            missing_config_backup_files_mapping.append(selected_hostname)
        i += 1

    if len(missing_config_backup_files_mapping) > 0:
        logging.error("Missing Config Backup Files mapping to hostnames")
        raise CustomException("Config Backup Files Missing",
                              f"Below Config Backup files are missing as per uploaded host details:\n{', '.join(missing_config_backup_files_mapping)}")

    logging.info("Returning the result_dictionary with mapping of hostnames and file")
    return result_dictionary


def main_func(**kwargs: dict) -> str:
    """
    Main function for the general module of post checks.
	Args: kwargs (dict): keyword arguments containing argument
            vendor_selected = contains the string signifying which vendor is being selected by the user.
	Returns:
	   flag (str): string containing the status of the execution of the module
	"""
    global flag
    flag = ''

    username = os.popen(cmd="cmd.exe /C \"echo %username%\"").read().strip()

    host_details = host_details_pickle_checker()
    vendor_selected = str(kwargs['vendor_selected'])
    logging.info(f"Got the vendor_selected as {vendor_selected}")

    path_for_host_details = rf"C:\Users\{username}\AppData\Local\CLI_Automation\Host_details_Pickle_file\Host_details.pkl"
    logging.info("Creating the Pandas ExcelFile object to read the host details file")

    host_details_df = pandas.read_pickle(path_for_host_details)
    host_details_df = host_details_df.where(~host_details_df.isna(), "TempNA")

    logging.info(
        f"Created the dataframe from \'Host_details.pkl\' uploaded by the user ===>\n{host_details_df.to_markdown()}\n"
    )

    try:
        path_for_node_checks_post_files_folder = os.path.join(os.path.dirname(host_details), 'Post_Running_Config_Backup')

        temp_df = host_details_df[host_details_df['Vendor'].str.strip().str.upper() == vendor_selected.strip().upper()]

        if not os.path.exists(path_for_node_checks_post_files_folder):
            logging.debug(
                f"\'{path_for_node_checks_post_files_folder}\' not found\n"
            )
            raise CustomException("Folder Not Founded!",
                                  "\'Post_Running Config Backup\' Folder not Found!")

        list_of_files_in_running_config_backup_folder = os.listdir(path_for_node_checks_post_files_folder)

        if len(list_of_files_in_running_config_backup_folder) == 0:
            logging.debug(
                "Raising Custom Exception as there are no files in the \'Post_Running_Config_Backup\' folder\n"
            )
            raise CustomException("Config Backup Files Missing!",
                                  "No Config backup Files Found in \'Post_Running_Config_Backup\' folder")

        list_of_files_in_running_config_backup_folder = [element for element in
                                                         list_of_files_in_running_config_backup_folder
                                                         if (
                                                                 (os.path.isfile(
                                                                     os.path.join(path_for_node_checks_post_files_folder, element)))
                                                                 and
                                                                 (element.endswith('.txt'))
                                                         )]

        logging.info(
            f"Files found in \'Post_Running_Config_Backup\' == \'{path_for_node_checks_post_files_folder}\' ==>\n{'\n'.join(list_of_files_in_running_config_backup_folder)}\n"
        )

        logging.info(
            f"Finding the array containing hostnames from the filtered \'Host Details\' file ====>\n{temp_df.to_markdown()}\n"
        )

        array_of_unique_hostnames = temp_df['Host_Name'].unique()

        ip_hostname_mapping = dict(
                                    zip(
                                        temp_df['Host_IP'], temp_df['Host_Name']
                                    )
                                )

        if vendor_selected.strip().upper() == 'NOKIA':
            logging.info(
                "Calling \'hostnames_to_config_backup_file_mapping\' to get the file path mapping to the hostnames\n"
            )
            result_dictionary = hostnames_to_config_backup_file_mapping(
                list_of_filenames= list_of_files_in_running_config_backup_folder,
                list_of_hostnames= array_of_unique_hostnames,
                parent_directory_of_config_backup_files= path_for_node_checks_post_files_folder
            )

            logging.debug(
                "Calling the module for Running Configuration Checks for \'Nokia\' Vendor"
            )

            from Nokia.Nokia_Running_Config_Checks_Post import main_func
            flag = main_func(file_mapping_dictionary= result_dictionary,
                             ip_hostname_mapping= ip_hostname_mapping)

        if vendor_selected.strip().upper() == 'ERICSSON':
            logging.debug(
                "Calling the module for Running Configuration Checks for \'Ericsson\' Vendor"
            )

        if vendor_selected.strip().upper() == 'CISCO':
            logging.debug(
                "Calling the module for Running Configuration Checks for \'Cisco\' Vendor"
            )

        if vendor_selected.strip().upper() == 'HUAWEI':
            logging.debug(
                "Calling the module for Running Configuration Checks for \'Huawei\' Vendor"
            )

        if flag != 'Unsuccessful':
            flag = 'Successful'

    except CustomException as e:
        logging.error(
            f"Exception Raised =>\nTitle ==> {e.title}\nMessage ==> {e.message}"
        )
        flag = 'Unsuccessful'

    except Exception as e:
        logging.error(
            f"Exception Occurred!==>\n\n{traceback.format_exc()}\nTitle==>{type(e)}\nMessage==>{str(e)}"
        )
        messagebox.showerror("Exception Occurred!", str(e))
        flag = 'Unsuccessful'

    finally:
        logging.info(f"Returning the flag => {flag}")
        logging.shutdown()
        return flag

# main_func(vendor_selected= "Nokia")
