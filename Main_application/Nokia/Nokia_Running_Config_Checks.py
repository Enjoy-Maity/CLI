import os
import logging
import traceback
import importlib
import numpy as np
import pickle
from pathlib import Path
from tkinter import messagebox

from Main_application.CustomThread import CustomThread


# from Custom_Exception import CustomException
class CustomException(Exception):
    def __init__(self, title: str, message: str):
        super().__init__()
        self.title = title
        self.message = message
        messagebox.showerror(title=self.title,
                             message=self.message)


flag = ''
section_dictionary = {}


def error_message_dict_filter(dictionary: dict) -> dict:
    """
    Filters the dictionary for removing empty dict or None values.
    :param dictionary: dictionary containing the error structure
    :return: result_dictionary : dict : cleaned dictionary
    """
    result_dictionary = {}
    logging.info(
        "Got the original dictionary as :-\n{" +
        f"{'\n'.join([f'{key} : {value}' for key, value in dictionary.items()])}" +
        "}\n"
    )

    if (dictionary is not None) and (isinstance(dictionary, dict)):
        # the structure of the dictionary is
        # {node: {
        #               section: {
        #                           reason: [list of Serial No.s] }}}
        if len(dictionary) > 0:
            logging.info(f"Length of the dictionary found greater than 0 ==>{len(dictionary)}\n")
            node_array = np.array(
                list(
                    dictionary.keys()
                )
            )
            logging.info(
                f"Got the dictionary keys =>\n{node_array}"
            )
            i = 0
            while i < node_array.size:
                node = node_array[i]
                if (dictionary[node] is not None) and (isinstance(dictionary[node], dict)):
                    if len(dictionary[node]) > 0:
                        sections_array = np.array(
                            list(dictionary[node].keys())
                        )

                        logging.info(
                            f"Got the section_array for node: {node}\n\t{sections_array}\n"
                        )

                        j = 0
                        while j < sections_array.size:
                            section = sections_array[j]
                            if (dictionary[node][section] is not None) and (isinstance(dictionary[node][section], dict)):
                                if len(dictionary[node][section]) > 0:
                                    reason_array = np.array(
                                        list(dictionary[node][section].keys())
                                    )

                                    logging.info(
                                        f"Got the array of reasons for node {node} =>\n\tfor section {section}\n\t\t ==>{reason_array}\n"
                                    )

                                    k = 0
                                    while k < reason_array.size:
                                        reason = reason_array[k]
                                        logging.info(f"for node => \'{node}\' and \n\tsection => {section}\n\t\tselected reason => {reason}")
                                        if (dictionary[node][section][reason] is not None) and (isinstance(dictionary[node][section][reason], (list, tuple))):
                                            if len(dictionary[node][section][reason]) > 0:
                                                if node not in result_dictionary:
                                                    result_dictionary[node] = {}
                                                    if section not in result_dictionary[node]:
                                                        result_dictionary[node][section] = {}
                                                        result_dictionary[node][section][reason] = dictionary[node][section][reason]
                                                    else:
                                                        result_dictionary[section][reason] = dictionary[node][section][reason]

                                                else:
                                                    if section not in result_dictionary[node]:
                                                        result_dictionary[node][section] = {}
                                                        result_dictionary[node][section][reason] = dictionary[node][section][reason]
                                                    else:
                                                        result_dictionary[node][section][reason] = dictionary[node][section][reason]

                                        k += 1

                            j += 1

                i += 1

    logging.info(
        "Created the final result dictionary as => {\n" +
        f"\t{'\n\t'.join(
            [f'{node}: \n{'\n\t\t'.join(
                [f'{section}: \n{'\n\t\t\t'.join(
                    [f'{reason}: {reason_list}' for reason, reason_list in reasons.items()]
                )}' for section, reasons in value.items()]
            )}' for node, value in result_dictionary.items()]
        )}" +
        "}"
    )
    return result_dictionary


def error_message_writer(parent_folder: str, error_message_dict: dict) -> str:
    """
    Writes the error message in a file.
    :param parent_folder: parent folder of the selected host_details
    :param error_message_dict: dictionary containing error details
    :return: error_message (str): contains the error message that has been written
    """
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
    while i < len(node_ips):
        sections = list(error_message_dict[node_ips[i]].keys())
        error_message = f"{error_message}\nNode IP : \"{node_ips[i]}\""
        j = 0
        while j < len(sections):
            error_message = f"{error_message}\nSection : \'{sections[j]}\'"

            reasons = list(error_message_dict[node_ips[i]][sections[j]].keys())
            k = 0
            while k < len(reasons):
                reason = reasons[k]
                sr_no_list = error_message_dict[node_ips[i]][sections[j]][reason]

                if reason.endswith(")"):
                    error_message = f"{error_message}\n\t{k + 1}.) {reason} ==>> {', '.join(str(element) for element in sr_no_list)}"

                else:
                    error_message = f"{error_message}\n\t{k + 1}.) {reason} for \'S.No.\' ==>> ({', '.join(str(int(element)) for element in sr_no_list)})"
                k += 1

            error_message = f"{error_message}\n"
            j += 1
        error_message = f"{error_message}\n\n"

        i += 1

    with open(error_file, 'w') as f:
        # print(f"Inside Main_func of Nokia now writing message line 366")
        f.write(error_message)
        f.close()
    del f

    logging.info("Wrote the error message for Nokia Running Config Checks")
    return error_message


def section_running_config_checks(dictionary, ip_node, running_config_backup_file_lines) -> dict:
    """
        Creates thread for calling section wise modules for Running Config Checks

        Arguments : (dictionary,ip_node)
            dictionary ===> dict
                description =====> {'Section Name' : dataframe containing data for the Section}
                                    'Section Name' ======> Section name, Example -> VPLS-1, VPLS-2, Layer3, etc.
                                     dataframe      ======> Dataframe containing the data in the ip node sheet pertaining to corresponding section key.}
            
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
    # thread_dictionary = {}
    # logging.info(f"Setting an event to wait until the thread is completed")
    # event = Event()
    # i = 0
    # while i < len(sections):
    #     try:
    #         if (len(dictionary[sections[i]]) > 0) and (sections[i] in section_dictionary.keys()):
    #             # Creating a variable to call the module according to section selected in particular iteration
    #             module_to_be_called = section_dictionary[sections[i]]
    #
    #             # Creating Thread to call the main_func() of the module corresponding to selected iteration section.
    #             thread_dictionary[sections[i]] = CustomThread(target=module_to_be_called.main_func,
    #                                                           args=(dictionary[sections[i]], ip_node, running_config_backup_file_lines))
    #             # thread_dictionary[sections[i]].daemon = True
    #             thread_dictionary[sections[i]].start()
    #         i += 1
    #
    #     except ImportError as e:
    #         temp_flag = 'Unsuccessful'
    #         logging.error(f"ImportError Occurred!======>\n\n{traceback.format_exc()}{e}")
    #         # messagebox.showerror("Exception Occurred!",e)
    #
    #     except Exception as e:
    #         temp_flag = 'Unsuccessful'
    #         logging.error(f"Exception Occurred!======>\n\n{traceback.format_exc()}{e}")
    #         # messagebox.showerror("Exception Occurred!",e)
    #
    # thread_result_dictionary = {}
    #
    # event.set()
    #
    # i = 0
    # while i < len(sections):
    #     if sections[i] in section_dictionary.keys():
    #         thread_result_dictionary[sections[i]] = thread_dictionary[sections[i]].join()
    #     i += 1

    thread_result_dictionary = {}
    i = 0
    while i < len(sections):
        if (len(dictionary[sections[i]]) > 0) and (sections[i] in section_dictionary.keys()):
            # Creating a variable to call the module according to section selected in particular iteration
            module_to_be_called = section_dictionary[sections[i]]

            # Creating Thread to call the main_func() of the module corresponding to selected iteration section.
            thread_result_dictionary[sections[i]] = module_to_be_called.main_func(dictionary[sections[i]], ip_node, running_config_backup_file_lines)

        i += 1
    logging.info(f"Got the thread_result_dictionary as \n{thread_result_dictionary} ")

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
    parent_folder = ""

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
        'VPLS-1': importlib.import_module("Main_application.Nokia.Nokia_Section_Running_Config_Checks.VPLS_1_nc"),
        'VPLS-2': importlib.import_module("Main_application.Nokia.Nokia_Section_Running_Config_Checks.VPLS_2_nc")
    }

    try:
        if not os.path.exists(pickle_path):
            raise CustomException("Nokia_Pickle File Missing", "Nokia Design Input Pickle File Not Found!")

        with open(pickle_path, "rb") as f:
            nokia_design_input_data = pickle.load(f)
            f.close()
        del f

        ip_hostname_mapping_ips = list(ip_hostname_mapping.keys())

        # thread_dictionary = {}

        # i = 0
        # while i < len(ip_hostname_mapping_ips):
        #     selected_ip = ip_hostname_mapping_ips[i]
        #     file_to_be_open = file_mapping_dictionary[ip_hostname_mapping[selected_ip]]
        #
        #     with open(file_to_be_open, "r") as f:
        #         running_config_backup_file_lines = f.readlines()
        #         f.close()
        #
        #     thread_dictionary[selected_ip] = CustomThread(target=section_running_config_checks,
        #                                                   args=(nokia_design_input_data[selected_ip],
        #                                                         selected_ip,
        #                                                         running_config_backup_file_lines))
        #     # thread_dictionary[selected_ip].daemon = True
        #     thread_dictionary[selected_ip].start()
        #     i += 1

        # logging.debug("Completed Creation of IP Node Threads")

        # main_func_event = Event()
        #
        # thread_result_dictionary = {}
        # i = 0
        # while i < len(ip_hostname_mapping_ips):
        #     selected_ip = ip_hostname_mapping_ips[i]
        #     thread_result_dictionary[selected_ip] = thread_dictionary[selected_ip].join()
        #     logging.info(f"Got the result_dictionary for {selected_ip}\n{thread_result_dictionary[selected_ip]}")
        #     # time.sleep(0.4)
        #     i += 1
        #
        # main_func_event.set()

        thread_result_dictionary = {}
        i = 0
        while i < len(ip_hostname_mapping_ips):
            selected_ip = ip_hostname_mapping_ips[i]
            file_to_be_open = file_mapping_dictionary[ip_hostname_mapping[selected_ip]]

            with open(file_to_be_open, "r") as f:
                running_config_backup_file_lines = f.readlines()
                f.close()
            del f

            thread_result_dictionary[ip_hostname_mapping_ips[i]] = section_running_config_checks(nokia_design_input_data[selected_ip],
                                                                                                 selected_ip,
                                                                                                 running_config_backup_file_lines)
            i += 1

        error_message_dict = {}
        # logging.debug("Stopping all the threads and getting their results")
        # logging.debug("Checking the thread result")
        i = 0
        while i < len(ip_hostname_mapping_ips):
            selected_ip = ip_hostname_mapping_ips[i]
            result_from_thread = thread_result_dictionary[selected_ip]

            logging.debug(f"Nokia ===> {selected_ip} ====> {result_from_thread =}")

            if result_from_thread is None:
                raise CustomException("Exception Occurred!", "Could not parse data!")

            if isinstance(result_from_thread, dict):
                error_message_dict[selected_ip] = result_from_thread

            if isinstance(result_from_thread, str):
                if result_from_thread == 'Unsuccessful':
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
        username = (os.popen(cmd=r'cmd.exe /C "echo %username%"').read()).strip()
        host_details_file_path = rf'C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\host_details_file_path.txt'
        # parent_folder = ''
        with open(host_details_file_path, 'r') as f:
            parent_folder = os.path.dirname(f.readline())
            f.close()

        del f

        error_message_dict = error_message_dict_filter(dictionary=error_message_dict)

        error_message = ''

        if len(error_message_dict) > 0:
            temp_thread = CustomThread(target=error_message_writer,
                                       args=(parent_folder,
                                             error_message_dict))
            temp_thread.daemon = True
            temp_thread.start()

            error_message = temp_thread.join()
            logging.info("Got the error message from the thread")

        if len(error_message) > 0:
            node_ips = list(error_message_dict.keys())
            error_message_to_show = f"Section-wise Wrong Input observed in uploaded 'Design Input Sheet' for below node ips :\n\n({', '.join(node_ips)})\n\nPlease Check the Error Input File \'Nokia_Nodes_Running_Config_Checks_Error.txt\' for further details!"
            logging.info("Raising CustomException for informing user about the wrong inputs on Nokia Design Input Sheet")

            flag = 'Unsuccessful'
            # messagebox.showerror(title='Wrong Input for Uploaded Template!', message=error_message_to_show)
            raise CustomException(title='Wrong Input for Uploaded Template!', message=error_message_to_show)

        if flag != 'Unsuccessful':
            flag = 'Successful'

    except CustomException as e:
        logging.error(f"raised CustomException==>\n title = {e.title}\n message = {e.message}")
        if e.title == "Wrong Input for Uploaded Template!":
            os.popen(cmd=rf'cmd.exe /C "notepad.exe {os.path.join(os.path.join(os.path.join(parent_folder, "Error_Folder"), "Running_Config_Checks_Results"),"Nokia_Nodes_Running_Config_Checks_Error.txt")}"')
        flag = 'Unsuccessful'

    except Exception as e:
        flag = 'Unsuccessful'
        logging.error(f"{traceback.format_exc()}\n\nException:==>{e}")
        messagebox.showerror("Exception Occurred!", str(e))

    finally:
        logging.info(f"Returning Status ==> {flag}")

        logging.shutdown()
        return flag

# main_func()
