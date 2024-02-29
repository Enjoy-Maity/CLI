import os
import numpy
import pickle
import importlib
import logging
from tkinter import messagebox
from pathlib import Path
from Main_application.CustomThread import CustomThread


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
    :param dictionary(dict): dictionary containing the error structure
    :return result_dictionary(dict): cleaned dictionary
    """
    result_dictionary = {}
    logging.info(
        "Got the original dictionary as :-\n{" +
        f"{'\n'.join([f'{key} : {value}' for key, value in dictionary.items()])}" +
        "}\n"
    )

    if (dictionary is not None) and (isinstance(dictionary, dict)):
        if len(dictionary) > 0:
            logging.info(
                f"Length of the dictionary found greater than 0 ==>{len(dictionary)}\n"
            )

            node_array = numpy.array(
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
                    if len(dictionary) > 0:
                        sections_array = numpy.array(
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
                                    reason_array = numpy.array(
                                        list(dictionary[node][section].keys())
                                    )

                                    logging.info(
                                        f"Got the array of reasons for node {node} =>\n\tfor section {section}\n\t\t ==>{reason_array}\n"
                                    )

                                    k = 0
                                    while k < reason_array.size:
                                        reason = reason_array[k]
                                        logging.info(
                                            f"for node => \'{node}\' and \n\tsection => {section}\n\t\tselected reason => {reason}"
                                        )

                                        logging.debug(f"{type(dictionary[node][section][reason]) = }")
                                        if (dictionary[node][section][reason] is not None) and (isinstance(dictionary[node][section][reason], (list, tuple))):

                                            if len(dictionary[node][section][reason]) > 0:
                                                if node not in result_dictionary:
                                                    result_dictionary[node] = {}

                                                    if section not in result_dictionary[node]:
                                                        result_dictionary[node][section] = {}
                                                        result_dictionary[node][section][reason] = dictionary[node][section][reason]
                                                    else:
                                                        result_dictionary[node][section][reason] = dictionary[node][section][reason]

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
    :param parent_folder(str): parent folder of the selected host_details
    :param error_message_dict(dict): dictionary containing error details
    :return error_message(str): contains the error message that has been written
    """
    error_folder = os.path.join(os.path.join(parent_folder, "Error_Folder"), "Post_Running_Config_Checks_Results")
    Path(error_folder).mkdir(exist_ok=True, parents=True)

    logging.debug(f"Creating the folder for Node checks namely for Nokia template checks\n{error_folder}")
    error_file = os.path.join(error_folder, "Nokia_Nodes_Post_Running_Config_Checks_Error.txt")

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


def section_running_config_checks(dictionary: dict, ip_node: str, running_config_backup_file_lines: list) -> dict:
    """
    Creates thread for calling section wise modules for Running Config Checks

    :param dictionary(dict):  {'Section Name' : dataframe containing data for the Section}
                                'Section Name' ======> Section name, Example -> VPLS-1, VPLS-2, Layer3, etc.
                                dataframe      ======> Dataframe containing the data in the ip node sheet pertaining to corresponding section key.}
    :param ip_node(str): node ip for which the dictionary is passed as argument.
    :param running_config_backup_file_lines(list): list of lines from pre-running config backup file of the host ip
    :return thread_result_dictionary(dict): {'Section Name' : [list of 'S.No.' where there is any problem in template checks in any of the section] }
                                                    or
                                                empty dictionary ===> {}
    """
    sections = list(dictionary.keys())

    thread_result_dictionary = {}
    i = 0
    while i < len(sections):
        if (len(dictionary[sections[i]]) > 0) and (sections[i] in section_dictionary):
            # Creating a variable to call the module according to section selected in particular iteration
            module_to_be_called = section_dictionary[sections[i]]

            # Creating Thread to call the main_func() of the module corresponding to selected iteration section.
            thread_result_dictionary[sections[i]] = module_to_be_called.main_func(dictionary[sections[i]], ip_node, running_config_backup_file_lines)
        i += 1

    logging.info(f"Got the thread_result_dictionary as \n{thread_result_dictionary} ")
    return thread_result_dictionary


def main_func(**kwargs: dict) -> str:
    """
    Main function for the Nokia running config post checks
    :param kwargs(dict): dictionary containing the ip_hostname_mapping and file_mapping_dictionary
                            ip_hostname_mapping(dict): dictionary containing ip_nodes as keys and hostname as values
                            file_mapping_dictionary(dict): dictionary containing hostnames
    :return flag(str): flag variable containing the status of execution
    """
    global flag
    flag = ''

    ip_hostname_mapping = kwargs['ip_hostname_mapping']
    file_mapping_dictionary = kwargs['file_mapping_dictionary']

    logging.info(f"ip_hostname_mapping := \n{'\n'.join([f'{key}: {value}' for key, value in ip_hostname_mapping.items()])}")
    logging.info(f"file_mapping_dictionary :=\n{'\n'.join([f'{key}: {value}' for key, value in file_mapping_dictionary.items()])}")

    username = os.popen(cmd='cmd.exe /C "echo %username%"').read().strip()
    pickle_path = rf"C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\Vendor_pickles\\NOKIA.pickle"

    global section_dictionary
    section_dictionary = {
        'VPLS-1': importlib.import_module("Main_application.Nokia.Nokia_Section_Running_Config_Checks_Post.VPLS_1_nc_post"),
        'VPLS-2': importlib.import_module("Main_application.Nokia.Nokia_Section_Running_Config_Checks_Post.VPLS_2_nc_post")
    }

    try:
        if not os.path.exists(pickle_path):
            raise CustomException(title='Nokia_Pickle File Missing',
                                  message='Nokia Design Input Pickle File Not Found!')

        with open(pickle_path, "rb") as f:
            nokia_design_input_data = pickle.load(f)
            f.close()

        del f

        thread_result_dictionary = {}

        ip_hostname_mapping_ips = list(ip_hostname_mapping.keys())
        i = 0
        while i < len(ip_hostname_mapping_ips):
            selected_ip = ip_hostname_mapping_ips[i]
            file_to_be_open = file_mapping_dictionary[ip_hostname_mapping[selected_ip]]

            with open(file_to_be_open, 'r') as f:
                running_config_backup_file_lines = f.readlines()
                f.close()
            del f

            thread_result_dictionary[selected_ip] = section_running_config_checks(dictionary=nokia_design_input_data[selected_ip],
                                                                                  ip_node=selected_ip,
                                                                                  running_config_backup_file_lines=running_config_backup_file_lines)
            i += 1

        error_message_dict = {}

        i = 0
        while i < len(ip_hostname_mapping_ips):
            selected_ip = ip_hostname_mapping_ips[i]
            result_from_thread = thread_result_dictionary[selected_ip]

            logging.debug(
                f"Nokia ===> {selected_ip} ====> {result_from_thread =}"
            )

            if result_from_thread is None:
                raise CustomException(title="Exception Occurred!",
                                      message="Could not parse data!")

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

        host_details_file_path = rf'C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\host_details_file_path.txt'
        parent_folder = ''
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
        flag = 'Unsuccessful'

    except Exception as e:
        logging.error(f"Exception Occurred!=>\nTitle==>{e.__class__.__name__}\nMessage==>{str(e)}")
        messagebox.showerror(title="Exception Occurred!",
                             message=str(e))
        flag = 'Unsuccessful'

    finally:
        logging.info(f"Returning flag variable=> {flag}")
        logging.shutdown()
        return flag
