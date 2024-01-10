import os
import sys
import logging
import traceback
import importlib
import pandas as pd
import numpy as np
from pathlib import Path
from Main_application.CustomThread import CustomThread
from Main_application.Custom_Exception import CustomException

flag = ''
section_dictionary = {}


def section_running_config_checks(dictionary, ip_node, running_config_backup_file_lines) -> dict:
    """
        Creates thread for calling section wise modules for Template Checks

        Arguments : (dictionary,ip_node)
            dictionary ===> dict
                description =====> {'Section Name' : dataframe containing data for the Section}
                                    'Section Name' ======> Section name, Example -> VPLS-1, VPLS-2, Layer3, etc.
                                    dataframe      ======> Dataframe containing the data in the ip node sheet pertaining to corresponding section key.
            
            ip_node ===> str
                description =====> node ip for which the dictionary is passed as argument.
            
            running_config_backup_file_lines ====> list
                description =====> list of lines from pre-running config backup file of the host ip
        
        return thread_result_dictionary
            thread_result_dictionary =====> dict
                description =====> {'Section Name' : [list of 'S.No.' where there is any problem in template checks in any of the section] } 
                                        or
                                    empty dictionary ===> {}
    """
    # print(log_file)
    # logging.basicConfig(filename=log_file,
    #                         filemode="a",
    #                         format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                         datefmt='%d-%b-%Y %I:%M:%S %p',
    #                         encoding= "UTF-8",
    #                         level=logging.DEBUG)

    sections = list(dictionary.keys())
    thread_dictionary = {}
    i = 0
    while i < len(sections):
        try:
            if (len(dictionary[sections[i]]) > 0) and (sections[i] in section_dictionary.keys()):
                # Creating a variable to call the module according to section selected in particular iteration
                module_to_be_called = section_dictionary[sections[i]]

                # Creating Thread to call the main_func() of the module corresponding to selected iteration section.
                thread_dictionary[sections[i]] = CustomThread(target=module_to_be_called.main_func,
                                                              args=(dictionary[sections[i]], ip_node, running_config_backup_file_lines))
                thread_dictionary[sections[i]].daemon = True
                thread_dictionary[sections[i]].start()
            i += 1

        except ImportError as e:
            temp_flag = 'Unsuccessful'
            logging.error(f"ImportError Occurred!======>\n\n{traceback.format_exc()}{e}")
            # messagebox().showerror("Exception Occurred!",e)

        except Exception as e:
            temp_flag = 'Unsuccessful'
            logging.error(f"Exception Occurred!======>\n\n{traceback.format_exc()}{e}")
            # messagebox().showerror("Exception Occurred!",e)

    thread_result_dictionary = {}

    i = 0
    while i < len(sections):
        if sections[i] in section_dictionary.keys():
            thread_result_dictionary[sections[i]] = thread_dictionary[sections[i]].join()
        i += 1

    return thread_result_dictionary


def main_func(**kwargs):
    """
        Performs the general node checks and calls the section specific node checks modules
        
        Arguments : (**kwargs)
            **kwargs ====> file_mapping_dictionary : dict
                            description =====> contains a dictionary with hostnames as keys and corresponding config backup files as values
                           
                           ip_hostname_mapping : dict
                            description =====> contains a dictionary of ips and hostnames.
        returns flag
            flag : str
                description =====> contains 'Unsuccessful' or 'Successful' string corresponding the status of execution completion
    """
    log_file_path = "C:/Ericsson_Application_Logs/CLI_Automation_Logs/"
    Path(log_file_path).mkdir(parents=True, exist_ok=True)

    # global log_file;
    # log_file = os.path.join(log_file_path, "Running_Config_Checks(Node_Checks).log")
    #
    # logging.basicConfig(filename=log_file,
    #                     filemode='a',
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt=7,
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)

    ip_hostname_mapping = kwargs['ip_hostname_mapping']
    file_mapping_dictionary = kwargs['file_mapping_dictionary']

    username = (os.popen('cmd.exe /C "echo %username%"').read()).strip()
    pickle_path = rf"C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\Vendor_pickles\\NOKIA.pickle"

    global flag
    flag = ""

    global section_dictionary
    # section_dictionary = {
    #     'VPLS-1': importlib.import_module("Nokia.Nokia_Section_Running_Config_Checks.VPLS_1_nc"),
    #     'VPLS-2': importlib.import_module("Nokia.Nokia_Section_Running_Config_Checks.VPLS_2_nc")
    # }
    section_dictionary = {
        'VPLS-1': importlib.import_module("Nokia_Section_Running_Config_Checks.VPLS_1_nc"),
        'VPLS-2': importlib.import_module("Nokia_Section_Running_Config_Checks.VPLS_2_nc")
    }

    try:
        if not os.path.exists(pickle_path):
            raise CustomException("Nokia_Pickle File Missing", "Nokia Design Input Pickle File Not Found!")

        with open(pickle_path, "rb") as f:
            nokia_design_input_data = pickle.load(f)
            f.close()
        del f

        ip_hostname_mapping_ips = list(ip_hostname_mapping.keys())

        thread_dictionary = {}

        i = 0
        while (i < len(ip_hostname_mapping_ips)):
            selected_ip = ip_hostname_mapping_ips[i]
            file_to_be_open = file_mapping_dictionary[ip_hostname_mapping[selected_ip]]

            with open(file_to_be_open, "r") as f:
                running_config_backup_file_lines = f.readlines()
                f.close()

            thread_dictionary[selected_ip] = CustomThread(target=section_running_config_checks,
                                                          args=(nokia_design_input_data[selected_ip],
                                                                selected_ip,
                                                                running_config_backup_file_lines))
            thread_dictionary[selected_ip].daemon = True
            thread_dictionary[selected_ip].start()
            i += 1

        logging.debug("Completed Creation of IP Node Threads")

        logging.debug("Stopping all the threads and getting their results")

        thread_result_dictionary = {}
        i = 0
        while (i < len(ip_hostname_mapping_ips)):
            selected_ip = ip_hostname_mapping_ips[i]
            thread_result_dictionary[selected_ip] = thread_dictionary[selected_ip].join()
            i += 1

        error_message_dict = {}

        logging.debug("Checking the thread result")
        i = 0
        while (i < len(ip_hostname_mapping_ips)):
            selected_ip = ip_hostname_mapping_ips[i]
            result_from_thread = thread_result_dictionary[selected_ip]

            logging.debug(f"Nokia ===> {selected_ip} ====> {result_from_thread =}")

            if (result_from_thread == None):
                raise CustomException("Exception Occurred!", "Could not parse data!")

            if (isinstance(result_from_thread, dict)):
                error_message_dict[selected_ip] = result_from_thread

            if (isinstance(result_from_thread, str)):
                if (result_from_thread == 'Unsuccessful'):
                    error_message_dict[selected_ip] = "Could not parse data for Specific Node Check"

                else:
                    error_message_dict[selected_ip] = result_from_thread
            i += 1

        """
            error_message_dict = {
                node_ip : {
                    Section : { reasons : [list of serial numbers with error in template checks]}
                }
            }
        """

        if (len(error_message_dict) > 0):
            error_folder = os.path.join(os.path.join(parent_folder, "Error_Folder"), "Running_Config_Checks_Results")
            Path(error_folder).mkdir(exist_ok=True, parents=True)

            logging.debug(f"Creating the folder for Node checks namely for Nokia template checks\n{error_folder}")
            error_file = os.path.join(error_folder, "Nokia_Nodes_Running_Config_Checks_Error.txt")

            """
                    error_message = "<================<<Errors Found in Template checks of "Nokia" Vendor Design Input sheet workbook>>================>
                                    Node IP : 'x.x.x.x'
                                    'Section'
                                    'Reason for 'S.No.' ==>> a, b, c, .........
                                    
                                    'Section'
                                    .......................................'"
                """

            logging.debug(f"Got the error_message_dict =====>{error_message_dict}\n")
            error_message = "<================<<Design Input Errors Observed in Below Uploaded Nodes for \"Nokia\" Vendor>>================>"

            node_ips = list(error_message_dict.keys())

            logging.debug(f"Node ips with errors ======>\n{node_ips}")

            i = 0
            while (i < len(node_ips)):
                sections = list(error_message_dict[node_ips[i]].keys())
                error_message = f"{error_message}\nNode IP : \"{node_ips[i]}\""
                j = 0
                while (j < len(sections)):
                    error_message = f"{error_message}\nSection : \'{sections[j]}\'"
                    reasons = list(error_message_dict[node_ips[i]][sections[j]].keys())
                    k = 0
                    while (k < len(reasons)):
                        reason = reasons[k]
                        sr_no_list = error_message_dict[node_ips[i]][sections[j]][reason]

                        if (reason.endswith(")")):
                            error_message = f"{error_message}\n\t{k + 1}.) {reason} ==>> {', '.join(str(element) for element in sr_no_list)}"

                        else:
                            error_message = f"{error_message}\n\t{k + 1}.) {reason} for \'S.No.\' ==>> ({', '.join(str(int(element)) for element in sr_no_list)})"
                        k += 1

                    error_message = f"{error_message}\n"
                    j += 1
                error_message = f"{error_message}\n\n"

                i += 1

            with open(error_file, 'w') as f:
                f.write(error_message)
                f.close()

            raise CustomException('Wrong Input for Uploaded Template!',
                                  f"Section-wise Wrong Input observed in uploaded 'Design Input Sheet' for node ips :\n\n({', '.join(element for element in node_ips)})\n\nPlease Check the Error Input File \'Template_Checks_error_Vendor_wise.txt\' for further details!")

        if (flag != 'Unsuccessful'):
            flag = 'Successful'

    except CustomException as e:
        flag = 'Unsuccessful'
        logging.error(f"{traceback.format_exc()}\n\nraised CustomException==>\ntitle = {e.title}\nmessage = {e.message}")

    except Exception as e:
        flag = 'Unsuccessful'
        logging.error(f"{traceback.format_exc()}\n\nException:==>{e}")
        messagebox().showerror("Exception Occurred!", e)

    finally:
        logging.info(f"Returning Status ==> {flag}")

        logging.shutdown()
        return flag

# main_func()
