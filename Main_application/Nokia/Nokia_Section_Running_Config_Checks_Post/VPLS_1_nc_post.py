import re
import logging
import traceback
import pandas as pd
from Main_application.CustomThread import CustomThread
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


def add_action_checks(dataframe: pd.DataFrame, running_config_backup_file_lines: list, ip_node: str, vpls_id_starter_lines_filter: list) -> dict:
    """
    Performs the Checks for the presence of VPLS ID in the post running config backup files
    :param dataframe: filtered dataframe with Action "A:Add" from the node ip Section dataframe
    :param running_config_backup_file_lines: List of lines from running config backup lines
    :param ip_node: Node IP for which the checks are being done
    :param vpls_id_starter_lines_filter: list of lines starting with vpls keyword
    :return result_dictionary (dict): dictionary containing the error results
                                      dictionary structure => {
                                                                error_reason: [list of S.No. with the errors]
                                                            }
                                                            or
                                                            empty dictionary -> {}
    """
    logging.debug(f"inside {__name__} for ip_node ==> {ip_node}")
    logging.debug(f"got the dataframe for ip_node {ip_node} =>\n{dataframe.to_markdown()}")
    add_action_checks_result_dictionary = {}

    return add_action_checks_result_dictionary


def modify_delete_action_checks(dataframe: pd.DataFrame, running_config_backup_file_lines: list, ip_node: str, vpls_id_starter_lines_filter: list) -> dict:
    """
    Performs the checks for the presence of VPLS ID in the post running config backup file
    :param dataframe: filtered dataframe with Action "A:Modify/Delete" from the node ip Section dataframe
    :param running_config_backup_file_lines: List of lines from running config backup lines
    :param ip_node: Node IP for which the checks are being done
    :param vpls_id_starter_lines_filter: list of lines starting with vpls keyword
    :return result_dictionary(dict): dictionary containing the error results
                                     dictionary structure => {
                                                                error_reason: [list of S.No. with the errors]
                                                            }
                                                            or
                                                            empty dictionary -> {}
    """
    logging.debug(f"Running modify_delete_action_checks for ip_node {ip_node}")

    modify_delete_action_checks_result_dictionary = {}

    logging.info(f"{ip_node}: -vpls_id_starter_lines_filter =>\n{'\n'.join(vpls_id_starter_lines_filter)}")

    return modify_delete_action_checks_result_dictionary


def sdp_checks_delete_dataframe_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """
    Checks for the sdp checks for the delete sequence action
    :param dataframe: dataframe containing the input details for which the checks are needed.
    :param ip_node: ip node for which the checks are being performed
    :return sdp_checks_delete_dataframe_result_dictionary(dict):
    """
    logging.debug("Running the sdp_checks_add_dataframe_func for ip_node \'{ip_node}\'")
    sdp_checks_delete_dataframe_result_dictionary = {}
    global sdp_starting_start_lines
    global mesh_sdp_lines_start_lines
    compiled_digits_pattern = re.compile(pattern=r"\d+")

    return sdp_checks_delete_dataframe_result_dictionary


def sdp_checks_add_dataframe_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """
    Checks for the sdp checks for the add sequence action
    :param dataframe: dataframe containing the input details for which the checks are needed.
    :param ip_node: ip node for which the checks are being performed
    :return sdp_checks_add_dataframe_result_dictionary(dict): returns the list of serial numbers with reason
    """
    logging.debug("Running the sdp_checks_add_dataframe_func for ip_node \'{ip_node}\'")
    sdp_checks_add_dataframe_result_dictionary = {}
    global sdp_starting_start_lines
    global mesh_sdp_lines_start_lines
    compiled_digits_pattern = re.compile(pattern=r"\d+")

    return sdp_checks_add_dataframe_result_dictionary


def lag_delete_action_dataframe_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """
    Performs the checks for lag section on Sequence Delete action dataframe
    :param dataframe: dataframe containing the input details for which the checks are needed
    :param ip_node: ip node for which the checks are being performed
    :return lag_delete_action_dataframe_check_result_dictionary (dict): returns the list of serial numbers with reason
    """
    logging.debug("Running the lag_delete_action_dataframe_checks_func for ip_node \'{ip_node}\'")
    lag_delete_action_dataframe_checks_result_dictionary = {}
    global lag_details_file_lines_list_block
    global sap_lag_starting_lines_from_service_lines_chunk
    compiled_pattern = re.compile(pattern=r"\d+")

    return lag_delete_action_dataframe_checks_result_dictionary


def lag_add_action_dataframe_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """
    Performs the checks for lag section on Sequence Add action dataframe
    :param dataframe: dataframe containing the input details for which the checks are needed
    :param ip_node: ip node for which the checks are being performed
    :return lag_add_action_dataframe_check_result_dictionary (dict): returns the list of serial numbers with reason
    """
    logging.debug(f"Running the lag_add_action_dataframe_checks_func for ip_node \'{ip_node}\'")
    lag_add_action_check_result_dictionary = {}
    global lag_details_file_lines_list_block
    global sap_lag_starting_lines_from_service_lines_chunk
    logging.info(f"starting checks for Add Section lag details check for VPLS-1 of {ip_node}")
    compiled_pattern = re.compile(pattern=r"\d+")

    if isinstance(sap_lag_starting_lines_from_service_lines_chunk, list):
        logging.info(f"{ip_node}: -sap_lag_starting_lines_from_service_lines_chunk ==> \n{'\n'.join(sap_lag_starting_lines_from_service_lines_chunk)}")

    return lag_add_action_check_result_dictionary


def sap_without_lag_add_dataframe_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """
    Performs the checks for sap without a lag section on Sequence Add action dataframe
    :param dataframe: dataframe containing the input details for which the checks are needed
    :param ip_node: ip node for which the checks are being performed
    :return sap_without_lag_add_dataframe_checks_result_dictionary (dict): returns the list of serial numbers with reason
    """
    logging.debug("Running the sap_without_lag_add_dataframe_checks_func for ip_node \'{ip_node}\'")

    global sap_starting_lines_from_service_lines_chunk
    global port_details_file_lines_list_block

    compiled_pattern = re.compile(pattern=r"[sap,\s,lag]+([esat\-,esat \-,\s,\d,/)]+)")
    logging.info(f'sap_starting_lines_from_service_lines_chunk=>\n{'\n'.join(sap_starting_lines_from_service_lines_chunk)}')
    sap_without_lag_add_dataframe_checks_result_dictionary = {}

    return sap_without_lag_add_dataframe_checks_result_dictionary


def sap_without_lag_delete_dataframe_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """
    Performs the checks for sap without a lag section on Sequence Delete action dataframe
    :param dataframe: dataframe containing the input details for which the checks are needed
    :param ip_node: ip node for which the checks are being performed
    :return sap_without_lag_delete_dataframe_checks_result_dictionary (dict): returns the list of serial numbers with reason.
    """
    logging.debug(f"Running the sap_without_lag_delete_dataframe_checks_func for ip_node \'{ip_node}\'")
    sap_without_lag_delete_dataframe_checks_result_dictionary = {}
    global sap_starting_lines_from_service_lines_chunk
    global port_details_file_lines_list_block

    compiled_pattern = re.compile(pattern=r"[sap,\s,lag]+([esat\-,esat \-,\s,\d,/)]+)")
    logging.info(f'sap_starting_lines_from_service_lines_chunk=>\n{'\n'.join(sap_starting_lines_from_service_lines_chunk)}')

    return sap_without_lag_delete_dataframe_checks_result_dictionary


def main_func(dataframe: pd.DataFrame, ip_node: str, running_config_backup_file_lines: list) -> dict:
    """
    Performs the Post Backup Node Checks for VPLS 1
    :param dataframe: contains the dataframe(tabular data) for the VPLS-1 Section of given ip_node for running_config checks
    :param ip_node: ip node for which the dataframe is passed
    :param running_config_backup_file_lines: list of lines from running_config_backup_file in which we need to perform checks
    :return result_dictionary (dict): {'Section Name': [list of 'S.No.' where there is any problem in template checks in any of the section] }
                                        or
                                    empty dictionary ===> {}
    """
    result_dictionary = {}

    # declaring all the global variables as None

    global service_file_lines_list_block
    service_file_lines_list_block = []

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

    # Creating Add Action Filtered Dataframe
    add_action_dataframe = dataframe[dataframe['Action'].str.upper().str.contains("ADD")]
    logging.info(
        f"Created the filtered dataframe for 'ADD' action for VPLS-1 Section for \"{ip_node}\":\n{add_action_dataframe.to_markdown()}"
    )

    # Creating Modify Action Filtered Dataframe
    modify_delete_action_dataframe = dataframe[dataframe['Action'].str.upper().str.contains("MODIFY|DELETE")]
    logging.debug(
        f"Got the dataframe for modify/delete action in VPLS-1 =>\n{modify_delete_action_dataframe.to_markdown()}\n"
    )

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
        if add_action_dataframe.shape[0] > 0:
            logging.debug(f"Creating the thread for checking the presence of VPLS ID clashes for {ip_node} for the dataframe\n{add_action_dataframe.to_markdown()}\n")
            add_action_result_dictionary_from_main_func = add_action_checks(add_action_dataframe,
                                                                            running_config_backup_file_lines,
                                                                            ip_node,
                                                                            vpls_id_starter_lines_filter)

            if len(result_dictionary) == 0:
                result_dictionary = add_action_result_dictionary_from_main_func

            else:
                result_dictionary.update(add_action_result_dictionary_from_main_func)

        if modify_delete_action_dataframe.shape[0] > 0:
            logging.debug(f"Calling the function for checking the sdp variable for {ip_node} for the dataframe\n{modify_delete_action_dataframe.to_markdown()}\n")
            modify_delete_result_dictionary_from_main_func = modify_delete_action_checks(modify_delete_action_dataframe,
                                                                                         running_config_backup_file_lines,
                                                                                         ip_node,
                                                                                         vpls_id_starter_lines_filter)
            if len(result_dictionary) == 0:
                result_dictionary = modify_delete_result_dictionary_from_main_func

            else:
                result_dictionary.update(modify_delete_result_dictionary_from_main_func)

        # Creating dataframe for add sequence with mesh sdp
        mesh_sdp_add_df = dataframe.loc[((~dataframe["Mesh-sdp"].str.startswith("TempNA")) & (dataframe["Sequence"].str.upper().str.endswith("ADD")))]
        logging.debug(f"Filtered the mesh sdp with sequence input \"Add\" for ip ==> \'{ip_node}\':\n{mesh_sdp_add_df.to_markdown()}\n")

        # Creating dataframe for modify sequence with mesh sdp
        mesh_sdp_delete_df = dataframe.loc[((~dataframe["Mesh-sdp"].str.startswith("TempNA")) & (dataframe["Sequence"].str.upper().str.endswith("DELETE")))]
        logging.debug(f"Filtered the mesh sdp with sequence input \"Delete\" for ip_node ==> \'{ip_node}\':\n{mesh_sdp_delete_df.to_markdown()}\n")

        if mesh_sdp_add_df.shape[0] > 0:
            if sdp_existence_status_dictionary is None:
                sdp_existence_status_dictionary = {}

            logging.debug(f"Calling method for mesh_sdp_add checks for ip_node \'{ip_node}\' ==>\n{mesh_sdp_add_df.to_markdown()}\n")
            mesh_sdp_add_result_dictionary_from_main_func = sdp_checks_add_dataframe_func(mesh_sdp_add_df,
                                                                                          ip_node)
            if len(result_dictionary) == 0:
                result_dictionary = mesh_sdp_add_result_dictionary_from_main_func
            else:
                result_dictionary.update(mesh_sdp_add_result_dictionary_from_main_func)

        if mesh_sdp_delete_df.shape[0] > 0:
            if sdp_existence_status_dictionary is None:
                sdp_existence_status_dictionary = {}

            logging.debug(f"Calling method for mesh_sdp_delete checks for ip_node \'{ip_node}\' ==>\n{mesh_sdp_delete_df.to_markdown()}\n")
            mesh_sdp_delete_result_dictionary_from_main_func = sdp_checks_delete_dataframe_func(mesh_sdp_delete_df,
                                                                                                ip_node)
            if len(result_dictionary) == 0:
                result_dictionary = mesh_sdp_delete_result_dictionary_from_main_func

            else:
                result_dictionary.update(mesh_sdp_delete_result_dictionary_from_main_func)

        # Creating a filtered dataframe for design input for sap with lag
        sap_lag_dataframe = dataframe.loc[((~dataframe["Sap/Lag"].str.strip().str.startswith("TempNA")) & (dataframe["Sap/Lag"].str.strip().str.startswith("sap lag")))]

        # Creating filtered dataframe for design input for sap with lag for add sequence
        sap_lag_add_dataframe = sap_lag_dataframe.loc[sap_lag_dataframe["Sequence"].str.strip().str.lower().str.endswith("add")]
        logging.info(
            f"Got the sap_lag_add_dataframe for ip \'{ip_node}\'\n{sap_lag_add_dataframe.to_markdown()}"
        )

        # Creating filtered dataframe for design input for sap with lag for delete sequence
        sap_lag_delete_dataframe = sap_lag_dataframe.loc[sap_lag_dataframe["Sequence"].str.strip().str.lower().str.endswith("delete")]
        logging.info(
            f"Got the sap_lag_delete_dataframe for ip \'{ip_node}\'\n{sap_lag_delete_dataframe.to_markdown()}"
        )

        # Creating filtered dataframe for design input for sap without lag
        sap_without_lag_dataframe = dataframe.loc[
            (~dataframe["Sap/Lag"].str.strip().str.startswith("TempNA")) & (dataframe["Sap/Lag"].str.match(r"(\s*)sap([-,\d,\s,\w]+)/([\d,\s])/([\d,\s])([:,\d,\s]*)$"))]

        # Creating filtered dataframe for design input for sap without lag for add sequence
        sap_without_lag_add_dataframe = sap_without_lag_dataframe.loc[(sap_without_lag_dataframe["Sequence"]).str.strip().str.lower().str.endswith("add")]
        logging.info(
            f"Got the sap_without_lag_add_dataframe for ip \'{ip_node}\'\n{sap_without_lag_add_dataframe.to_markdown()}"
        )

        # Creating filtered dataframe for design input for sap without lag for delete sequence
        sap_without_lag_delete_dataframe = sap_without_lag_dataframe.loc[sap_without_lag_dataframe["Sequence"].str.strip().str.lower().str.endswith("delete")]
        logging.info(
            f"Got the sap_without_lag_delete_dataframe for ip \'{ip_node}\'\n{sap_without_lag_delete_dataframe.to_markdown()}"
        )

        if (sap_lag_add_dataframe.shape[0] > 0) and ((isinstance(sap_lag_starting_lines_from_service_lines_chunk, list)) and (len(sap_lag_starting_lines_from_service_lines_chunk) > 0)):
            lag_add_action_dataframe_checks_result_dictionary_from_main_func = lag_add_action_dataframe_checks_func(sap_lag_add_dataframe,
                                                                                                                    ip_node)

            if len(result_dictionary) == 0:
                result_dictionary = lag_add_action_dataframe_checks_result_dictionary_from_main_func

            else:
                result_dictionary.update(lag_add_action_dataframe_checks_result_dictionary_from_main_func)

            logging.info(
                f'{ip_node}: - Updated the result dictionary with sap_without_lag_dataframe_delete_action_result_dictionary\n \'{'{\n'}\'' +
                f'{''.join([f'{key} : {value}' for key, value in lag_add_action_dataframe_checks_result_dictionary_from_main_func.items()])}' +
                '}'
            )

        if (sap_lag_delete_dataframe.shape[0] > 0) and ((isinstance(sap_lag_starting_lines_from_service_lines_chunk, list)) and (len(sap_lag_starting_lines_from_service_lines_chunk) > 0)):
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

        if (sap_without_lag_add_dataframe.shape[0] > 0) and ((isinstance(sap_starting_lines_from_service_lines_chunk, list)) and (len(sap_starting_lines_from_service_lines_chunk) > 0)):
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

        if (sap_without_lag_delete_dataframe.shape[0] > 0) and ((isinstance(sap_starting_lines_from_service_lines_chunk, list)) and (len(sap_starting_lines_from_service_lines_chunk) > 0)):
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

    except Exception as e:
        logging.error(f"{traceback.format_exc()}\nException Occurred!==>\n Title ==> {type(e)}\n Message ==> {str(e)}")
        title = str(type(e))
        message = str(e)
        messagebox.showerror(title=title,
                             message=message)
        result_dictionary = {}

    finally:
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
