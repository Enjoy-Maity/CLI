import os
import logging
import pandas as pd
import re
from file_lines_handler import File_lines_handler as flh
from Custom_Exception import CustomException
from CustomThread import CustomThread


def sap_without_lag_add_dataframe_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Performs the checks for sap without lag section on Sequence Add action dataframe

    Args:
        dataframe (pd.DataFrame): _description_ : dataframe containing the input details for which the checks are needed
        ip_node (str): _description_ : ip node for which the checks are being performed

    Returns:
        result_dictionary (dict): _description_ : returns the list of serial numbers with reason
    """
    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt="%d-%b-%Y %I:%M:%S %p",
                        encoding="UTF-8",
                        level=logging.DEBUG)

    logging.debug("Running the sap_without_lag_add_dataframe_checks_func for ip_node \'{ip_node}\'")

    global sap_starting_lines_from_service_lines_chunk
    global port_details_file_lines_list_block

    result_dictionary = {}

    reason = "Port-Detail not found or configured as access and wrong Sap entry found in template"
    reason2 = "Given Sap entry clash found"

    i = 0
    while (i < len(dataframe)):
        selected_port_details_input_from_dataframe = (dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")]).split()[1]
        selected_detail_input_from_dataframe = dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")]

        port_status = False
        port_status_index = 0
        port_mode_status = ""

        j = 0
        while (j < len(port_details_file_lines_list_block)):
            if (port_details_file_lines_list_block[j].startswith(f"port {selected_port_details_input_from_dataframe}")):
                port_status = True
                port_status_index = j

            if ((port_status) and (j > port_status_index)):
                if (port_details_file_lines_list_block[j].startswith("mode")):
                    port_mode_status = port_details_file_lines_list_block[j].split()[1].strip()

                if (port_details_file_lines_list_block[j].lower() == "exit"):
                    break
            j += 1

        if (not port_status):
            if (reason in result_dictionary):
                result_dictionary[reason] = []
                result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            else:
                result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            continue

        if ((port_status) and (port_mode_status == "access")):
            if (selected_detail_input_from_dataframe.__contains__(":")):
                if (len(selected_detail_input_from_dataframe.split(":")[1].strip()) == 0):
                    if (not reason in result_dictionary):
                        result_dictionary[reason] = []
                        result_dictionary[reason].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
                    else:
                        result_dictionary[reason].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
            else:
                if (not reason in result_dictionary):
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
                else:
                    result_dictionary[reason].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

            continue

        not_selected_port_details_input_from_dataframe_found_status = False
        k = 0
        while (k < len(sap_starting_lines_from_service_lines_chunk)):
            if (sap_starting_lines_from_service_lines_chunk[k].strip().startswith(selected_detail_input_from_dataframe)):
                not_selected_port_details_input_from_dataframe_found_status = True
                break
            k += 1

        if (not_selected_port_details_input_from_dataframe_found_status):
            if (not reason2 in result_dictionary):
                result_dictionary[reason2] = []
                result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            else:
                result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

        i += 1

    logging.debug(f"Returning result_dictionary from sap_without_lag_add_dataframe_checks_func for VPLS-1 for ip_node ==> {ip_node}")
    return result_dictionary


def sap_without_lag_delete_dataframe_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Performs the checks for sap without lag section on Sequence Delete action dataframe

    Args:
        dataframe (pd.DataFrame): _description_ : dataframe containing the input details for which the checks are needed
        ip_node (str): _description_ : ip node for which the checks are being performed

    Returns:
        result_dictionary (dict): _description_ : returns the list of serial numbers with reason
    """
    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt="%d-%b-%Y %I:%M:%S %p",
                        encoding="UTF-8",
                        level=logging.DEBUG)

    logging.debug("Running the sap_without_lag_delete_dataframe_checks_func for ip_node \'{ip_node}\'")
    result_dictionary = {}
    global sap_starting_lines_from_service_lines_chunk;
    global port_details_file_lines_list_block;

    reason = "Given Sap Entry Not Found"
    reason2 = "Port-Detail not found or configured as access and wrong Sap entry found"
    i = 0
    while (i < len(dataframe)):
        selected_port_details_from_dataframe_input = (dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")]).split()[1]
        selected_sap_details_from_dataframe_input = dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")].strip()
        selected_port_status = False
        selected_port_mode_status = ""
        selected_port_line_index = 0

        j = 0
        while (j < len(port_details_file_lines_list_block)):
            selected_port_status = False
            if (port_details_file_lines_list_block[j].startswith(f"port {selected_port_details_from_dataframe_input}")):
                selected_port_status = True
                selected_port_line_index = j

            if selected_port_status and (j > selected_port_lines_index):
                if port_details_file_lines_list_block[j].startswith("mode"):
                    selected_port_mode_status = (port_details_file_lines_list_block[j]).split()[1].strip()

                if (port_details_file_lines_list_block[j].lower() == ("exit")):
                    break

            j += 1

        if (not selected_port_status):
            if (not reason2 in result_dictionary):
                result_dictionary[reason2] = []
                result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

            else:
                result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

            continue

        if ((selected_port_status) and (selected_port_mode_status.lower() == "access")):
            if (selected_sap_details_from_dataframe_input.__contains__(":")):
                if (len(selected_sap_details_from_dataframe_input.split(":")[1].strip()) == 0):
                    if (not reason2 in result_dictionary):
                        result_dictionary[reason2] = []
                        result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
                    else:
                        result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
                    continue
            else:
                if (not reason2 in result_dictionary):
                    result_dictionary[reason2] = []
                    result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

                else:
                    result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

            continue

        selected_sap_details_from_dataframe_input_found = False

        k = 0
        while (k < len(sap_starting_lines_from_service_lines_chunk)):
            if (sap_starting_lines_from_service_lines_chunk[k].strip().startswith(selected_sap_details_from_dataframe_input)):
                selected_sap_details_from_dataframe_input_found = True
                break
            k += 1

        if (not selected_sap_details_from_dataframe_input_found):
            if (not reason2 in result_dictionary):
                result_dictionary[reason2] = []
                result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

            else:
                result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])
        i += 1

    return result_dictionary


def lag_add_action_dataframe_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Performs the checks for lag section on Sequence Add action dataframe

    Args:
        dataframe (pd.DataFrame): _description_ : dataframe containing the input details for which the checks are needed
        ip_node (str): _description_ : ip node for which the checks are being performed

    Returns:
        result_dictionary (dict): _description_ : returns the list of serial numbers with reason
    """
    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt="%d-%b-%Y %I:%M:%S %p",
                        encoding="UTF-8",
                        level=logging.DEBUG)

    logging.debug("Running the lag_add_action_dataframe_checks_func for ip_node \'{ip_node}\'")
    result_dictionary = {}
    global lag_details_file_lines_list_block;
    global sap_lag_starting_lines_from_service_lines_chunk;

    compiled_pattern = re.compile(pattern=r"\d+")

    reason = "Lag not found or configured as access and wrong Sap entry found in input template"
    reason2 = "Given Sap entry clash found"

    i = 0
    while (i < len(dataframe)):
        selected_sap_lag_variable = dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")]
        lag_in_selected_variable = re.findall(pattern=compiled_pattern,
                                              string=selected_sap_lag_variable)
        lag_status = False
        lag_mode_status = ""

        lag_status_index = 0
        j = 0
        while (j < len(lag_details_file_lines_list_block)):
            if (lag_details_file_lines_list_block[j].strip().startswith(f"lag {lag_in_selected_variable}")):
                lag_status = True
                lag_status_index = j

            if ((lag_status) and (j > lag_status_index)):
                if (lag_details_file_lines_list_block[j].startswith(f"mode")):
                    lag_mode_status = lag_details_file_lines_list_block[j].split()[1].strip()

                if (lag_details_file_lines_list_block[j].lower() == 'exit'):
                    break

            j += 1

        if (not lag_status):
            if (not reason in result_dictionary):
                result_dictionary[reason] = []
                result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            else:
                result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            continue

        if ((lag_status) and (lag_mode_status == "access")):
            if (selected_sap_lag_variable.__contains__(":")):
                if (len(selected_sap_lag_variable.split(":")[1].strip()) == 0):
                    if (not reason in result_dictionary):
                        result_dictionary[reason] = []
                        result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                    else:
                        result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                    continue
            else:
                if (not reason in result_dictionary):
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                else:
                    result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                continue

        selected_sap_lag_variable_founding_status = False

        k = 0
        while (k < len(sap_lag_starting_lines_from_service_lines_chunk)):
            if (sap_lag_starting_lines_from_service_lines_chunk[k].startswith(selected_sap_lag_variable)):
                selected_sap_lag_variable_founding_status = True
                break
            k += 1

        if (not selected_sap_lag_variable_founding_status):
            if (not reason2 in result_dictionary):
                result_dictionary[reason2] = []
                result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            else:
                result_dictionary[reason2].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

        i += 1

    logging.debug(f"Returning result_dictionary from lag_add_action_dataframe_checks_func for VPLS-1 for ip_node ==> {ip_node}")
    return result_dictionary


def lag_delete_action_dataframe_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Performs the checks for lag section on Sequence Add action dataframe

    Args:
        dataframe (pd.DataFrame): _description_ : dataframe containing the input details for which the checks are needed
        ip_node (str): _description_ : ip node for which the checks are being performed

    Returns:
        result_dictionary (dict): _description_ : returns the list of serial numbers with reason
    """
    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt="%d-%b-%Y %I:%M:%S %p",
                        encoding="UTF-8",
                        level=logging.DEBUG)

    logging.debug("Running the lag_delete_action_dataframe_checks_func for ip_node \'{ip_node}\'")
    result_dictionary = {}
    global lag_details_file_lines_list_block;
    global sap_lag_starting_lines_from_service_lines_chunk;

    reason = "Given Sap Entry Not Found"
    reason2 = "LAG Entry Not Found"

    i = 0
    while (i < len(dataframe)):
        selected_sap_lag_variable = dataframe.iloc[i, dataframe.columns.get_loc("Sap/Lag")]
        lag_in_selected_variable = re.findall(pattern=compiled_pattern,
                                              string=selected_sap_lag_variable)
        lag_status = False
        lag_mode_status = ""

        lag_status_index = 0
        j = 0
        while (j < len(lag_details_file_lines_list_block)):
            if (lag_details_file_lines_list_block[j].strip().startswith(f"lag {lag_in_selected_variable}")):
                lag_status = True
                lag_status_index = j

            if ((lag_status) and (j > lag_status_index)):
                if (lag_details_file_lines_list_block[j].startswith(f"mode")):
                    lag_mode_status = lag_details_file_lines_list_block[j].strip().split("")[1]

                if (lag_details_file_lines_list_block[j].lower() == 'exit'):
                    break

            j += 1

        if (not lag_status):
            if (not reason2 in result_dictionary):
                result_dictionary[reason2] = []
                result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

            else:
                result_dictionary[reason2].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

            continue

        if ((lag_status) and (lag_mode_status == "access")):
            if (selected_sap_lag_variable.__contains__(":")):
                if (len(selected_sap_lag_variable.split(":")[1].strip()) == 0):
                    if (not reason in result_dictionary):
                        result_dictionary[reason] = []
                        result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                    else:
                        result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                    continue
            else:
                if (not reason in result_dictionary):
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                else:
                    result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                continue

        selected_sap_lag_variable_founding_status = False

        k = 0
        while (k < len(sap_lag_starting_lines_from_service_lines_chunk)):
            if (sap_lag_starting_lines_from_service_lines_chunk[k].startswith(selected_sap_lag_variable)):
                selected_sap_lag_variable_founding_status = True
                break
            k += 1

        if (not selected_sap_lag_variable_founding_status):
            if (not reason in result_dictionary):
                result_dictionary[reason] = []
                result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            else:
                result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

        i += 1

    logging.debug(f"Returning result_dictionary from lag_add_action_dataframe_checks_func for VPLS-1 for ip_node ==> {ip_node}")
    return result_dictionary


def sdp_checks_add_dataframe_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Checks for the sdp checks for the add sequence action

    Args:
        dataframe (pd.DataFrame): _description_ : dataframe containing the input details for which the checks are needed.
        ip_node (str): _description_ : ip node for which the checks are being performed
        
    return result_dictionary
        result_dictionary (dict) : _description_ : returns the list of serial numbers with reason
    """
    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt="%d-%b-%Y %I:%M:%S %p",
                        encoding="UTF-8",
                        level=logging.DEBUG)

    logging.debug("Running the sdp_checks_add_dataframe_func for ip_node \'{ip_node}\'")
    result_dictionary = {}
    global sdp_starting_start_lines;
    global mesh_sdp_lines_start_lines;

    reason = "Given 'S:Add' Mesh-SDP clash found"
    reason2 = ""

    compiled_digits_pattern = re.compile(pattern=r"\d+")
    i = 0
    while (i < len(dataframe)):
        mesh_sdp_digit_variable = (re.findall(pattern=compiled_digits_pattern,
                                              string=dataframe.iloc[i, dataframe.columns.get_loc("Mesh-sdp")]))[0]

        mesh_input_from_dataframe = (dataframe.iloc[i, dataframe.columns.get_loc("Mesh-sdp")]).lower()
        mesh_sdp_input_status = False

        j = 0
        while (j < len(sdp_starting_start_lines)):
            if (sdp_starting_start_lines[j].strip().startswith(f"sdp {mesh_sdp_digit_variable}")):
                sdp_existence_status_dictionary[f"sdp {mesh_sdp_digit_variable}"] = "Found"
                break
            j += 1

        if ((not f"sdp {mesh_sdp_digit_variable}" in sdp_existence_status_dictionary)):
            sdp_existence_status_dictionary[f"sdp {mesh_sdp_digit_variable}"] = "Not Found"

        k = 0
        while (k < len(mesh_sdp_lines_start_lines)):
            if (mesh_sdp_lines_start_lines[k].strip().startswith(mesh_input_from_dataframe)):
                mesh_sdp_input_status = True
                break
            k += 1

        if (mesh_sdp_input_status):
            if (reason in result_dictionary):
                result_dictionary[reason] = []
                result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            else:
                result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

        i += 1

    logging.debug(f"Returning the result_dictionary from sdp_checks_add_dataframe_func for ip_node \'{ip_node}\':\n\'{'\n'.join([f'{key}:{value}' for key, value in result_dictionary.items()])}")
    return result_dictionary


def sdp_checks_delete_dataframe_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Checks for the sdp checks for the add sequence action

    Args:
        dataframe (pd.DataFrame): _description_ : dataframe containing the input details for which the checks are needed.
        ip_node (str): _description_ : ip node for which the checks are being performed
        
    return result_dictionary
        result_dictionary (dict) : _description_ : returns the list of serial numbers with reason
    """
    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt="%d-%b-%Y %I:%M:%S %p",
                        encoding="UTF-8",
                        level=logging.DEBUG)

    logging.debug("Running the sdp_checks_delete_dataframe_func for ip_node \'{ip_node}\'")
    result_dictionary = {}
    global sdp_starting_start_lines;
    global mesh_sdp_lines_start_lines;

    reason = "Given 'S:Delete' Mesh-SDP not found"

    compiled_digits_pattern = re.compile(pattern="\d+")
    i = 0
    while (i < len(dataframe)):
        mesh_sdp_digit_variable = (re.findall(pattern=compiled_digits_pattern,
                                              string=dataframe.iloc[i, dataframe.columns.get_loc("Mesh-sdp")]))[0]

        mesh_input_from_dataframe = (dataframe.iloc[i, dataframe.columns.get_loc("Mesh-sdp")]).lower()
        mesh_sdp_input_status = False

        j = 0
        while (j < len(sdp_starting_start_lines)):
            if (sdp_starting_start_lines[j].strip().startswith(f"sdp {mesh_sdp_digit_variable}")):
                sdp_existence_status_dictionary[f"sdp {mesh_sdp_digit_variable}"] = "Found"
                break
            j += 1

        if ((not f"sdp {mesh_sdp_digit_variable}" in sdp_existence_status_dictionary)):
            reason = "Given 'S:Delete' sdp not found"
            sdp_existence_status_dictionary[f"sdp {mesh_sdp_digit_variable}"] = "Not Found"

            if (not reason in result_dictionary):
                result_dictionary[reason] = []
                result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            else:
                result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            continue

        k = 0
        while (k < len(mesh_sdp_lines_start_lines)):
            if (mesh_sdp_lines_start_lines[k].strip().startswith(mesh_input_from_dataframe)):
                mesh_sdp_input_status = True
                break
            k += 1

        if (not mesh_sdp_input_status):
            if (reason in result_dictionary):
                result_dictionary[reason] = []
                result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

            else:
                result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

        i += 1
    logging.debug(f"Returning the result_dictionary from sdp_checks_delete_dataframe_func for ip_node \'{ip_node}\':\n\'{'\n'.join([f'{key}:{value}' for key, value in result_dictionary.items()])}")
    return result_dictionary


def add_action_checks(dataframe: pd.DataFrame, running_config_backup_file_lines: list, ip_node: str, vpls_id_starter_lines_filter: list) -> dict:
    """
        Performs the Checks for the presence of VPLS ID in the running config backup files
        
        Arguments : (dataframe, running_config_backup_file_lines,ip_node,vpls_id_starter_lines_filter)
            dataframe ===> pandas.DataFrame
                description =====> filtered dataframe with Action "A:Add" from the node ip Section dataframe
            
            running_config_backup_file_lines ===> list
                description =====> List of lines from running config backup lines
                
            ip_node ===> str
                description =====> Node IP for which the checks are being done
                
            vpls_id_starter_lines_filter ===> list
                description =====> list of lines starting with vpls keyword
        
        return result_dictionary
            result_dictionary ===> dict
                description =====> dictionary containing the error results in the form of a dictionary
                                    dictionary structure => {
                                                                error_reason : [list of S.No. with the errors]
                                                            }
                                                            or 
                                                            empty dictionary -> {}
    """
    global log_file;
    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt="%d-%b-%Y %I:%M:%S %p",
                        encoding="UTF-8",
                        level=logging.DEBUG)
    logging.debug(f"inside {__name__} for ip_node ==> {ip_node}")

    logging.debug(f"got the dataframe for ip_node => {dataframe.to_markdown()}")
    result_dictionary = {}

    reason = "Action:Add VPLS ID Clash found"
    i = 0
    while (i < len(dataframe)):
        vpls_id_to_be_searched = int(dataframe.iloc[i, dataframe.columns.get_loc("VPLS ID")])
        j = 0
        while (j < len(vpls_id_starter_lines_filter)):
            if (vpls_id_starter_lines_filter[j].startswith(f"vpls {vpls_id_to_be_searched} ")):
                if (not reason in result_dictionary):
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(int(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")]))

                else:
                    result_dictionary[reason].append(dataframe)
                break
            j += 1
        i += 1

    reason = "Action:Add VPLS Name Clash found"
    service_name_lines_filter_list = flh().file_lines_starter_filter(file_lines_list=running_config_backup_file_lines,
                                                                     start_word="service-name ")

    i = 0
    while (i < len(dataframe)):
        vpls_name_to_be_searched = str(dataframe.iloc[i, dataframe.columns.get_loc("VPLS Name")])
        j = 0
        while (j < len(service_name_lines_filter_list)):
            if (vpls_id_starter_lines_filter[j].startswith(f"service-name \"{vpls_name_to_be_searched}\"")):
                if (not reason in result_dictionary):
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

                else:
                    result_dictionary[reason].append(dataframe)
                break
            j += 1
        i += 1

    logging.debug(f"Returning the result_dictionary from add_action_checks for ip_node \'{ip_node}\' :\n\'{'\n'.join([f'{key}:{value}' for key, value in result_dictionary.items()])}")
    return result_dictionary


def modify_delete_action_checks(dataframe: pd.DataFrame, running_config_backup_file_lines: list, ip_node: str, vpls_id_starter_lines_filter: list):
    """
        Performs the checks for the presence of SDP variable in the running config backup files
        
        Arguments : (dataframe, running_config_backup_file_lines,ip_node,vpls_id_starter_lines_filter)
        dataframe ===> pandas.DataFrame
                description =====> filtered dataframe with Action "A:Modify/Delete" from the node ip Section dataframe
            
            running_config_backup_file_lines ===> list
                description =====> List of lines from running config backup lines
                
            ip_node ===> str
                description =====> Node IP for which the checks are being done
            
            vpls_id_starter_lines_filter ===> list
                description =====> list of lines starting with vpls keyword
        
        return result_dictionary
            result_dictionary ===> dict
                description =====> dictionary containing the error results in the form of a dictionary
                                    dictionary structure => {
                                                                error_reason : [list of S.No. with the errors]
                                                            }
                                                            or 
                                                            empty dictionary -> {}
    """
    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt="%d-%b-%Y %I:%M:%S %p",
                        encoding="UTF-8",
                        level=logging.DEBUG)

    logging.debug(f"Running modify_delete_action_checks for ip_node {ip_node}")

    result_dictionary = {}

    reason = "Action:Modify/Delete VPLS ID not found"
    i = 0
    while (i < len(dataframe)):
        vpls_id_to_be_searched = int(dataframe.iloc[i, dataframe.columns.get_loc("VPLS ID")])
        j = 0
        flag = False
        while (j < len(vpls_id_starter_lines_filter)):
            if (vpls_id_starter_lines_filter[j].startswith(f"vpls {vpls_id_to_be_searched} ")):
                flag = True
                break
            j += 1

        if (not flag):
            if (not reason in result_dictionary):
                result_dictionary[reason] = []
                result_dictionary[reason].append(dataframe.iloc[i, dataframe.columns.get_loc("S.No.")])

            else:
                result_dictionary[reason].append(dataframe)
        i += 1

    logging.debug(f"Returning the result_dictionary from modify_delete_action_checks :\n\'{'\n'.join([f'{key}:{value}' for key, value in result_dictionary.items()])}")
    return result_dictionary


def main_func(dataframe: pd.DataFrame, ip_node: str, running_config_backup_file_lines: list):
    """
        Performs the Node Checks for VPLS 1 
        
        Arguments : (dataframe, ip_node, running_config_backup_file_lines)
            dataframe ===> pandas.DataFrame
                description ======> contains the dataframe(tabular data) for the VPLS-1 Section of given ip_node for running_config checks
                
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
    # username = (os.popen('cmd.exe /C "echo %username%"').read()).strip()

    global log_file;
    log_file = rf"C:/Ericsson_Application_Logs/CLI_Automation_Logs/Running_Config_Checks(Node_Checks).log"

    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt="%d-%b-%Y %I:%M:%S %p",
                        encoding="UTF-8",
                        level=logging.DEBUG)

    # dataframe = dataframe.fillna("TempNA")
    result_dictionary = {}
    try:
        dataframe = dataframe.where(~dataframe.isna(), "TempNA")

        # global flag;

        add_action_dataframe = dataframe[dataframe['Action'].str.upper().str.contains("ADD")]
        add_action_dataframe_checks = {}

        vpls_id_starter_lines_filter = flh().file_lines_starter_filter(file_lines_list=running_config_backup_file_lines,
                                                                       start_word="vpls")

        global services_file_lines_list_block;
        service_file_lines_list_block = flh().file_lines_chunk_divisor(file_lines_list=running_config_backup_file_lines,
                                                                       start_string='echo "Service Configuration"',
                                                                       end_string_pattern=r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration"$')

        global port_details_file_lines_list_block;
        port_details_file_lines_list_block = flh().file_lines_chunk_divisor(file_lines_list=running_config_backup_file_lines,
                                                                            start_string='echo "Port Configuration"',
                                                                            end_string_pattern=r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration"$')
        global lag_details_file_lines_list_block;
        lag_details_file_lines_list_block = flh().file_lines_chunk_divisor(file_lines_list=running_config_backup_file_lines,
                                                                           start_string='echo "LAG Configuration"',
                                                                           end_string_pattern=r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration"$')

        add_action_thread = ""
        if (len(add_action_dataframe) > 0):
            logging.debug(f"Creating the thread for checking the presence of VPLS ID for {ip_node} for the dataframe\n{add_action_dataframe.to_markdown()}\n")
            add_action_thread = CustomThread(target=add_action_checks,
                                             args=(add_action_dataframe, running_config_backup_file_lines, ip_node, vpls_id_starter_lines_filter))
            add_action_thread.daemon = True
            add_action_thread.start()

        modify_delete_thread = ""
        modify_delete_action_dataframe = dataframe[dataframe['Action'].str.upper().str.contains("MODIFY|DELETE")]
        logging.debug("")

        if (len(modify_delete_action_dataframe) > 0):
            logging.debug(f"Creating the thread for checking the sdp variable for {ip_node} for the dataframe\n{modify_delete_action_dataframe.to_markdown()}\n")
            modify_delete_thread = CustomThread(target=modify_delete_action_checks,
                                                args=(modify_delete_action_dataframe, running_config_backup_file_lines, ip_node, vpls_id_starter_lines_filter))
            modify_delete_thread.daemon = True
            modify_delete_thread.start()

        mesh_sdp_add_df = dataframe.loc[((~dataframe["Mesh-sdp"].str.startswith("TempNA")) & (dataframe["Sequence"].str.upper().str.endswith("ADD")))]
        logging.debug(f"Filtered the mesh sdp with sequence input \"Add\" for ip ==> \'{ip_node}\':\n{mesh_sdp_add_df.to_markdown()}\n")

        mesh_sdp_delete_df = dataframe.loc[((~dataframe["Mesh-sdp"].str.startswith("TempNA")) & (dataframe["Sequence"].str.upper().str.endswith("DELETE")))]
        logging.debug(f"Filtered the mesh sdp with sequence input \"Delete\" for ip_node ==> \'{ip_node}\':\n{mesh_sdp_delete_df.to_markdown()}\n")

        if (len(mesh_sdp_add_df) > 0):
            global mesh_sdp_lines_start_lines;
            mesh_sdp_lines_start_lines = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
                                                                         start_word="mesh-sdp ")
            global sdp_starting_start_lines;
            sdp_starting_start_lines = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
                                                                       start_word="sdp ")

            logging.debug(f"Created file lines filter with lines starting with 'mesh-sdp' for ip_node \'{ip_node}\' with len==>\n{len(mesh_sdp_lines_start_lines)}\n")

            global sdp_existence_status_dictionary;
            sdp_existence_status_dictionary = {}

            logging.debug(f"Creating the thread for mesh_sdp_add checks for ip_node \'{ip_node}\' ==>\n{mesh_sdp_add_df.to_markdown()}\n")
            mesh_sdp_add_thread = CustomThread(target=sdp_checks_add_dataframe_func,
                                               args=(mesh_sdp_add_df, ip_node))
            mesh_sdp_add_thread.daemon = True
            mesh_sdp_add_thread.start()

        if (len(mesh_sdp_delete_df) > 0):
            if ((not mesh_sdp_lines_start_lines in globals()) or (not mesh_sdp_lines_start_lines in locals())):
                global mesh_sdp_lines_start_lines;
                mesh_sdp_lines_start_lines = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
                                                                             start_word="mesh-sdp ")

                global sdp_starting_start_lines;
                sdp_starting_start_lines = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
                                                                           start_word="sdp ")

                logging.debug(f"Created file lines filter with lines starting with 'mesh-sdp' for ip_node \'{ip_node}\' with len==>\n{len(mesh_sdp_lines_start_lines)}\n")
                logging.debug(f"Created file lines filter with lines starting with 'sdp' for ip_node \'{ip_node}\' with len==>\n{len(sdp_starting_start_lines)}\n")

            if (not ((sdp_existence_status_dictionary in globals()) or (sdp_existence_status_dictionary in locals()))):
                global sdp_existence_status_dictionary;
                sdp_existence_status_dictionary = {}

            logging.debug(f"Creating the thread for mesh_sdp_delete checks for ip_node \'{ip_node}\' ==>\n{mesh_sdp_delete_df.to_markdown()}\n")
            mesh_sdp_delete_thread = CustomThread(target=sdp_checks_delete_dataframe_func,
                                                  args=(mesh_sdp_delete_df, ip_node))
            mesh_sdp_delete_thread.daemon = True
            mesh_sdp_delete_thread.start()

        sap_lag_dataframe = dataframe.loc[((~dataframe["Sap/Lag"].str.strip().str.startswith("TempNA")) & (dataframe["Sap/Lag"].str.strip().str.startswith("sap lag")))]
        sap_lag_add_dataframe = sap_lag_dataframe.loc[sap_lag_dataframe["Sequence"].str.strip().str.lower().str.endswith("add")]
        sap_lag_delete_dataframe = sap_lag_dataframe.loc[sap_lag_dataframe["Sequence"].str.strip().str.lower().str.endswith("delete")]

        sap_without_lag_dataframe = dataframe.loc[((~dataframe["Sap/Lag"].str.strip().str.startswith("TempNA")) & (dataframe["Sap/Lag"].str.strip().str.contains("/")))]
        sap_without_lag_add_dataframe = sap_without_lag_dataframe.loc[(sap_without_lag_dataframe["Sequence"]).str.strip().str.endswith("add")]
        sap_without_lag_delete_dataframe = sap_without_lag_dataframe.loc[sap_without_lag_dataframe["Sequence"].str.strip().str.endswith("delete")]

        if (len(sap_lag_add_dataframe) > 0):
            logging.debug(f"Creating the file_lines_chunk for sap_lag for VPLS-1 for ip_node ==> {ip_node}")

            global sap_lag_starting_lines_from_service_lines_chunk;
            sap_lag_starting_lines_from_service_lines_chunk = flh().file_lines_starter_filter(file_lines_list=services_file_lines_list_block,
                                                                                              start_word="sap lag-")
            logging.debug(f"Created the sap_lag_starting_file_lines_chunk fo sap_lag for VPLS-1 for ip_node ==> {ip_node} with => {len(sap_lag_starting_lines_from_service_lines_chunk) = }\n")

            lag_add_action_dataframe_checks_thread = CustomThread(target=lag_add_action_dataframe_checks_func,
                                                                  args=(sap_lag_add_dataframe, ip_node))
            lag_add_action_dataframe_checks_thread.daemon = True
            lag_add_action_dataframe_checks_thread.start()

        if (len(sap_lag_delete_dataframe) > 0):
            if (not (sap_lag_starting_lines_from_service_lines_chunk in globals()) or (sap_lag_starting_lines_from_service_lines_chunk in locals())):
                logging.debug(f"Creating the file_lines_chunk for sap_lag for VPLS-1 for ip_node ==> {ip_node}")

                global sap_lag_starting_lines_from_service_lines_chunk;
                sap_lag_starting_lines_from_service_lines_chunk = flh().file_lines_starter_filter(file_lines_list=services_file_lines_list_block,
                                                                                                  start_word="sap lag-")
                logging.debug(f"Created the sap_lag_starting_file_lines_chunk for sap_lag for VPLS-1 for ip_node ==> {ip_node} with => {len(sap_lag_starting_lines_from_service_lines_chunk) = }\n")

            lag_delete_action_dataframe_checks_thread = CustomThread(target=lag_delete_action_dataframe_checks_func,
                                                                     args=(sap_lag_delete_dataframe, ip_node))
            lag_delete_action_dataframe_checks_thread.daemon = True
            lag_delete_action_dataframe_checks_thread.start()

        if (len(sap_without_lag_add_dataframe) > 0):
            global sap_starting_lines_from_service_lines_chunk;
            sap_starting_lines_from_service_lines_chunk = flh().file_lines_starter_filter(file_lines_list=services_file_lines_list_block,
                                                                                          start_word="sap ")

            logging.debug(f"Created the sap_starting_file_lines_chunk fo sap_lag for VPLS-1 for ip_node ==> {ip_node} with => {len(sap_starting_lines_from_service_lines_chunk) = }\n")
            sap_without_lag_dataframe_add_action_thread = CustomThread(target=sap_without_lag_add_dataframe_checks_func,
                                                                       args=(sap_without_lag_add_dataframe, ip_node))

            sap_without_lag_dataframe_add_action_thread.daemon = True
            sap_without_lag_dataframe_add_action_thread.start()

        if (len(sap_without_lag_delete_dataframe) > 0):
            if (not ((sap_starting_lines_from_service_lines_chunk in globals()) and (sap_starting_lines_from_service_lines_chunk in locals()))):
                logging.debug(f"Creating the file_lines_chunk for sap_lag for VPLS-1 for ip_node ==> {ip_node}")

                global sap_starting_lines_from_service_lines_chunk;
                sap_starting_lines_from_service_lines_chunk = flh().file_lines_starter_filter(file_lines_list=services_file_lines_list_block,
                                                                                              start_word="sap ")

                logging.debug(f"Created the sap_starting_file_lines_chunk for sap for VPLS-1 for ip_node ==> {ip_node} with => {len(sap_lag_starting_lines_from_service_lines_chunk) = }\n")

            logging.debug(f"Created the sap_starting_file_lines_chunk fo sap_lag for VPLS-1 for ip_node ==> {ip_node} with => {len(sap_starting_lines_from_service_lines_chunk) = }\n")
            sap_without_lag_dataframe_delete_action_thread = CustomThread(target=sap_without_lag_delete_dataframe_checks_func,
                                                                          args=(sap_without_lag_delete_dataframe, ip_node))

            sap_without_lag_dataframe_delete_action_thread.daemon = True
            sap_without_lag_dataframe_delete_action_thread.start()

        if ((add_action_thread in locals()) or (add_action_thread in globals())):
            if (isinstance(add_action_thread, CustomThread)):
                if (len(result_dictionary) == 0):
                    result_dictionary = add_action_thread.join()

                else:
                    result_dictionary.update(add_action_thread.join())

        if ((modify_delete_thread in locals()) or (modify_delete_thread in globals())):
            if (isinstance(modify_delete_thread, CustomThread)):
                if (len(result_dictionary) == 0):
                    result_dictionary = modify_delete_thread.join()

                else:
                    result_dictionary.update(modify_delete_thread.join())

        if ((mesh_sdp_add_thread in locals()) or (mesh_sdp_add_thread in globals())):
            if (isinstance(mesh_sdp_add_thread, CustomThread)):
                if (len(result_dictionary) == 0):
                    result_dictionary = mesh_sdp_add_thread.join()

                else:
                    result_dictionary.update(mesh_sdp_add_thread.join())

        if ((mesh_sdp_delete_thread in locals()) or (mesh_sdp_delete_thread in globals())):
            if (isinstance(mesh_sdp_delete_thread, CustomThread)):
                if (len(result_dictionary) == 0):
                    result_dictionary = mesh_sdp_delete_thread.join()

                else:
                    result_dictionary.update(mesh_sdp_delete_thread.join())

        if ((lag_add_action_dataframe_checks_thread in globals()) or (lag_add_action_dataframe_checks_thread in locals())):
            if (isinstance(lag_add_action_dataframe_checks_thread, CustomThread)):
                if (len(result_dictionary) == 0):
                    result_dictionary = lag_add_action_dataframe_checks_thread.join()

                else:
                    result_dictionary.update(lag_add_action_dataframe_checks_thread.join())

        if ((lag_delete_action_dataframe_checks_thread in globals()) or (lag_delete_action_dataframe_checks_thread in locals())):
            if (isinstance(lag_delete_action_dataframe_checks_thread, CustomThread)):
                if (len(result_dictionary) == 0):
                    result_dictionary = lag_delete_action_dataframe_checks_thread.join()

                else:
                    result_dictionary = lag_delete_action_dataframe_checks_thread.join()

        if ((sap_without_lag_dataframe_add_action_thread in globals()) or (sap_without_lag_dataframe_add_action_thread in locals())):
            if (isinstance(sap_without_lag_dataframe_add_action_thread, CustomThread)):
                if (len(result_dictionary) == 0):
                    result_dictionary = sap_without_lag_dataframe_add_action_thread.join()

                else:
                    result_dictionary.update(sap_without_lag_dataframe_add_action_thread.join())

        if ((sap_without_lag_dataframe_delete_action_thread in globals()) or (sap_without_lag_dataframe_delete_action_thread in locals())):
            if (isinstance(sap_without_lag_dataframe_delete_action_thread, CustomThread)):
                if (len(result_dectionary) == 0):
                    result_dictionary = sap_without_lag_dataframe_delete_action_thread.join()

                else:
                    result_dictionary.update(sap_without_lag_dataframe_delete_action_thread.join())

    except Exception:
        pass

    finally:
        for key, values in result_dictionary.items():
            result_dictionary[key] = sorted(list(set(values)))

        logging.debug(f"Returning the result dictionary from VPLS_1_nc for ip_node \'{ip_node}\' ===>\n {'\n'.join([f'{key} : {value}' for key, value in result_dictionary.items()])}\n")

        logging.shutdown()

        return result_dictionary
