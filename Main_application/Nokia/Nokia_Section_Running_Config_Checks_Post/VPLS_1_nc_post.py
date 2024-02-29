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
# sdp_existence_status_dictionary = {}
sap_lag_starting_lines_from_service_lines_chunk = []
sap_starting_lines_from_service_lines_chunk = []
result_dictionary = {}
vpls_chunks_dictionary = {}
vpls_state_dictionary = {}


class CustomException(Exception):
    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message
        super().__init__(self.title, self.message)

def add_modify_sequence_action_checks(dataframe: pd.DataFrame, running_config_backup_file_lines: list, ip_node: str, vpls_id_starter_lines_filter: list) -> None:
    """
    Performs the Checks for the presence of VPLS ID in the post running config backup files
    :param dataframe: filtered dataframe with Action "A:Add" from the node ip Section dataframe
    :param running_config_backup_file_lines: List of lines from running config backup lines
    :param ip_node: Node IP for which the checks are being done
    :param vpls_id_starter_lines_filter: list of lines starting with vpls keyword
    :return None
    """
    # result_dictionary (dict): dictionary containing the error results
    #                                   dictionary structure => {
    #                                                             error_reason: [list of S.No. with the errors]
    #                                                         }
    #                                                         or
    #                                                         empty dictionary -> {}

    logging.debug(f"inside {__name__} for ip_node ==> {ip_node}")
    logging.debug(f"got the dataframe for ip_node {ip_node} =>\n{dataframe.to_markdown()}")

    # add_action_checks_result_dictionary = {}
    global result_dictionary
    global service_file_lines_list_block
    global vpls_chunks_dictionary

    reason = "VPLS ID not found"
    reason2 = "VPLS Name not configured"

    unique_vpls_ids = dataframe['VPLS ID'].unique().astype(float)
    unique_vpls_ids = unique_vpls_ids.astype(int)

    dataframe['VPLS ID'] = dataframe.loc[:, 'VPLS ID'].astype(float).astype(int)

    i = 0

    while i < unique_vpls_ids.size:
        string_to_be_searched = f'vpls {unique_vpls_ids[i]}'
        temp_df = dataframe.loc[dataframe['VPLS ID'] == unique_vpls_ids[i]]
        vpls_chunk_file_lines = vpls_chunks_dictionary[unique_vpls_ids[i]]
        vpls_found = False

        j = 0
        while j < len(vpls_id_starter_lines_filter):
            if str(vpls_id_starter_lines_filter[j]).startswith(string_to_be_searched):
                vpls_found = True
                break
            j += 1

        if not vpls_found:
            if reason not in result_dictionary:
                result_dictionary[reason] = []
                result_dictionary[reason].extend(temp_df['S.No.'].astype(float).astype(int))

            else:
                sr_list = [s_no for s_no in temp_df['S.No.'].astype(float).astype(int) if s_no not in result_dictionary[reason]]
                result_dictionary[reason].extend(sr_list)

        if (vpls_found) and (str(temp_df.iloc[0, temp_df.columns.get_loc("Action")]).strip().upper().endswith("ADD")):
            vpls_name = temp_df.iloc[0, temp_df.columns.get_loc('VPLS Name')]
            vpls_name_found = False
            j = 0
            while j < len(vpls_chunk_file_lines):
                if str(vpls_chunk_file_lines[j]).__contains__(vpls_name):
                    vpls_name_found = True
                    break
                j += 1

            if not vpls_name_found:
                if reason not in result_dictionary:
                    result_dictionary[reason2] = []
                    result_dictionary[reason2].extend(temp_df['S.No.'])

                else:
                    result_dictionary[reason2].extend(temp_df['S.No.'])
        i += 1

    logging.info(
        f"{ip_node}:- add_modify_sequence_action_checks"
        "{\n}"
        f"{'\n'.join([f'{key}: {', '.join([str(value) for value in values])}' for key,values in result_dictionary.items()])}"
        "\n}"
    )
    # return add_action_checks_result_dictionary



def sdp_checks_delete_dataframe_func(dataframe: pd.DataFrame, ip_node: str) -> None:
    """
    Checks for the sdp checks for the delete sequence action
    :param dataframe: dataframe containing the input details for which the checks are needed.
    :param ip_node: ip node for which the checks are being performed
    :return None
    """
    logging.debug(f"Running the sdp_checks_delete_dataframe_func for ip_node \'{ip_node}\'")
    # sdp_checks_delete_dataframe_result_dictionary = {}

    global result_dictionary
    global sdp_starting_start_lines
    global service_file_lines_list_block
    global vpls_chunks_dictionary

    # global mesh_sdp_lines_start_lines
    # compiled_digits_pattern = re.compile(pattern=r"\d+")

    # reason = "Given SDP not found"
    reason2 = "Given Mesh-SDP not removed"

    unique_vpls_ids = dataframe["VPLS ID"].unique().astype(float)
    unique_vpls_ids = unique_vpls_ids.astype(int)
    dataframe['VPLS ID'] = dataframe.loc[:, 'VPLS ID'].astype(float).astype(int)

    i = 0
    while i < unique_vpls_ids.size:
        temp_df = dataframe.loc[dataframe['VPLS ID'] == unique_vpls_ids[i]]
        # vpls_chunk_list = flh().file_lines_chunk_divisor(file_lines_list=service_file_lines_list_block,
        #                                                      start_string= f"vpls {unique_vpls_ids[i]}",
        #                                                      end_string_pattern= r"^vpls/s*/w+")
        vpls_chunk_list = vpls_chunks_dictionary[unique_vpls_ids[i]]

        j = 0
        while j < temp_df.shape[0]:

            mesh_sdp_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp")])
            mesh_sdp_variable_found = False
            k = 0
            while k < len(vpls_chunk_list):
                if str(vpls_chunk_list[k]).startswith(mesh_sdp_variable):
                    mesh_sdp_variable_found = True
                k += 1

            if mesh_sdp_variable_found:
                if reason2 not in result_dictionary:
                    result_dictionary[reason2] = []
                    result_dictionary[reason2].append(int(temp_df.iloc[j, temp_df.columns.get_loc("S.No.")]))

                else:
                    result_dictionary[reason2].append(int(temp_df.iloc[j, temp_df.columns.get_loc("S.No.")]))

            j += 1
        i += 1

    logging.info(
        f"{ip_node}:- sdp_checks_delete_datframe_func "
        "{\n"
        f"{'\n'.join([f'{key}: {', '.join([str(value) for value in values])}' for key,values in result_dictionary.items()])}"
        "\n}"
    )

    # return sdp_checks_delete_dataframe_result_dictionary


def sdp_checks_add_modify_dataframe_func(dataframe: pd.DataFrame, ip_node: str) -> None:
    """
    Checks for the sdp checks for the add sequence action
    :param dataframe: dataframe containing the input details for which the checks are needed.
    :param ip_node: ip node for which the checks are being performed
    :return None
    """
    # sdp_checks_add_dataframe_result_dictionary(dict): returns the list of serial numbers with reason

    logging.debug(f"Running the sdp_checks_add_modify_dataframe_func for ip_node \'{ip_node}\'")
    # sdp_checks_add_dataframe_result_dictionary = {}
    global result_dictionary
    global sdp_starting_start_lines
    global service_file_lines_list_block
    global vpls_chunks_dictionary
    # global mesh_sdp_lines_start_lines
    compiled_digits_pattern = re.compile(pattern=r"\d+")

    reason = "Given SDP not found"
    reason2 = "Given Mesh-SDP not configured"

    unique_vpls_ids = dataframe["VPLS ID"].unique().astype(float)
    unique_vpls_ids = unique_vpls_ids.astype(int)

    dataframe['VPLS ID'] = dataframe.loc[:, 'VPLS ID'].astype(float).astype(int)

    i = 0
    while i < unique_vpls_ids.size:
        temp_df = dataframe.loc[dataframe['VPLS ID'] == unique_vpls_ids[i]]
        # vpls_chunk_list = flh().file_lines_chunk_divisor(file_lines_list=service_file_lines_list_block,
        #                                                      start_string= f"vpls {unique_vpls_ids[i]}",
        #                                                      end_string_pattern= r"^vpls/s*/w+")

        j = 0
        while j < temp_df.shape[0]:
            sdp_variable = re.findall(compiled_digits_pattern, str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp")]))[0]
            logging.debug(
                f"{ip_node}: - Cheking for sdp variable \'{sdp_variable}\' for vpls_id {unique_vpls_ids[i]}"
            )
            sdp_variable_found = False

            k = 0
            while k < len(sdp_starting_start_lines):
                if sdp_starting_start_lines[k].startswith(f"sdp {sdp_variable} "):
                    sdp_variable_found = True
                    break
                k += 1

            if not sdp_variable_found:
                if reason not in result_dictionary:
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(int(temp_df.iloc[j, temp_df.columns.get_loc("S.No.")]))

                else:
                    result_dictionary[reason].append(int(temp_df.iloc[j, temp_df.columns.get_loc("S.No.")]))

            mesh_sdp_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp")])
            logging.debug(
                f"{ip_node}: - Got the mesh-sdp line \'{mesh_sdp_variable}\' for vpls id \'{unique_vpls_ids[i]}\'"
            )
            mesh_sdp_variable_found = False

            k = 0
            logging.debug(
                f"{ip_node}: - Checking for the mesh-sdp line for vpls \'{unique_vpls_ids[i]}\'\n"
                f"{'\n'.join(vpls_chunks_dictionary[unique_vpls_ids[i]])}"
            )
            while k < len(vpls_chunks_dictionary[unique_vpls_ids[i]]):
                line = str(vpls_chunks_dictionary[unique_vpls_ids[i]][k])
                if line.startswith(mesh_sdp_variable):
                    mesh_sdp_variable_found = True
                k += 1

            if not mesh_sdp_variable_found:
                if reason2 not in result_dictionary:
                    result_dictionary[reason2] = []
                    result_dictionary[reason2].append(int(temp_df.iloc[j, temp_df.columns.get_loc("S.No.")]))

                else:
                    result_dictionary[reason2].append(int(temp_df.iloc[j, temp_df.columns.get_loc("S.No.")]))

            j += 1
        i += 1

    logging.info(
        f"{ip_node} :- sdp_checks_add_modify_dataframe_func"
        " {\n"
        f"{'\n'.join([f'{key} : {', '.join([str(value) for value in values])}' for key,values in result_dictionary.items()])}"
        "\n}"
    )
    # return sdp_checks_add_dataframe_result_dictionary


def sap_field_non_blank_filtered_df_with_sequence_add_and_modify_checks(dataframe: pd.DataFrame, ip_node: str) -> None:
    """Checks for sap field with sequence add or modify

    Args:
        dataframe (pd.DataFrame): filtered dataframe with sap field non blank
        ip_node (str): ip node for which the checks are being performed
    """

    logging.info(f"{ip_node}: - Starting the checks for sap field with add or modify sequence")

    global vpls_chunks_dictionary

    unique_vpls_ids = dataframe['VPLS ID'].unique().astype(float)
    unique_vpls_ids = unique_vpls_ids.astype(int)

    logging.info(f"{ip_node}: - list of unique vpls ids\n[{','.join(str(id) for id in unique_vpls_ids)}]")

    dataframe['VPLS ID'] = dataframe.loc[:, 'VPLS ID'].astype(float).astype(int)

    reason = "Given Sap entry not configured"

    i = 0
    while i < unique_vpls_ids.size:
        temp_df = dataframe.loc[dataframe["VPLS ID"] == unique_vpls_ids[i]]

        j = 0
        while j < temp_df.shape[0]:
            sap_variable = temp_df.iloc[j, temp_df.columns.get_loc("Sap/Lag")]
            sap_variable_found = False

            vpls_chunk_file_list = vpls_chunks_dictionary[int(unique_vpls_ids[i])]
            logging.debug(
                f"{ip_node}: - Checking the sap entry \'{sap_variable}\' for vpls_id \'{unique_vpls_ids[i]}\'"
            )

            logging.debug(
                f"{ip_node}: - Got vpls chunk for vpls id \'{unique_vpls_ids[i]}\'=>\n{'\n'.join(vpls_chunk_file_list)}"
            )

            k = 0
            while k < len(vpls_chunk_file_list):
                line = str(vpls_chunk_file_list[k]).strip()
                if line.__contains__(sap_variable):
                    sap_variable_found = True
                    break

                k += 1

            if not sap_variable_found:
                if reason not in result_dictionary:
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(int(temp_df.iloc[j, temp_df.columns.get_loc("S.No.")]))

                else:
                    result_dictionary[reason].append(int(temp_df.iloc[j, temp_df.columns.get_loc("S.No.")]))
            j += 1
        i += 1

    logging.info(
        f"{ip_node}:- sap_field_non_blank_filtered_df_with_sequence_add_and_modify_checks "
        "{\n"
        f"{'\n'.join([f'{key}: {', '.join([str(value) for value in values])}' for key,values in result_dictionary.items()])}"
        "\n}"
    )



def sap_field_non_blank_filtered_df_with_sequence_delete_checks(dataframe: pd.DataFrame, ip_node: str):
    """Checks for sap field with sequence delete

    Args:
        dataframe (pd.DataFrame): filtered dataframe with sap field non blank
        ip_node (str): ip node for which the checks are being performed
    """

    logging.info(f"{ip_node}: - Starting the checks for sap field with delete sequence")

    global vpls_chunks_dictionary

    unique_vpls_ids = dataframe['VPLS ID'].unique().astype(float)
    unique_vpls_ids = unique_vpls_ids.astype(int)

    logging.info(f"{ip_node}: - list of unique vpls ids\n[{','.join(unique_vpls_ids.astype(str))}]")

    dataframe['VPLS ID'] = dataframe.loc[:, 'VPLS ID'].astype(float).astype(int)

    reason = "Given Sap not removed"

    i = 0
    while i < unique_vpls_ids.size:
        temp_df = dataframe.loc[dataframe["VPLS ID"] == unique_vpls_ids[i]]

        j = 0
        while j < temp_df.shape[0]:
            sap_variable = temp_df.iloc[j, temp_df.columns.get_loc("Sap/Lag")]
            sap_variable_found = False

            vpls_chunk_file_list = vpls_chunks_dictionary[unique_vpls_ids[i]]

            k = 0
            while k < len(vpls_chunk_file_list):
                line = str(vpls_chunk_file_list[k]).strip()
                if line.__contains__(sap_variable):
                    sap_variable_found = True
                    break

                k += 1

            if sap_variable_found:
                if reason not in result_dictionary:
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(int(temp_df.iloc[j, temp_df.columns.get_loc("S.No.")]))

                else:
                    result_dictionary[reason].append(int(temp_df.iloc[j, temp_df.columns.get_loc("S.No.")]))
            j += 1
        i += 1

    logging.info(
        f"{ip_node}:- sap_field_non_blank_filtered_df_with_sequence_delete_checks "
        "{\n"
        f"{'\n'.join([f'{key}: {', '.join([str(value) for value in values])}' for key,values in result_dictionary.items()])}"
        "\n}"
    )



def show_service_using_vpls_state_dictionary_creater(file_lines_list: list, ip_node: str, dataframe: pd.DataFrame) -> dict:
    """Creates Dictionary from the dataframe created from the captured output of command 'show service service-using vpls'

    Args:
        file_lines_list (list): list of lines from the running config backup file
        ip_node (str): ip node for which the checks being done
        dataframe (pd.DataFrame): dataframe containing the entire data for VPLS-1 for selected ip

    Returns:
        vpls_state_dictionary (dict): dictionary containing the vpls_states
    """

    vpls_state_dictionary = {}

    filtered_lines = []
    compiled_pattern = re.compile(pattern= r"^\d+")

    i = 0
    while i < len(file_lines_list):
        line = str(file_lines_list).strip()
        if re.search(pattern= compiled_pattern, string=line) is not None:
            filtered_lines.append(line)
        i += 1

    logging.info(
        f"{ip_node}: - Created the filtered lines\n[\n"
        f"{'\n'.join(filtered_lines)}"
        "\n]"
    )
    required_columns = ["ServiceId", "Type", "Adm", "Opr", "CustomerId", "Service Name"]

    if len(filtered_lines[0].split()) != len(required_columns):
        result_dictionary["Length of line for \'show service service-using vpls\' is not equal"] = list(dataframe["S.No."].astype(float).astype(int))
        raise CustomException("Length Mismatch", "Length of line for \'show service service-using vpls\' is not equal")

    i = 0
    while i < len(filtered_lines):
        filtered_lines[i] = filtered_lines[i].split()
        i += 1

    logging.info(
        f"{ip_node}: - Created the filtered lines after splitting\n[\n"
        f"{'\n'.join(filtered_lines)}"
        "\n]"
    )

    dataframe_from_show_service_using_vpls = pd.DataFrame(data= filtered_lines, columns= required_columns)

    logging.info(
        f"{ip_node}: - Created the dataframe from the \'show service service-using vpls\'\n"
        f"{dataframe_from_show_service_using_vpls.to_markdown()}\n"
    )

    vpls_state_dictionary = dict(zip(dataframe_from_show_service_using_vpls["ServiceID"].astype(float).astype(int), dataframe_from_show_service_using_vpls["Opr"]))

    logging.info(
        f"{ip_node}: - {'\n'.join([f'{key} : {value}' for key,value in vpls_state_dictionary.items()])}"
    )
    return vpls_state_dictionary



def vpls_state_checker(dataframe: pd.DataFrame, ip_node:str) -> None:
    """Checks the state of the VPLS and adds the Serial Number containing the VPLS for which the state is down to the result dictionary.

    Args:
        dataframe (pd.DataFrame): dataframe containing the sequence "Add", "Modify", and "Delete"
        ip_node (str): ip node for which the VPLS states are being checked.
    """

    global result_dictionary
    global vpls_state_dictionary

    logging.info(
        f"{ip_node}: - Starting the checks for vpls_state_dictionary"
    )

    unique_vpls_ids = dataframe["VPLS ID"].unique().astype(float).astype(int)

    logging.info(
        f"{ip_node}: - Unique vpls ids in passed dataframe\n{dataframe.to_markdown()}\n["
        f"{', '.join(unique_vpls_ids.astype(str))}"
        "\n]"
    )

    dataframe["VPLS ID"] = dataframe.loc[:, "VPLS ID"].astype(float).astype(int)

    reason = "Given VPLS id found to be 'Down' state"
    i = 0
    while i < unique_vpls_ids.size:
        selected_vpls_id = unique_vpls_ids[i]
        if str(vpls_state_dictionary[selected_vpls_id]).strip().upper() != "UP":
            temp_df = dataframe.loc[dataframe["VPLS ID"] == unique_vpls_ids[i]]

            temp_df["S.No."] = temp_df.loc[:, "S.No."].astype(float).astype(int)

            if reason not in result_dictionary:
                result_dictionary[reason] = []
                result_dictionary[reason].extend(temp_df["S.No."].astype(float).astype(int))

            else:
                result_dictionary[reason].extend(temp_df["S.No."].astype(float).astype(int))
        i += 1

    logging.info(
        f"{ip_node}:- vpls_state_checker "
        "{\n"
        f"{'\n'.join([f'{key}: {', '.join([str(value) for value in values])}' for key,values in result_dictionary.items()])}"
        "\n}"
    )



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

    global result_dictionary
    result_dictionary = {}

    # declaring all the global variables as None

    global service_file_lines_list_block
    service_file_lines_list_block = []

    global vpls_state_dictionary
    vpls_state_dictionary = {}

    global port_details_file_lines_list_block, lag_details_file_lines_list_block, mesh_sdp_lines_start_lines, sdp_starting_start_lines
    global vpls_chunks_dictionary
    vpls_chunks_dictionary = {}

    # global sdp_existence_status_dictionary
    port_details_file_lines_list_block = []
    lag_details_file_lines_list_block = []
    mesh_sdp_lines_start_lines = []
    sdp_starting_start_lines = []
    # sdp_existence_status_dictionary = {}

    # global exception_raised
    # exception_raised = False

    global sap_lag_starting_lines_from_service_lines_chunk
    sap_lag_starting_lines_from_service_lines_chunk = []

    global sap_starting_lines_from_service_lines_chunk
    sap_starting_lines_from_service_lines_chunk = []

    show_service_service_using_vpls_lines_list = []
    compiled_pattern = re.compile(r"^A\s*:\s*([A-Z,_,\d]+)#([-,\s*,\w+]+)$")
    host_name = ""

    dataframe = dataframe.where(~dataframe.isna(), "TempNA")

    # Commented Right Now but needed
    # show_service_service_using_vpls_line_found = False
    running_config_backup_file_lines = flh().file_lines_cleaner(file_lines_list=running_config_backup_file_lines)
    # i = 0
    # while i < len(running_config_backup_file_lines):
    #     line = (running_config_backup_file_lines[i]).strip()
    #     if line.endswith("show service service-using vpls"):
    #         host_name = re.search(pattern=compiled_pattern, string=line).group(1)
    #         show_service_service_using_vpls_line_found = True
    #         show_service_service_using_vpls_lines_list = flh().file_lines_chunk_divisor_pattern(file_lines_list=running_config_backup_file_lines[i:],
    #                                                                                             starting_string_pattern= rf'[A,\s,:]*{host_name}\s*#\s*show service service-using vpls',
    #                                                                                             end_string_pattern= r"^A\s*:\s*([A-Z,_,\d]+)#([-,\s*,\w+]+)$")
    #         break
    #     i += 1

    try:
        # Commented Right Now but needed
        # if not show_service_service_using_vpls_line_found:
        #     result_dictionary["Post Running Config Backup chunk containing the states of vpls not found"] = list(dataframe["S.No."].astype(float).astype(int))
        #     raise CustomException(title= "Vpls state not found",
        #                                 message= "File chunk containing the states of vpls not found!")

        # vpls_state_dictionary = show_service_using_vpls_state_dictionary_creater(file_lines_list= show_service_service_using_vpls_lines_list,
        #                                                                         ip_node= ip_node,
        #                                                                         dataframe= dataframe)

        # vpls_state_checker(dataframe= dataframe,
        #                 ip_node= ip_node)

        # global flag;

        # Creating Add Action Filtered Dataframe
        add_modify_sequence_dataframe = dataframe[dataframe['Sequence'].str.upper().str.contains("ADD|MODIFY")]
        logging.info(
            f"Created the filtered dataframe for 'ADD' action for VPLS-1 Section for \"{ip_node}\":\n{add_modify_sequence_dataframe.to_markdown()}"
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

        port_details_file_lines_list_block_thread = CustomThread(target=flh().file_lines_chunk_divisor,
                                                                args=(running_config_backup_file_lines,
                                                                    'echo \"Port Configuration\"',
                                                                    r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration"$'))

        port_details_file_lines_list_block_thread.start()

        logging.info(f"Got the port_details_file_lines_list_block for \"{ip_node}\"")

        lag_details_file_lines_list_block_thread = CustomThread(target=flh().file_lines_chunk_divisor,
                                                                args=(running_config_backup_file_lines,
                                                                    'echo \"LAG Configuration\"',
                                                                    r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration"$'))

        lag_details_file_lines_list_block_thread.start()

        logging.info(f"Got the lag_details_file_lines_list_block for \"{ip_node}\"")

        service_file_lines_list_block = service_file_lines_list_block_thread.join()
        logging.info(f"Got the service_file_list_block for \"{ip_node}\"=> {'\n'.join(str(line) for line in service_file_lines_list_block)}")

        port_details_file_lines_list_block = port_details_file_lines_list_block_thread.join()
        lag_details_file_lines_list_block = lag_details_file_lines_list_block_thread.join()

        mesh_sdp_lines_start_lines_thread = CustomThread(target=flh().file_lines_starter_filter,
                                                        args=(service_file_lines_list_block,
                                                            "mesh-sdp "))

        mesh_sdp_lines_start_lines_thread.start()

        sdp_starting_start_lines_thread = CustomThread(target=flh().file_lines_starter_filter,
                                                    args=(service_file_lines_list_block,
                                                            "sdp "))

        sdp_starting_start_lines_thread.start()

        mesh_sdp_lines_start_lines = mesh_sdp_lines_start_lines_thread.join()

        if isinstance(mesh_sdp_lines_start_lines, list):
            logging.debug(f"Created file lines filter with lines starting with 'mesh-sdp' for ip_node \'{ip_node}\' with len==>\n{len(mesh_sdp_lines_start_lines)}\n")

        sdp_starting_start_lines = sdp_starting_start_lines_thread.join()
        if isinstance(sdp_starting_start_lines, list):
            logging.debug(
                f"{ip_node}: - sdp_starting_start_lines=>\n{'\n'.join(sdp_starting_start_lines)}"
            )

        sap_lag_starting_lines_from_service_lines_chunk_thread = CustomThread(target=flh().file_lines_starter_filter,
                                                                            args=(service_file_lines_list_block,
                                                                                    "sap lag-"))

        logging.debug(f"Creating the file_lines_chunk for sap_lag for VPLS-1 for ip_node ==> {ip_node}")

        sap_lag_starting_lines_from_service_lines_chunk_thread.start()

        sap_starting_lines_from_service_lines_chunk_thread = CustomThread(target=flh().file_lines_starter_filter,
                                                                        args=(service_file_lines_list_block,
                                                                                "sap "))

        # sap_starting_lines_from_service_lines_chunk_thread.daemon = True
        sap_starting_lines_from_service_lines_chunk_thread.start()

        sap_lag_starting_lines_from_service_lines_chunk = sap_lag_starting_lines_from_service_lines_chunk_thread.join()
        logging.debug(f"Created the sap_lag_starting_file_lines_chunk for sap_lag for VPLS-1 for ip_node ==> {ip_node} with => {len(sap_lag_starting_lines_from_service_lines_chunk) = }\n")

        sap_lag_starting_lines_from_service_lines_chunk = sap_starting_lines_from_service_lines_chunk_thread.join()
        sap_starting_lines_from_service_lines_chunk = sap_starting_lines_from_service_lines_chunk_thread.join()

        add_modify_action_checks = dataframe.loc[~dataframe["Action"].str.strip().str.startswith('TempNA') & dataframe["Action"].str.strip().str.upper().str.contains("ADD|MODIFY")]

        logging.info(
            f"{ip_node}: - add_modify_action_checks \n{add_modify_action_checks.to_markdown()}"
        )

        i = 0
        while i < add_modify_action_checks.shape[0]:
            vpls_id = add_modify_action_checks.iloc[i, add_modify_action_checks.columns.get_loc('VPLS ID')]
            logging.info(
                f"{ip_node}: - Creating the file list chunk for vpls id {vpls_id}"
            )
            vpls_chunks_dictionary[int(vpls_id)] = flh().file_lines_chunk_divisor(file_lines_list=service_file_lines_list_block,
                                                                                start_string= f"vpls {vpls_id} ",
                                                                                end_string_pattern= r"^(vpls|vprn|echo|interface)+\s*\w+")
            logging.info(
                f"\n\n{ip_node}: - vpls_chunks_dictionary[{int(vpls_id)}] => \n\t\t{'\n'.join(str(line) for line in vpls_chunks_dictionary[int(vpls_id)])}"
            )

            i += 1

        # logging.info(f"{ip_node}: - Vpls_chunks_dictionary => \n{'\n'.join([f'{key}: {'\t\t\n'.join([str(value) for value in values])}' for key, values in vpls_chunks_dictionary.items()])}")
        logging.info(f"{ip_node}: - Vpls_chunks_dictionary => \n{vpls_chunks_dictionary}")

        if add_modify_sequence_dataframe.shape[0] > 0:
            logging.debug(f"Creating the thread for checking the presence of VPLS ID clashes for {ip_node} for the dataframe\n{add_modify_sequence_dataframe.to_markdown()}\n")

            add_modify_sequence_action_checks(add_modify_sequence_dataframe,
                                              running_config_backup_file_lines,
                                              ip_node,
                                              vpls_id_starter_lines_filter)

        # Creating dataframe for add sequence with mesh sdp
        mesh_sdp_add_modify_df = dataframe.loc[((~dataframe["Mesh-sdp"].str.startswith("TempNA")) & (dataframe["Sequence"].str.upper().str.contains("ADD|MODIFY",regex=True)))]
        logging.debug(f"Filtered the mesh sdp with sequence input \"Add\" for ip ==> \'{ip_node}\':\n{mesh_sdp_add_modify_df.to_markdown()}\n")

        # Creating dataframe for modify sequence with mesh sdp
        mesh_sdp_delete_df = dataframe.loc[((~dataframe["Mesh-sdp"].str.startswith("TempNA")) & ((dataframe["Action"].str.upper().str.endswith("MODIFY")) & (dataframe["Sequence"].str.upper().str.endswith("DELETE"))))]
        logging.debug(f"Filtered the mesh sdp with sequence input \"Delete\" for ip_node ==> \'{ip_node}\':\n{mesh_sdp_delete_df.to_markdown()}\n")

        if mesh_sdp_add_modify_df.shape[0] > 0:

            logging.debug(f"Calling method for mesh_sdp_add checks for ip_node \'{ip_node}\' ==>\n{mesh_sdp_add_modify_df.to_markdown()}\n")

            sdp_checks_add_modify_dataframe_func(mesh_sdp_add_modify_df,
                                                 ip_node)

        if mesh_sdp_delete_df.shape[0] > 0:

            logging.debug(f"Calling method for mesh_sdp_delete checks for ip_node \'{ip_node}\' ==>\n{mesh_sdp_delete_df.to_markdown()}\n")

            sdp_checks_delete_dataframe_func(mesh_sdp_delete_df,
                                             ip_node)

        sap_field_non_blank_filtered_df_with_sequence_add_or_modify = dataframe.loc[(~dataframe['Sap/Lag'].str.strip().str.endswith('TempNA')) & (dataframe['Sequence'].str.strip().str.upper().str.contains("ADD|MODIFY"))]

        sap_field_non_blank_filtered_df_with_sequence_delete = dataframe.loc[(~dataframe['Sap/Lag'].str.strip().str.endswith('TempNA')) & (dataframe['Sequence'].str.strip().str.upper().str.endswith("DELETE"))]

        if sap_field_non_blank_filtered_df_with_sequence_add_or_modify.shape[0] > 0:

            logging.info(f"{ip_node}: - filtered df for sap with sequence add or modify\n{sap_field_non_blank_filtered_df_with_sequence_add_or_modify.to_markdown()}")
            sap_field_non_blank_filtered_df_with_sequence_add_and_modify_checks(dataframe=sap_field_non_blank_filtered_df_with_sequence_add_or_modify,
                                                                                ip_node=ip_node)



        if sap_field_non_blank_filtered_df_with_sequence_delete.shape[0] >0:

            logging.info(f"{ip_node}: - filtered df for sap with sequence delete\n{sap_field_non_blank_filtered_df_with_sequence_delete.to_markdown()}")

            sap_field_non_blank_filtered_df_with_sequence_delete_checks(dataframe= sap_field_non_blank_filtered_df_with_sequence_delete,
                                                                        ip_node= ip_node)

    except CustomException as e:
        logging.error(
            "Exception Occurred!==>\n"
            f"\t\tTitle ==> {e.title}\n"
            f"\t\t\tMessage ==> {e.message}\n"
        )


    except Exception as e:
        logging.error(f"{traceback.format_exc()}\nException Occurred!==>\n Title ==> {e.__class__.__name__}\n Message ==> {str(e)}")
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
