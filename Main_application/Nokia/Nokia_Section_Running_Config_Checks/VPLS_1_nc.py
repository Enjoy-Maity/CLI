import logging
import traceback

import pandas as pd
import re

from CustomThread import CustomThread
from Main_application.file_lines_handler import File_lines_handler as flh
from tkinter import messagebox

service_file_lines_list_block = []
port_details_file_lines_list_block = []
lag_details_file_lines_list_block = []
mesh_sdp_lines_start_lines = []
sdp_starting_start_lines = []
sdp_existence_status_dictionary = {}
sap_lag_starting_lines_from_service_lines_chunk = []
sap_starting_lines_from_service_lines_chunk = []


# exception_raised = False


def sap_without_lag_add_dataframe_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Performs the checks for sap without a lag section on Sequence Add action dataframe

    Args:
        dataframe (pd.DataFrame): _description_ : dataframe containing the input details for which the checks are needed
        ip_node (str): _description_ : ip node for which the checks are being performed

    Returns:
        sap_without_lag_add_dataframe_checks_result_dictionary (dict): _description_ : returns the list of serial numbers with reason
    """
    # logging.basicConfig(filename=log_file,
    #                     filemode='a',
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt="%d-%b-%Y %I:%M:%S %p",
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)

    logging.debug("Running the sap_without_lag_add_dataframe_checks_func for ip_node \'{ip_node}\'")

    global sap_starting_lines_from_service_lines_chunk
    global port_details_file_lines_list_block

    compiled_pattern = re.compile(pattern=r"[sap,\s,lag]+([esat\-,esat \-,\s,\d,/)]+)")
    second_compiled_pattern = re.compile

    logging.info(f'sap_starting_lines_from_service_lines_chunk=>\n{'\n'.join(sap_starting_lines_from_service_lines_chunk)}')
    sap_without_lag_add_dataframe_checks_result_dictionary = {}

    reason = "Port-Detail not found or configured as access. So, wrong Sap entry found in template"
    reason2 = "Given Sap entry (without LAG) clash found"

    if (isinstance(port_details_file_lines_list_block, list)) and (isinstance(sap_starting_lines_from_service_lines_chunk, list)):
        i = 0
        while i < len(dataframe):
            # selected_port_details_input_from_dataframe = (dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")]).split()[1]
            selected_port_details_input_from_dataframe = str(dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")])
            pattern_extract = re.search(compiled_pattern, selected_port_details_input_from_dataframe)

            selected_port_details_input_from_dataframe = re.sub(pattern= r"\s", repl= "", string= pattern_extract.group(1))

            if len(selected_port_details_input_from_dataframe) == 0:
                sap_without_lag_add_dataframe_checks_result_dictionary[reason] = int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
                continue

            logging.info(f"{ip_node}: - {selected_port_details_input_from_dataframe = }")
            selected_detail_input_from_dataframe = dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")]

            port_status = False
            port_status_index = 0
            port_mode_status = ""

            j = 0
            while j < len(port_details_file_lines_list_block):
                if port_details_file_lines_list_block[j].startswith(f"port {selected_port_details_input_from_dataframe}"):
                    port_status = True
                    port_status_index = j

                if port_status and (j > port_status_index):
                    if port_details_file_lines_list_block[j].startswith("mode"):
                        port_mode_status = port_details_file_lines_list_block[j].split()[1].strip()

                    if port_details_file_lines_list_block[j].lower() == "exit":
                        break
                j += 1

            if not port_status:
                if reason not in sap_without_lag_add_dataframe_checks_result_dictionary:
                    sap_without_lag_add_dataframe_checks_result_dictionary[reason] = []
                    sap_without_lag_add_dataframe_checks_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                else:
                    sap_without_lag_add_dataframe_checks_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                i += 1
                continue

            if port_status and (port_mode_status == "access"):
                if selected_detail_input_from_dataframe.__contains__(":"):
                    if len(selected_detail_input_from_dataframe.split(":")[1].strip()) == 0:
                        if reason not in sap_without_lag_add_dataframe_checks_result_dictionary:
                            sap_without_lag_add_dataframe_checks_result_dictionary[reason] = []
                            sap_without_lag_add_dataframe_checks_result_dictionary[reason].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
                        else:
                            sap_without_lag_add_dataframe_checks_result_dictionary[reason].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
                else:
                    if reason not in sap_without_lag_add_dataframe_checks_result_dictionary:
                        sap_without_lag_add_dataframe_checks_result_dictionary[reason] = []
                        sap_without_lag_add_dataframe_checks_result_dictionary[reason].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
                    else:
                        sap_without_lag_add_dataframe_checks_result_dictionary[reason].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

                i += 1
                continue

            not_selected_port_details_input_from_dataframe_found_status = False
            logging.info(f"{ip_node}: - Checking for {selected_detail_input_from_dataframe =}")
            k = 0
            while k < len(sap_starting_lines_from_service_lines_chunk):
                if sap_starting_lines_from_service_lines_chunk[k].strip().startswith(selected_detail_input_from_dataframe):
                    not_selected_port_details_input_from_dataframe_found_status = True
                    break
                k += 1

            if not_selected_port_details_input_from_dataframe_found_status:
                if reason2 not in sap_without_lag_add_dataframe_checks_result_dictionary:
                    sap_without_lag_add_dataframe_checks_result_dictionary[reason2] = []
                    sap_without_lag_add_dataframe_checks_result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                else:
                    sap_without_lag_add_dataframe_checks_result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            i += 1

        logging.debug(f"Returning result_dictionary from sap_without_lag_add_dataframe_checks_func for VPLS-1 for ip_node ==> {ip_node}")

    return sap_without_lag_add_dataframe_checks_result_dictionary


def sap_without_lag_delete_dataframe_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Performs the checks for sap without a lag section on Sequence Delete action dataframe

    Args:
        dataframe (pd.DataFrame): _description_ : dataframe containing the input details for which the checks are needed
        ip_node (str): _description_ : ip node for which the checks are being performed

    Returns:
        sap_without_lag_delete_dataframe_checks_result_dictionary (dict): _description_ : returns the list of serial numbers with reason
    """
    # logging.basicConfig(filename=log_file,
    #                     filemode='a',
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt="%d-%b-%Y %I:%M:%S %p",
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)

    logging.debug(f"Running the sap_without_lag_delete_dataframe_checks_func for ip_node \'{ip_node}\'")
    sap_without_lag_delete_dataframe_checks_result_dictionary = {}
    global sap_starting_lines_from_service_lines_chunk
    global port_details_file_lines_list_block

    compiled_pattern = re.compile(pattern= r"[sap,\s,lag]+([esat\-,esat \-,\s,\d,/)]+)")

    reason = "Given Sap Entry (without LAG) Not Found"
    reason2 = "Port-Detail not found or configured as access. So, wrong Sap entry found"

    if (isinstance(port_details_file_lines_list_block, list)) and (isinstance(sap_starting_lines_from_service_lines_chunk, list)):
        i = 0
        while i < len(dataframe):
            # selected_port_details_from_dataframe_input = (dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")]).strip().split()[1].strip().split(':')[0]

            selected_port_details_from_dataframe_input = str(dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")])
            pattern_extract = re.search(compiled_pattern, selected_port_details_from_dataframe_input)

            selected_port_details_from_dataframe_input = re.sub(pattern=r"\s", repl="", string=pattern_extract.group(1))

            if len(selected_port_details_from_dataframe_input) == 0:
                sap_without_lag_delete_dataframe_checks_result_dictionary[reason2] = int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
                continue

            selected_sap_details_from_dataframe_input = dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")].strip()
            selected_port_status = False
            selected_port_mode_status = ""
            selected_port_line_index = 0

            j = 0
            while j < len(port_details_file_lines_list_block):
                selected_port_status = False
                if port_details_file_lines_list_block[j].startswith(f"port {selected_port_details_from_dataframe_input}"):
                    selected_port_status = True
                    selected_port_line_index = j

                if selected_port_status and (j > selected_port_line_index):
                    if port_details_file_lines_list_block[j].startswith("mode"):
                        selected_port_mode_status = (port_details_file_lines_list_block[j]).split()[1].strip()

                    if port_details_file_lines_list_block[j].lower() == "exit":
                        break

                j += 1

            if not selected_port_status:
                if reason2 not in sap_without_lag_delete_dataframe_checks_result_dictionary:
                    sap_without_lag_delete_dataframe_checks_result_dictionary[reason2] = []
                    sap_without_lag_delete_dataframe_checks_result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

                else:
                    sap_without_lag_delete_dataframe_checks_result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

                i += 1
                continue

            if selected_port_status and (selected_port_mode_status.lower() == "access"):
                if selected_sap_details_from_dataframe_input.__contains__(":"):
                    if len(selected_sap_details_from_dataframe_input.split(":")[1].strip()) == 0:
                        if reason2 not in sap_without_lag_delete_dataframe_checks_result_dictionary:
                            sap_without_lag_delete_dataframe_checks_result_dictionary[reason2] = []
                            sap_without_lag_delete_dataframe_checks_result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
                        else:
                            sap_without_lag_delete_dataframe_checks_result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

                        i += 1
                        continue
                else:
                    if reason2 not in sap_without_lag_delete_dataframe_checks_result_dictionary:
                        sap_without_lag_delete_dataframe_checks_result_dictionary[reason2] = []
                        sap_without_lag_delete_dataframe_checks_result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

                    else:
                        sap_without_lag_delete_dataframe_checks_result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

                i += 1
                continue

            selected_sap_details_from_dataframe_input_found = False

            k = 0
            while k < len(sap_starting_lines_from_service_lines_chunk):
                if sap_starting_lines_from_service_lines_chunk[k].strip().startswith(selected_sap_details_from_dataframe_input):
                    selected_sap_details_from_dataframe_input_found = True
                    break
                k += 1

            if not selected_sap_details_from_dataframe_input_found:
                if reason not in sap_without_lag_delete_dataframe_checks_result_dictionary:
                    sap_without_lag_delete_dataframe_checks_result_dictionary[reason] = []
                    sap_without_lag_delete_dataframe_checks_result_dictionary[reason].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

                else:
                    sap_without_lag_delete_dataframe_checks_result_dictionary[reason].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
            i += 1

    logging.info(
        f"Returning result_dictionary from sap_without_lag_delete_dataframe_checks_func for VPLS-1 for ip_node ==> \'{ip_node}\'\n{'\n'.join([f'{key}: {value}' for key, value in sap_without_lag_delete_dataframe_checks_result_dictionary.items()])}")

    return sap_without_lag_delete_dataframe_checks_result_dictionary


def lag_add_action_dataframe_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Performs the checks for lag section on Sequence Add action dataframe

    Args:
        dataframe (pd.DataFrame): _description_ : dataframe containing the input details for which the checks are needed
        ip_node (str): _description_ : ip node for which the checks are being performed

    Returns:
        lag_add_action_dataframe_check_result_dictionary (dict): _description_ : returns the list of serial numbers with reason
    """
    # logging.basicConfig(filename=log_file,
    #                     filemode='a',
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt="%d-%b-%Y %I:%M:%S %p",
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)

    logging.debug(f"Running the lag_add_action_dataframe_checks_func for ip_node \'{ip_node}\'")
    lag_add_action_check_result_dictionary = {}
    global lag_details_file_lines_list_block
    global sap_lag_starting_lines_from_service_lines_chunk

    if isinstance(sap_lag_starting_lines_from_service_lines_chunk, list):
        logging.info(f"{ip_node}: -sap_lag_starting_lines_from_service_lines_chunk ==> \n{'\n'.join(sap_lag_starting_lines_from_service_lines_chunk)}")
    # print(lag_details_file_lines_list_block)

    logging.info(f"starting checks for Add Section lag details check for VPLS-1 of {ip_node}")
    compiled_pattern = re.compile(pattern=r"\d+")

    reason = "Lag not found or configured as access. So, wrong Sap entry found in input template"
    reason2 = "Given Sap entry (with LAG) clash found"

    i = 0
    while i < len(dataframe):
        selected_sap_lag_variable = dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")]
        lag_in_selected_variable = re.findall(pattern=compiled_pattern,
                                              string=selected_sap_lag_variable)[0]
        logging.info(f"{ip_node}:-  got the lag selected as \'{lag_in_selected_variable}\' for vpls_id \'{dataframe.iloc[i, dataframe.columns.get_loc(r"VPLS ID")]}\'")
        lag_status = False
        lag_mode_status = ""

        logging.info(f"{ip_node}:- Starting loop")
        lag_status_index = 0
        j = 0
        while j < len(lag_details_file_lines_list_block):
            if lag_details_file_lines_list_block[j].strip().startswith(f"lag {lag_in_selected_variable}"):
                logging.info(f"{ip_node}:- lag found for \'{lag_in_selected_variable}\' for vpls_id \'{dataframe.iloc[i, dataframe.columns.get_loc(r"VPLS ID")]}\'")
                lag_status = True
                lag_status_index = j

            if lag_status and (j > lag_status_index):
                if lag_details_file_lines_list_block[j].startswith(f"mode"):
                    lag_mode_status = lag_details_file_lines_list_block[j].split()[1].strip()
                    logging.info(
                        f"{ip_node}:- lag status mode found \'{lag_mode_status}\' for \'{lag_in_selected_variable}\' for vpls_id \'{dataframe.iloc[i, dataframe.columns.get_loc("VPLS ID")]}\'")

                if lag_details_file_lines_list_block[j].lower() == 'exit':
                    break

            j += 1

        if not lag_status:
            logging.info(f"{ip_node}: - lag \'{lag_in_selected_variable}\' not found for {dataframe.iloc[i, dataframe.columns.get_loc("VPLS ID")]}")
            logging.info(f"{ip_node}: - {lag_add_action_check_result_dictionary.keys() =}")
            logging.info(f"{ip_node}: - {(reason not in lag_add_action_check_result_dictionary) =}")
            if reason not in lag_add_action_check_result_dictionary:
                lag_add_action_check_result_dictionary[reason] = []
                lag_add_action_check_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            else:
                lag_add_action_check_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            i += 1

            continue

        if lag_status and (lag_mode_status == "access"):
            if selected_sap_lag_variable.__contains__(":"):
                if len(selected_sap_lag_variable.split(":")[1].strip()) == 0:
                    logging.info(
                        f"{ip_node}:- wrong sap_lag entry found for 'access' mode found \'{selected_sap_lag_variable}\' for \'{lag_in_selected_variable}\' for vpls_id \'{dataframe.iloc[i, dataframe.columns.get_loc(r"VPLS ID")]}\'")
                    if reason not in lag_add_action_check_result_dictionary:
                        lag_add_action_check_result_dictionary[reason] = []
                        lag_add_action_check_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                    else:
                        lag_add_action_check_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                    i += 1

                    continue
            else:
                logging.info(
                    f"{ip_node}:- wrong sap_lag entry found for 'access' mode found \'{selected_sap_lag_variable}\' without \'vpls details\'\nfor \'{lag_in_selected_variable}\' for vpls_id \'{dataframe.iloc[i, dataframe.columns.get_loc(r"VPLS ID")]}\'")
                if reason not in lag_add_action_check_result_dictionary:
                    lag_add_action_check_result_dictionary[reason] = []
                    lag_add_action_check_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                else:
                    lag_add_action_check_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                i += 1

                continue

        selected_sap_lag_variable_founding_status = False
        logging.info(f"{ip_node}: - Finding {selected_sap_lag_variable} in sap_lag_starting_lines_from_service_lines_chunk")

        k = 0
        while k < len(sap_lag_starting_lines_from_service_lines_chunk):
            if sap_lag_starting_lines_from_service_lines_chunk[k].startswith(selected_sap_lag_variable):
                logging.info(f'{ip_node}: - Setting selected sap founding status value as False for \'{dataframe.iloc[i, dataframe.columns.get_loc('VPLS ID')]}\'\n')
                selected_sap_lag_variable_founding_status = True
                break
            k += 1

        if selected_sap_lag_variable_founding_status:
            logging.info(f'{ip_node}: - selected sap founded  for \'{dataframe.iloc[i, dataframe.columns.get_loc('VPLS ID')]}\'\nSo, adding to result dictionary\n')
            if reason2 not in lag_add_action_check_result_dictionary:
                lag_add_action_check_result_dictionary[reason2] = []
                lag_add_action_check_result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            else:
                lag_add_action_check_result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))
        logging.info(
            f"{ip_node}: - got the lag_add_action_check_result_dictionary as {lag_add_action_check_result_dictionary} for iteration {i}"
        )
        i += 1

    logging.debug(f"Returning lag_add_action_check_result_dictionary from lag_add_action_dataframe_checks_func for VPLS-1 for ip_node ==> {ip_node}\n{lag_add_action_check_result_dictionary}\n")

    return lag_add_action_check_result_dictionary


def lag_delete_action_dataframe_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Performs the checks for lag section on Sequence Delete action dataframe

    Args:
        dataframe (pd.DataFrame): _description_ : dataframe containing the input details for which the checks are needed
        ip_node (str): _description_ : ip node for which the checks are being performed

    Returns:
        lag_delete_action_dataframe_checks_result_dictionary (dict): _description_ : returns the list of serial numbers with reason
    """
    # logging.basicConfig(filename=log_file,
    #                     filemode='a',
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt="%d-%b-%Y %I:%M:%S %p",
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)

    logging.debug("Running the lag_delete_action_dataframe_checks_func for ip_node \'{ip_node}\'")
    lag_delete_action_dataframe_checks_result_dictionary = {}
    global lag_details_file_lines_list_block
    global sap_lag_starting_lines_from_service_lines_chunk
    # print(lag_details_file_lines_list_block)
    reason = "Given Sap Entry (with LAG) Not Found"
    reason2 = "LAG Entry Not Found"

    compiled_pattern = re.compile(pattern=r"\d+")

    if (isinstance(lag_details_file_lines_list_block, list)) and (isinstance(sap_lag_starting_lines_from_service_lines_chunk, list)):
        i = 0
        while i < len(dataframe):
            selected_sap_lag_variable = dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")]
            lag_in_selected_variable = re.findall(pattern=compiled_pattern,
                                                  string=selected_sap_lag_variable)[0]

            lag_status = False
            lag_mode_status = ""

            lag_status_index = 0
            # print(lag_details_file_lines_list_block)
            j = 0
            while j < len(lag_details_file_lines_list_block):
                if lag_details_file_lines_list_block[j].strip().startswith(f"lag {lag_in_selected_variable}"):
                    lag_status = True
                    lag_status_index = j

                if lag_status and (j > lag_status_index):
                    if lag_details_file_lines_list_block[j].startswith(f"mode"):
                        lag_mode_status = lag_details_file_lines_list_block[j].strip().split("")[1]

                    if lag_details_file_lines_list_block[j].lower() == 'exit':
                        break

                j += 1

            if not lag_status:
                if reason2 not in lag_delete_action_dataframe_checks_result_dictionary:
                    lag_delete_action_dataframe_checks_result_dictionary[reason2] = []
                    lag_delete_action_dataframe_checks_result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

                else:
                    lag_delete_action_dataframe_checks_result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

                i += 1

                continue

            if lag_status and (lag_mode_status == "access"):
                if selected_sap_lag_variable.__contains__(":"):
                    if len(selected_sap_lag_variable.split(":")[1].strip()) == 0:
                        if reason2 not in lag_delete_action_dataframe_checks_result_dictionary:
                            lag_delete_action_dataframe_checks_result_dictionary[reason2] = []
                            lag_delete_action_dataframe_checks_result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                        else:
                            lag_delete_action_dataframe_checks_result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                        i += 1
                        continue
                else:
                    if reason2 not in lag_delete_action_dataframe_checks_result_dictionary:
                        lag_delete_action_dataframe_checks_result_dictionary[reason2] = []
                        lag_delete_action_dataframe_checks_result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                    else:
                        lag_delete_action_dataframe_checks_result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                    i += 1
                    continue

            selected_sap_lag_variable_founding_status = False

            k = 0
            while k < len(sap_lag_starting_lines_from_service_lines_chunk):
                if sap_lag_starting_lines_from_service_lines_chunk[k].startswith(selected_sap_lag_variable):
                    selected_sap_lag_variable_founding_status = True
                    break
                k += 1

            if not selected_sap_lag_variable_founding_status:
                if reason not in lag_delete_action_dataframe_checks_result_dictionary:
                    lag_delete_action_dataframe_checks_result_dictionary[reason] = []
                    lag_delete_action_dataframe_checks_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                else:
                    lag_delete_action_dataframe_checks_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            i += 1

    logging.debug(
        f"Returning result_dictionary from lag_delete_action_dataframe_checks_func for VPLS-1 for ip_node ==> \'{ip_node}\':\n{'\n'.join([f'{key}: {value}' for key, value in lag_delete_action_dataframe_checks_result_dictionary.items()])}")
    return lag_delete_action_dataframe_checks_result_dictionary


def sdp_checks_add_dataframe_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Checks for the sdp checks for the add sequence action

    Args:
        dataframe (pd.DataFrame): _description_ : dataframe containing the input details for which the checks are needed.
        ip_node (str): _description_ : ip node for which the checks are being performed
        
    return result_dictionary
        sdp_checks_add_dataframe_result_dictionary (dict): _description_ : returns the list of serial numbers with reason
    """
    # logging.basicConfig(filename=log_file,
    #                     filemode='a',
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt="%d-%b-%Y %I:%M:%S %p",
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)

    logging.debug("Running the sdp_checks_add_dataframe_func for ip_node \'{ip_node}\'")
    sdp_checks_add_dataframe_result_dictionary = {}
    global sdp_starting_start_lines
    global mesh_sdp_lines_start_lines

    reason = "Given Mesh-SDP clash found"
    # reason2 = ""

    compiled_digits_pattern = re.compile(pattern=r"\d+")

    if (isinstance(sdp_starting_start_lines, list)) and (isinstance(mesh_sdp_lines_start_lines, list)):
        i = 0
        while i < len(dataframe):
            mesh_sdp_digit_variable = (re.findall(pattern=compiled_digits_pattern,
                                                  string=dataframe.iloc[i, dataframe.columns.get_loc("Mesh-sdp")]))[0]

            mesh_input_from_dataframe = (dataframe.iloc[i, dataframe.columns.get_loc("Mesh-sdp")]).lower()
            mesh_sdp_input_status = False

            j = 0
            while j < len(sdp_starting_start_lines):
                if sdp_starting_start_lines[j].strip().startswith(f"sdp {mesh_sdp_digit_variable}"):
                    sdp_existence_status_dictionary[f"sdp {mesh_sdp_digit_variable}"] = "Found"
                    break
                j += 1

            if not f"sdp {mesh_sdp_digit_variable}" in sdp_existence_status_dictionary:
                if isinstance(sdp_existence_status_dictionary, dict):
                    sdp_existence_status_dictionary[f"sdp {mesh_sdp_digit_variable}"] = "Not Found"

            k = 0
            while k < len(mesh_sdp_lines_start_lines):
                if mesh_sdp_lines_start_lines[k].strip().startswith(mesh_input_from_dataframe):
                    mesh_sdp_input_status = True
                    break
                k += 1

            if mesh_sdp_input_status:
                if reason not in sdp_checks_add_dataframe_result_dictionary:
                    sdp_checks_add_dataframe_result_dictionary[reason] = []
                    sdp_checks_add_dataframe_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                else:
                    sdp_checks_add_dataframe_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            i += 1

    logging.info(f"{ip_node}: -\n{'\n'.join([f'{key} : {value}' for key, value in sdp_existence_status_dictionary.items()])}")

    logging.debug(
        f"Returning the result_dictionary from sdp_checks_add_dataframe_func for ip_node \'{ip_node}\':\n\'{'\n'.join([f'{key}:{value}' for key, value in sdp_checks_add_dataframe_result_dictionary.items()])}")
    return sdp_checks_add_dataframe_result_dictionary


def sdp_checks_delete_dataframe_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Checks for the sdp checks for the delete sequence action

    Args:
        dataframe (pd.DataFrame): _description_ : dataframe containing the input details for which the checks are needed.
        ip_node (str): _description_ : ip node for which the checks are being performed
        
    return result_dictionary
        sdp_checks_delete_dataframe_result_dictionary (dict): _description_ : returns the list of serial numbers with reason
    """
    # logging.basicConfig(filename=log_file,
    #                     filemode='a',
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt="%d-%b-%Y %I:%M:%S %p",
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)

    logging.debug("Running the sdp_checks_delete_dataframe_func for ip_node \'{ip_node}\'")
    sdp_checks_delete_dataframe_result_dictionary = {}
    global sdp_starting_start_lines
    global mesh_sdp_lines_start_lines

    reason = "Given Mesh-SDP not found"

    compiled_digits_pattern = re.compile(pattern=r"\d+")

    if (isinstance(sdp_starting_start_lines, list)) and (isinstance(mesh_sdp_lines_start_lines, list)):
        i = 0
        while i < len(dataframe):
            mesh_sdp_digit_variable = (re.findall(pattern=compiled_digits_pattern,
                                                  string=dataframe.iloc[i, dataframe.columns.get_loc("Mesh-sdp")]))[0]

            mesh_input_from_dataframe = (dataframe.iloc[i, dataframe.columns.get_loc("Mesh-sdp")]).lower()
            mesh_sdp_input_status = False

            j = 0
            while j < len(sdp_starting_start_lines):
                if sdp_starting_start_lines[j].strip().startswith(f"sdp {mesh_sdp_digit_variable}"):
                    if isinstance(sdp_existence_status_dictionary, dict):
                        sdp_existence_status_dictionary[f"sdp {mesh_sdp_digit_variable}"] = "Found"
                        break
                j += 1

            if not f"sdp {mesh_sdp_digit_variable}" in sdp_existence_status_dictionary:
                reason = "Given 'S:Delete' sdp not found"
                sdp_existence_status_dictionary[f"sdp {mesh_sdp_digit_variable}"] = "Not Found"

                if reason not in sdp_checks_delete_dataframe_result_dictionary:
                    sdp_checks_delete_dataframe_result_dictionary[reason] = []
                    sdp_checks_delete_dataframe_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                else:
                    sdp_checks_delete_dataframe_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                i += 1

                continue

            k = 0
            while k < len(mesh_sdp_lines_start_lines):
                if mesh_sdp_lines_start_lines[k].strip().startswith(mesh_input_from_dataframe):
                    mesh_sdp_input_status = True
                    break
                k += 1

            if not mesh_sdp_input_status:
                if reason not in sdp_checks_delete_dataframe_result_dictionary:
                    sdp_checks_delete_dataframe_result_dictionary[reason] = []
                    sdp_checks_delete_dataframe_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                else:
                    sdp_checks_delete_dataframe_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            i += 1

    logging.debug(
        f"Returning the result_dictionary from sdp_checks_delete_dataframe_func for ip_node \'{ip_node}\':\n\'{'\n'.join([f'{key}:{value}' for key, value in sdp_checks_delete_dataframe_result_dictionary.items()])}")
    return sdp_checks_delete_dataframe_result_dictionary


def add_action_checks(dataframe: pd.DataFrame, running_config_backup_file_lines: list, ip_node: str, vpls_id_starter_lines_filter: list) -> dict:
    """
        Performs the Checks for the presence of VPLS ID in the running config backup files
        
        Arguments: (dataframe, running_config_backup_file_lines, ip_node, vpls_id_starter_lines_filter)
            dataframe ===> pandas.DataFrame
                description =====> filtered dataframe with Action "A:Add" from the node ip Section dataframe
            
            running_config_backup_file_lines ===> list
                description =====> List of lines from running config backup lines
                
            ip_node ===> str
                description =====> Node IP for which the checks are being done
                
            vpls_id_starter_lines_filter ===> list
                description =====> list of lines starting with vpls keyword
        
        return result_dictionary
            add_action_checks_result_dictionary ===> dict
                description =====> dictionary containing the error results
                                    dictionary structure => {
                                                                error_reason: [list of S.No. with the errors]
                                                            }
                                                            or 
                                                            empty dictionary -> {}
    """
    # global log_file;
    # logging.basicConfig(filename=log_file,
    #                     filemode='a',
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt="%d-%b-%Y %I:%M:%S %p",
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)
    logging.debug(f"inside {__name__} for ip_node ==> {ip_node}")

    logging.debug(f"got the dataframe for ip_node {ip_node} =>\n{dataframe.to_markdown()}")
    add_action_checks_result_dictionary = {}

    reason = "Action:Add, VPLS ID Clash found"
    reason2 = "VPLS Name Clash found"

    if str(dataframe.iloc[0, dataframe.columns.get_loc('MPBN Node Type ( Router/Switch )')]).strip().lower() == 'router':
        # print(ip_node, "inside router condition")
        i = 0
        while i < len(dataframe):
            vpls_id_to_be_searched = ''
            vpls_name_to_be_searched = str(dataframe.iloc[i, dataframe.columns.get_loc("VPLS Name")])
            vpls_id_status = False
            vpls_name_status = False

            if isinstance(dataframe.iloc[i, dataframe.columns.get_loc("VPLS ID")], (int | float)):
                vpls_id_to_be_searched = int(dataframe.iloc[i, dataframe.columns.get_loc("VPLS ID")])
            else:
                vpls_id_to_be_searched = int(str(dataframe.iloc[i, dataframe.columns.get_loc("VPLS ID")]).strip())

            j = 0
            while j < len(vpls_id_starter_lines_filter):

                if vpls_id_starter_lines_filter[j].startswith(f"vpls {vpls_id_to_be_searched} "):
                    logging.info(f"Clash found for {vpls_id_to_be_searched} for \'ADD\' action for ip node \'{ip_node}\'")
                    vpls_id_status = True
                    if reason not in add_action_checks_result_dictionary:
                        add_action_checks_result_dictionary[reason] = []
                        add_action_checks_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                    else:
                        add_action_checks_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                if vpls_id_starter_lines_filter[j].__contains__(vpls_name_to_be_searched):
                    logging.info(f"Clash found for {vpls_name_to_be_searched} for \'ADD\' action for ip node \'{ip_node}\'")
                    vpls_name_status = True
                    if reason2 not in add_action_checks_result_dictionary:
                        add_action_checks_result_dictionary[reason2] = []
                        add_action_checks_result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc('S.No.')]))

                    else:
                        add_action_checks_result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc('S.No.')]))

                if vpls_id_status or vpls_name_status:
                    break

                j += 1
            i += 1

    if str(dataframe.iloc[0, dataframe.columns.get_loc('MPBN Node Type ( Router/Switch )')]).strip().lower() == 'switch':
        # print("Inside Switch condition")
        service_name_lines_filter_list = flh().file_lines_starter_filter(file_lines_list=running_config_backup_file_lines,
                                                                         start_word="service-name ")
        logging.debug(f"service name lines filter list\n{'\n'.join(service_name_lines_filter_list)}")

        i = 0
        while i < len(dataframe):
            vpls_id_to_be_searched = ''
            vpls_name_to_be_searched = str(dataframe.iloc[i, dataframe.columns.get_loc("VPLS Name")])

            if isinstance(dataframe.iloc[i, dataframe.columns.get_loc("VPLS ID")], (int | float)):
                vpls_id_to_be_searched = int(dataframe.iloc[i, dataframe.columns.get_loc("VPLS ID")])
            else:
                vpls_id_to_be_searched = int(str(dataframe.iloc[i, dataframe.columns.get_loc("VPLS ID")]).strip())

            j = 0
            while j < len(vpls_id_starter_lines_filter):
                if vpls_id_starter_lines_filter[j].startswith(f"vpls {vpls_id_to_be_searched} "):
                    logging.info(f"Clash found for {vpls_id_to_be_searched} for \'ADD\' action for ip node \'{ip_node}\'")
                    if reason not in add_action_checks_result_dictionary:
                        add_action_checks_result_dictionary[reason] = []
                        add_action_checks_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                    else:
                        add_action_checks_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))
                    break
                j += 1

            j = 0
            while j < len(service_name_lines_filter_list):
                if service_name_lines_filter_list[j].startswith(f"service-name \"{vpls_name_to_be_searched}\""):
                    logging.info(f"Clash found for {vpls_name_to_be_searched} for \'ADD\' action for ip node \'{ip_node}\'")
                    if reason2 not in add_action_checks_result_dictionary:
                        add_action_checks_result_dictionary[reason2] = []
                        add_action_checks_result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

                    else:
                        add_action_checks_result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))
                    break
                j += 1
            i += 1

    logging.debug(
        f"Returning the result_dictionary from add_action_checks for ip_node \'{ip_node}\' :\n\'{'\n'.join([f'{key}:{value}' for key, value in add_action_checks_result_dictionary.items()])}")
    return add_action_checks_result_dictionary


def modify_delete_action_checks(dataframe: pd.DataFrame, running_config_backup_file_lines: list, ip_node: str, vpls_id_starter_lines_filter: list):
    """
        Performs the checks for the presence of SDP variable in the running config backup files
        
        Arguments: (dataframe, running_config_backup_file_lines, ip_node, vpls_id_starter_lines_filter)
        dataframe ===> pandas.DataFrame
                description =====> filtered dataframe with Action "A:Modify/Delete" from the node ip Section dataframe
            
            running_config_backup_file_lines ===> list
                description =====> List of lines from running config backup lines
                
            ip_node ===> str
                description =====> Node IP for which the checks are being done
            
            vpls_id_starter_lines_filter ===> list
                description =====> list of lines starting with vpls keyword
        
        return result_dictionary
            modify_delete_action_checks_result_dictionary ===> dict
                description =====> dictionary containing the error results
                                    dictionary structure => {
                                                                error_reason: [list of S.No. with the errors]
                                                            }
                                                            or 
                                                            empty dictionary -> {}
    """
    # logging.basicConfig(filename=log_file,
    #                     filemode='a',
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt="%d-%b-%Y %I:%M:%S %p",
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)

    logging.debug(f"Running modify_delete_action_checks for ip_node {ip_node}")

    modify_delete_action_checks_result_dictionary = {}

    if str(ip_node).endswith('93'):
        logging.info(f"{ip_node}: -vpls_id_starter_lines_filter =>\n{'\n'.join(vpls_id_starter_lines_filter)}")

    reason = "Action:Modify, VPLS ID not found"

    i = 0
    while i < len(dataframe):
        vpls_id_to_be_searched = int(dataframe.iloc[i, dataframe.columns.get_loc("VPLS ID")])
        j = 0
        flag = False
        while j < len(vpls_id_starter_lines_filter):
            if vpls_id_starter_lines_filter[j].startswith(f"vpls {vpls_id_to_be_searched} "):
                flag = True
                break
            j += 1

        if not flag:
            if reason not in modify_delete_action_checks_result_dictionary:
                modify_delete_action_checks_result_dictionary[reason] = []
                modify_delete_action_checks_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            else:
                modify_delete_action_checks_result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))
        i += 1

    if len(modify_delete_action_checks_result_dictionary) > 0:
        logging.debug(f"Returning the result_dictionary from modify_delete_action_checks :\n\'{'\n'.join([f'{key}:{value}' for key, value in modify_delete_action_checks_result_dictionary.items()])}")

    else:
        logging.debug(f"Returning the result_dictionary from modify_delete_action_checks :\n\'{modify_delete_action_checks_result_dictionary}")

    return modify_delete_action_checks_result_dictionary


def main_func(dataframe: pd.DataFrame, ip_node: str, running_config_backup_file_lines: list):
    """
        Performs the Node Checks for VPLS 1 
        
        Arguments: (dataframe, ip_node, running_config_backup_file_lines)
            dataframe ===> pandas.DataFrame
                description ======> contains the dataframe(tabular data) for the VPLS-1 Section of given ip_node for running_config checks
                
            ip_node ===> str
                description =====> ip node for which the dataframe is passed
                
            running_config_backup_file_lines ==> list
                description =====> list of lines from running_config_backup_file in which we need to perform checks
                
        return result_dictionary
            result_dictionary ===> dictionary
                description =====> {'Section Name': [list of 'S.No.' where there is any problem in template checks in any of the section] }
                                        or
                                    empty dictionary ===> {}
    """
    # username = (os.popen('cmd.exe /C "echo %username%"').read()).strip()

    # global log_file;
    # log_file = rf"C:/Ericsson_Application_Logs/CLI_Automation_Logs/Running_Config_Checks(Node_Checks).log"
    #
    # logging.basicConfig(filename=log_file,
    #                     filemode='a',
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt="%d-%b-%Y %I:%M:%S %p",
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)

    # dataframe = dataframe.fillna("TempNA")
    result_dictionary = {}

    # declaring all the global variables as None

    global service_file_lines_list_block
    service_file_lines_list_block = None

    global port_details_file_lines_list_block, lag_details_file_lines_list_block, mesh_sdp_lines_start_lines, sdp_starting_start_lines
    global sdp_existence_status_dictionary
    port_details_file_lines_list_block = []
    lag_details_file_lines_list_block = []
    mesh_sdp_lines_start_lines = []
    sdp_starting_start_lines = []
    sdp_existence_status_dictionary = {}

    # global exception_raised
    # exception_raised = False

    global sap_lag_starting_lines_from_service_lines_chunk
    sap_lag_starting_lines_from_service_lines_chunk = []

    global sap_starting_lines_from_service_lines_chunk
    sap_starting_lines_from_service_lines_chunk = []

    dataframe = dataframe.where(~dataframe.isna(), "TempNA")

    # global flag;

    add_action_dataframe = dataframe[dataframe['Action'].str.upper().str.contains("ADD")]
    logging.info(
        f"Created the filtered dataframe for 'ADD' action for VPLS-1 Section for \"{ip_node}\":\n{add_action_dataframe.to_markdown()}"
    )

    modify_delete_action_dataframe = dataframe[dataframe['Action'].str.upper().str.contains("MODIFY|DELETE")]
    logging.debug(f"Got the dataframe for modify/delete action in VPLS-1 =>\n{modify_delete_action_dataframe.to_markdown()}\n")

    vpls_id_starter_lines_filter = flh().file_lines_starter_filter(file_lines_list=running_config_backup_file_lines,
                                                                   start_word="vpls")
    logging.info(f"Got the vpls_id_starter_lines_filter for \"{ip_node}\"=>\n{'\n'.join(vpls_id_starter_lines_filter)}")

    service_file_lines_list_block_thread = CustomThread(target=flh().file_lines_chunk_divisor,
                                                        args=(running_config_backup_file_lines,
                                                              'echo \"Service Configuration\"',
                                                              r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration\"$'))
    # service_file_lines_list_block_thread.daemon = True
    service_file_lines_list_block_thread.start()
    # service_file_lines_list_block = flh().file_lines_chunk_divisor(file_lines_list=running_config_backup_file_lines,
    #                                                                start_string='echo \"Service Configuration\"',
    #                                                                end_string_pattern=r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration\"$')

    logging.info(f"Got the service_file_list_block for \"{ip_node}\"")

    port_details_file_lines_list_block_thread = CustomThread(target=flh().file_lines_chunk_divisor,
                                                             args=(running_config_backup_file_lines,
                                                                   'echo \"Port Configuration\"',
                                                                   r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration"$'))
    # port_details_file_lines_list_block_thread.daemon = True
    port_details_file_lines_list_block_thread.start()
    # port_details_file_lines_list_block = flh().file_lines_chunk_divisor(file_lines_list=running_config_backup_file_lines,
    #                                                                     start_string='echo \"Port Configuration\"',
    #                                                                     end_string_pattern=r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration"$')

    logging.info(f"Got the port_details_file_lines_list_block for \"{ip_node}\"")

    lag_details_file_lines_list_block_thread = CustomThread(target=flh().file_lines_chunk_divisor,
                                                            args=(running_config_backup_file_lines,
                                                                  'echo \"LAG Configuration\"',
                                                                  r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration"$'))
    # lag_details_file_lines_list_block_thread.daemon = True
    lag_details_file_lines_list_block_thread.start()
    # lag_details_file_lines_list_block = flh().file_lines_chunk_divisor(file_lines_list=running_config_backup_file_lines,
    #                                                                    start_string='echo \"LAG Configuration\"',
    #                                                                    end_string_pattern=r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration"$')
    # print(f"Got the lag_details_file_lines_list_block for {ip_node}=>\n [\n\t{'\n\t'.join(lag_details_file_lines_list_block)}\n]")
    logging.info(f"Got the lag_details_file_lines_list_block for \"{ip_node}\"")

    service_file_lines_list_block = service_file_lines_list_block_thread.join()
    port_details_file_lines_list_block = port_details_file_lines_list_block_thread.join()
    lag_details_file_lines_list_block = lag_details_file_lines_list_block_thread.join()

    mesh_sdp_lines_start_lines_thread = CustomThread(target=flh().file_lines_starter_filter,
                                                     args=(service_file_lines_list_block,
                                                           "mesh-sdp "))
    # mesh_sdp_lines_start_lines_thread.daemon = True
    mesh_sdp_lines_start_lines_thread.start()

    sdp_starting_start_lines_thread = CustomThread(target=flh().file_lines_starter_filter,
                                                   args=(service_file_lines_list_block,
                                                         "sdp "))
    # sdp_starting_start_lines_thread.daemon = True
    sdp_starting_start_lines_thread.start()

    mesh_sdp_lines_start_lines = mesh_sdp_lines_start_lines_thread.join()

    if isinstance(mesh_sdp_lines_start_lines, list):
        logging.debug(f"Created file lines filter with lines starting with 'mesh-sdp' for ip_node \'{ip_node}\' with len==>\n{len(mesh_sdp_lines_start_lines)}\n")

    sdp_starting_start_lines = sdp_starting_start_lines_thread.join()

    sap_lag_starting_lines_from_service_lines_chunk_thread = CustomThread(target=flh().file_lines_starter_filter,
                                                                          args=(service_file_lines_list_block,
                                                                                "sap lag-"))
    # flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
    #                                                                               start_word="sap lag-"))
    logging.debug(f"Creating the file_lines_chunk for sap_lag for VPLS-1 for ip_node ==> {ip_node}")
    # sap_lag_starting_lines_from_service_lines_chunk_thread.daemon = True
    sap_lag_starting_lines_from_service_lines_chunk_thread.start()

    sap_starting_lines_from_service_lines_chunk_thread = CustomThread(target=flh().file_lines_starter_filter,
                                                                      args=(service_file_lines_list_block,
                                                                            "sap "))
    # flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
    #                                                                                           start_word="sap ")

    # sap_starting_lines_from_service_lines_chunk_thread.daemon = True
    sap_starting_lines_from_service_lines_chunk_thread.start()

    sap_lag_starting_lines_from_service_lines_chunk = sap_lag_starting_lines_from_service_lines_chunk_thread.join()
    logging.debug(f"Created the sap_lag_starting_file_lines_chunk for sap_lag for VPLS-1 for ip_node ==> {ip_node} with => {len(sap_lag_starting_lines_from_service_lines_chunk) = }\n")

    sap_lag_starting_lines_from_service_lines_chunk = sap_starting_lines_from_service_lines_chunk_thread.join()
    sap_starting_lines_from_service_lines_chunk = sap_starting_lines_from_service_lines_chunk_thread.join()

    try:
        if len(add_action_dataframe) > 0:
            logging.debug(f"Creating the thread for checking the presence of VPLS ID clashes for {ip_node} for the dataframe\n{add_action_dataframe.to_markdown()}\n")
            add_action_result_dictionary_from_main_func = add_action_checks(add_action_dataframe,
                                                                            running_config_backup_file_lines,
                                                                            ip_node,
                                                                            vpls_id_starter_lines_filter)

            if len(result_dictionary) == 0:
                result_dictionary = add_action_result_dictionary_from_main_func

            else:
                result_dictionary.update(add_action_result_dictionary_from_main_func)

        if len(modify_delete_action_dataframe) > 0:
            logging.debug(f"Calling the function for checking the sdp variable for {ip_node} for the dataframe\n{modify_delete_action_dataframe.to_markdown()}\n")
            modify_delete_result_dictionary_from_main_func = modify_delete_action_checks(modify_delete_action_dataframe,
                                                                                         running_config_backup_file_lines,
                                                                                         ip_node,
                                                                                         vpls_id_starter_lines_filter)
            if len(result_dictionary) == 0:
                result_dictionary = modify_delete_result_dictionary_from_main_func

            else:
                result_dictionary.update(modify_delete_result_dictionary_from_main_func)

        mesh_sdp_add_df = dataframe.loc[((~dataframe["Mesh-sdp"].str.startswith("TempNA")) & (dataframe["Sequence"].str.upper().str.endswith("ADD")))]
        logging.debug(f"Filtered the mesh sdp with sequence input \"Add\" for ip ==> \'{ip_node}\':\n{mesh_sdp_add_df.to_markdown()}\n")

        mesh_sdp_delete_df = dataframe.loc[((~dataframe["Mesh-sdp"].str.startswith("TempNA")) & (dataframe["Sequence"].str.upper().str.endswith("DELETE")))]
        logging.debug(f"Filtered the mesh sdp with sequence input \"Delete\" for ip_node ==> \'{ip_node}\':\n{mesh_sdp_delete_df.to_markdown()}\n")

        if len(mesh_sdp_add_df) > 0:
            # mesh_sdp_lines_start_lines = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
            #                                                              start_word="mesh-sdp ")

            # sdp_starting_start_lines = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
            #                                                            start_word="sdp ")

            if sdp_existence_status_dictionary is None:
                sdp_existence_status_dictionary = {}

            logging.debug(f"Creating the thread for mesh_sdp_add checks for ip_node \'{ip_node}\' ==>\n{mesh_sdp_add_df.to_markdown()}\n")
            mesh_sdp_add_result_dictionary_from_main_func = sdp_checks_add_dataframe_func(mesh_sdp_add_df,
                                                                                          ip_node)
            if len(result_dictionary) == 0:
                result_dictionary = mesh_sdp_add_result_dictionary_from_main_func
            else:
                result_dictionary.update(mesh_sdp_add_result_dictionary_from_main_func)

        if len(mesh_sdp_delete_df) > 0:
            # if mesh_sdp_lines_start_lines is None:
            #     mesh_sdp_lines_start_lines = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
            #                                                                  start_word="mesh-sdp ")
            #
            #     logging.debug(f"Created file lines filter with lines starting with 'mesh-sdp' for ip_node \'{ip_node}\' with len==>\n{len(mesh_sdp_lines_start_lines)}\n")
            #
            # if sdp_starting_start_lines is None:
            #     sdp_starting_start_lines = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
            #                                                                start_word="sdp ")
            #
            #     logging.debug(f"Created file lines filter with lines starting with 'sdp' for ip_node \'{ip_node}\' with len==>\n{len(sdp_starting_start_lines)}\n")

            if sdp_existence_status_dictionary is None:
                sdp_existence_status_dictionary = {}

            logging.debug(f"Creating the thread for mesh_sdp_delete checks for ip_node \'{ip_node}\' ==>\n{mesh_sdp_delete_df.to_markdown()}\n")
            mesh_sdp_delete_result_dictionary_from_main_func = sdp_checks_delete_dataframe_func(mesh_sdp_delete_df,
                                                                                                ip_node)
            if len(result_dictionary) == 0:
                result_dictionary = mesh_sdp_delete_result_dictionary_from_main_func

            else:
                result_dictionary.update(mesh_sdp_delete_result_dictionary_from_main_func)

        sap_lag_dataframe = dataframe.loc[((~dataframe["Sap/Lag"].str.strip().str.startswith("TempNA")) & (dataframe["Sap/Lag"].str.strip().str.startswith("sap lag")))]
        sap_lag_add_dataframe = sap_lag_dataframe.loc[sap_lag_dataframe["Sequence"].str.strip().str.lower().str.endswith("add")]
        logging.info(
            f"Got the sap_lag_add_dataframe for ip \'{ip_node}\'\n{sap_lag_add_dataframe.to_markdown()}"
        )
        sap_lag_delete_dataframe = sap_lag_dataframe.loc[sap_lag_dataframe["Sequence"].str.strip().str.lower().str.endswith("delete")]
        logging.info(
            f"Got the sap_lag_delete_dataframe for ip \'{ip_node}\'\n{sap_lag_delete_dataframe.to_markdown()}"
        )

        sap_without_lag_dataframe = dataframe.loc[
            (~dataframe["Sap/Lag"].str.strip().str.startswith("TempNA")) & (dataframe["Sap/Lag"].str.match(r"(\s*)sap([-,\d,\s,\w]+)/([\d,\s])/([\d,\s])([:,\d,\s]*)$"))]
        sap_without_lag_add_dataframe = sap_without_lag_dataframe.loc[(sap_without_lag_dataframe["Sequence"]).str.strip().str.lower().str.endswith("add")]
        logging.info(
            f"Got the sap_without_lag_add_dataframe for ip \'{ip_node}\'\n{sap_without_lag_add_dataframe.to_markdown()}"
        )
        sap_without_lag_delete_dataframe = sap_without_lag_dataframe.loc[sap_without_lag_dataframe["Sequence"].str.strip().str.lower().str.endswith("delete")]
        logging.info(
            f"Got the sap_without_lag_delete_dataframe for ip \'{ip_node}\'\n{sap_without_lag_delete_dataframe.to_markdown()}"
        )

        # if ser

        if (len(sap_lag_add_dataframe) > 0) and ((isinstance(sap_lag_starting_lines_from_service_lines_chunk, list)) and (len(sap_lag_starting_lines_from_service_lines_chunk) > 0)):
            logging.debug(f"Creating the file_lines_chunk for sap_lag for VPLS-1 for ip_node ==> {ip_node}")

            logging.debug(f"Created the sap_lag_starting_file_lines_chunk fo sap_lag for VPLS-1 for ip_node ==> {ip_node} with => {len(sap_lag_starting_lines_from_service_lines_chunk) = }\n")

            lag_add_action_dataframe_checks_result_dictionary_from_main_func = lag_add_action_dataframe_checks_func(sap_lag_add_dataframe,
                                                                                                                    ip_node)
            if len(result_dictionary) == 0:
                result_dictionary = lag_add_action_dataframe_checks_result_dictionary_from_main_func

            else:
                result_dictionary.update(lag_add_action_dataframe_checks_result_dictionary_from_main_func)

        if (len(sap_lag_delete_dataframe) > 0) and ((isinstance(sap_lag_starting_lines_from_service_lines_chunk, list)) and (len(sap_lag_starting_lines_from_service_lines_chunk) > 0)):

            lag_delete_action_dataframe_checks_result_dictionary_from_main_func = lag_delete_action_dataframe_checks_func(sap_lag_delete_dataframe,
                                                                                                                          ip_node)
            if len(result_dictionary) == 0:
                result_dictionary = lag_delete_action_dataframe_checks_result_dictionary_from_main_func

            else:
                result_dictionary.update(lag_delete_action_dataframe_checks_result_dictionary_from_main_func)

            logging.info(
                f'{ip_node}: - Updated the result dictionary with sap_without_lag_dataframe_delete_action_result_dictionary\n \'{'{\n'}\'' +
                f'{''.join([f'{key} : {value}' for key, value in lag_delete_action_dataframe_checks_result_dictionary_from_main_func.items()])}' +
                '}'
            )

        if (len(sap_without_lag_add_dataframe) > 0) and ((isinstance(sap_starting_lines_from_service_lines_chunk, list)) and (len(sap_starting_lines_from_service_lines_chunk) > 0)):
            logging.debug(f"Created the sap_starting_file_lines_chunk fo sap_lag for VPLS-1 for ip_node ==> {ip_node} with => {len(sap_starting_lines_from_service_lines_chunk) = }\n")
            sap_without_lag_dataframe_add_action_result_dictionary_from_main_func = sap_without_lag_add_dataframe_checks_func(sap_without_lag_add_dataframe,
                                                                                                                              ip_node)

            if len(result_dictionary) == 0:
                result_dictionary = sap_without_lag_dataframe_add_action_result_dictionary_from_main_func

            else:
                result_dictionary.update(sap_without_lag_dataframe_add_action_result_dictionary_from_main_func)

            logging.info(
                f'{ip_node}: - Updated the result dictionary with sap_without_lag_dataframe_add_action_result_dictionary_from_main_func\n \'{'{\n'}\'' +
                f'{''.join([f'{key} : {value}' for key, value in sap_without_lag_dataframe_add_action_result_dictionary_from_main_func.items()])}' +
                '}'
            )

        if (len(sap_without_lag_delete_dataframe) > 0) and ((isinstance(sap_starting_lines_from_service_lines_chunk, list)) and (len(sap_starting_lines_from_service_lines_chunk) > 0)):
            logging.debug(f"Creating the file_lines_chunk for sap_lag for VPLS-1 for ip_node ==> {ip_node}")

            # if sap_starting_lines_from_service_lines_chunk is None:
            #     sap_starting_lines_from_service_lines_chunk = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
            #                                                                                   start_word="sap ")

            logging.debug(f"Created the sap_starting_file_lines_chunk for sap for VPLS-1 for ip_node ==> {ip_node} with => {len(sap_lag_starting_lines_from_service_lines_chunk) = }\n")

            sap_without_lag_dataframe_delete_action_result_dictionary_from_main_func = sap_without_lag_delete_dataframe_checks_func(sap_without_lag_delete_dataframe,
                                                                                                                                    ip_node)

            if len(result_dictionary) == 0:
                result_dictionary = sap_without_lag_dataframe_delete_action_result_dictionary_from_main_func

            else:
                result_dictionary.update(sap_without_lag_dataframe_delete_action_result_dictionary_from_main_func)

            logging.info(
                f'{ip_node}: - Updated the result dictionary with sap_without_lag_dataframe_delete_action_result_dictionary\n \'{'{\n'}\'' +
                f'{''.join([f'{key} : {value}' for key, value in sap_without_lag_dataframe_delete_action_result_dictionary_from_main_func.items()])}' +
                '}'
            )

        # logging.info(f"result_dictionary for {ip_node} before add_action_thread termination :\n{result_dictionary}")
        # if ('add_action_thread' in locals()) or ('add_action_thread' in globals()):
        #     print(type(add_action_thread))
        #     if isinstance(add_action_thread, CustomThread):
        #         temp_var = add_action_thread.join()
        #         print(temp_var)
        #         if len(result_dictionary) == 0:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary = temp_var

        #         else:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary.update(temp_var)
        #         print(f"Inside the add action checks thread termination for ip {ip_node}{result_dictionary = }")

        # print(f"Before modify delete checks {ip_node = } {result_dictionary =}")

        # logging.info(f"result_dictionary for {ip_node} before modify_delete_thread termination :\n{result_dictionary}")
        # if ('modify_delete_thread' in locals()) or ('modify_delete_thread' in globals()):
        #     if isinstance(modify_delete_thread, CustomThread):
        #         temp_var = modify_delete_thread.join()
        #         print(temp_var)
        #         if len(result_dictionary) == 0:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary = temp_var

        #         else:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary.update(temp_var)

        # logging.info(f"result_dictionary for {ip_node} before mesh_sdp_add_thread termination :\n{result_dictionary}")
        # if ('mesh_sdp_add_thread' in locals()) or ('mesh_sdp_add_thread' in globals()):
        #     if isinstance(mesh_sdp_add_thread, CustomThread):
        #         temp_var = mesh_sdp_add_thread.join()
        #         print(temp_var)
        #         if len(result_dictionary) == 0:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary = temp_var

        #         else:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary.update(temp_var)

        # logging.info(f"result_dictionary for {ip_node} before mesh_sdp_delete_thread termination :\n{result_dictionary}")
        # if ('mesh_sdp_delete_thread' in locals()) or ('mesh_sdp_delete_thread' in globals()):
        #     if isinstance(mesh_sdp_delete_thread, CustomThread):
        #         temp_var = mesh_sdp_delete_thread.join()
        #         print(temp_var)
        #         if len(result_dictionary) == 0:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary = temp_var

        #         else:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary.update(temp_var)

        # logging.info(f"result_dictionary for {ip_node} before lag_add_action_dataframe_checks_thread termination :\n{result_dictionary}")
        # if ('lag_add_action_dataframe_checks_thread' in globals()) or ('lag_add_action_dataframe_checks_thread' in locals()):
        #     print(f"{type(lag_add_action_dataframe_checks_thread) = }")
        #     if isinstance(lag_add_action_dataframe_checks_thread, CustomThread):
        #         temp_var = lag_add_action_dataframe_checks_thread.join()
        #         print(ip_node, temp_var)
        #         if len(result_dictionary) == 0:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary = temp_var

        #         else:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary.update(temp_var)

        # logging.info(f"result_dictionary for {ip_node} before lag_delete_action_dataframe_checks_thread termination :\n{result_dictionary}")
        # if ('lag_delete_action_dataframe_checks_thread' in globals()) or ('lag_delete_action_dataframe_checks_thread' in locals()):
        #     if isinstance(lag_delete_action_dataframe_checks_thread, CustomThread):
        #         temp_var = lag_delete_action_dataframe_checks_thread.join()
        #         if len(result_dictionary) == 0:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary = temp_var

        #         else:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary.update(temp_var)

        # logging.info(f"result_dictionary for {ip_node} before sap_without_lag_dataframe_add_action_thread termination :\n{result_dictionary}")
        # if ('sap_without_lag_dataframe_add_action_thread' in globals()) or ('sap_without_lag_dataframe_add_action_thread' in locals()):
        #     if isinstance(sap_without_lag_dataframe_add_action_thread, CustomThread):
        #         temp_var = sap_without_lag_dataframe_add_action_thread.join()
        #         print(temp_var)
        #         if len(result_dictionary) == 0:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary = temp_var

        #         else:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary.update(temp_var)

        # logging.info(f"result_dictionary for {ip_node} before sap_without_lag_dataframe_delete_action_thread termination :\n{result_dictionary}")
        # if ('sap_without_lag_dataframe_delete_action_thread' in globals()) or ('sap_without_lag_dataframe_delete_action_thread' in locals()):
        #     if isinstance(sap_without_lag_dataframe_delete_action_thread, CustomThread):
        #         temp_var = sap_without_lag_dataframe_delete_action_thread.join()
        #         print(temp_var)
        #         if len(result_dictionary) == 0:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary = temp_var

        #         else:
        #             if isinstance(temp_var, dict):
        #                 result_dictionary.update(temp_var)

    except Exception as e:
        # exception_raised = True
        logging.error(f"{traceback.format_exc()}\nException Occurred!==>\n Title ==> {type(e)}\n Message ==> {str(e)}")
        title = str(type(e))
        message = str(e)
        messagebox.showerror(title=title,
                             message=message)
        result_dictionary = {}

    finally:
        # print(ip_node)
        # print(result_dictionary)
        if len(result_dictionary) > 0:
            logging.info(f"Got the result dictionary for node {ip_node} \n {result_dictionary}")
            for key, values in result_dictionary.items():
                result_dictionary[key] = sorted(list(set(values)))

            logging.debug(f"Returning the result dictionary from VPLS_1_nc for ip_node \'{ip_node}\' ===>\n {'\n'.join([f'{key} : {value}' for key, value in result_dictionary.items()])}\n")

        else:
            result_dictionary = {}
            logging.debug(
                "Returning an empty dictionary."
            )
        logging.shutdown()

        return result_dictionary
