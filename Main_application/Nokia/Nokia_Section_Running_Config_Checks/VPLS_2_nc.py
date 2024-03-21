import logging
import traceback
from tkinter import messagebox

import numpy as np
import pandas as pd

from Main_application.CustomThread import CustomThread
from Main_application.file_lines_handler import File_lines_handler as flh

result_dictionary = {}
vpls_section_filter_lines_list = []
service_file_lines_list_block = []
global_running_config_backup_file_lines = []
port_details_file_lines_list = []


def common_checks_for_sequence_add(ip_node: str, dataframe: pd.DataFrame):
    """Performs the common checks for \'ADD\' sequence filtered dataframe irrespective of action.

    Args:
        ip_node (str): ip node for which the checks are being performed
        dataframe (pd.DataFrame): \'ADD\' action filtered dataframe
    """

    logging.debug(
        f"{ip_node}: - inside {__name__}"
    )

    global result_dictionary

    reason = "Route-distinguisher Clash found"

    global service_file_lines_list_block
    logging.debug(
        f"{ip_node}: - Got the dataframe\n{dataframe.to_markdown()}"
    )

    unique_vpls_ids = dataframe['VPLS ID'].unique().astype(float)
    unique_vpls_ids = unique_vpls_ids.astype(int)

    filtered_lines_starting_with_route_distinguisher = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
                                                                                       start_word="route-distinguisher ")

    logging.info(
        f"{ip_node}: - Got the list of filtered_lines_starting_with_route_distinguisher\n" +
        f"{'\n'.join(filtered_lines_starting_with_route_distinguisher)}"
    )

    i = 0
    while i < unique_vpls_ids.size:
        selected_vpls_id = unique_vpls_ids[i]
        temp_df = dataframe.loc[dataframe['VPLS ID'] == selected_vpls_id]
        logging.info(
            f"{ip_node}: - Got the temp dataframe for vpls id {selected_vpls_id}.\n{temp_df.to_markdown()}"
        )
        route_distinguisher_var = temp_df.iloc[0, temp_df.columns.get_loc("BGP")]
        logging.debug(
            f"{ip_node}: - Got the route_distinguisher_var for vpls id {selected_vpls_id}.\n{route_distinguisher_var}"
        )

        route_distinguisher_var_found = False

        j = 0
        while j < len(filtered_lines_starting_with_route_distinguisher):
            if filtered_lines_starting_with_route_distinguisher[j].strip() == route_distinguisher_var:
                route_distinguisher_var_found = True
                break
            j += 1

        if route_distinguisher_var_found:
            if reason not in result_dictionary:
                result_dictionary[reason] = []
                result_dictionary[reason].extend(temp_df["S.No."].astype(float).astype(int).to_list())
            else:
                result_dictionary[reason].extend(temp_df["S.No."].astype(float).astype(int).to_list())
        i += 1

    logging.info(
        f"{ip_node}: - Returning the result dictionary of {__name__} method execution " +
        f"\n{'\n'.join(
            [f'{key} : {
                ', '.join(str(value) for value in values)
            }' for key, values in result_dictionary.items()]
        )}"
    )


def add_action_checks(ip_node: str, dataframe: pd.DataFrame) -> dict:
    """Performs the checks for \'ADD\' action filtered dataframe.

    Args:
        ip_node (str): ip node for which the checks are being performed
        dataframe (pd.DataFrame): \'ADD\' action filtered dataframe

    Returns
        dict: dictionary containing reason for error and list for serial numbers of rows for which the error is triggered.
    """

    logging.debug(
        f"{ip_node}: - inside {__name__}"
    )
    add_action_result_dictionary = {}

    reason = "Action:Add VPLS ID Clash found"
    reason2 = "VPLS Name Clash found"

    global vpls_section_filter_lines_list
    global service_file_lines_list_block

    logging.debug(
        f"{ip_node}: - Got the dataframe\n{dataframe.to_markdown()}"
    )

    unique_vpls_ids = dataframe['VPLS ID'].unique().astype(float)
    unique_vpls_ids = unique_vpls_ids.astype(int)

    logging.info(
        f"{ip_node}: - Got the list of unique_vpls_ids for \'ADD\' action filtered dataframe.\n{'\n'.join(unique_vpls_ids.astype(str))}"
    )

    filtered_lines_starting_with_route_distinguisher = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
                                                                                       start_word="route-distinguisher ")

    logging.info(
        f"{ip_node}: - Got the list of filtered_lines_starting_with_route_distinguisher\n" +
        f"{'\n'.join(filtered_lines_starting_with_route_distinguisher)}"
    )

    i = 0
    while i < unique_vpls_ids.size:
        selected_vpls_id = unique_vpls_ids[i]
        temp_df = dataframe.loc[dataframe['VPLS ID'] == selected_vpls_id]
        logging.info(
            f"{ip_node}: - Got the temp dataframe for vpls id {selected_vpls_id}.\n{temp_df.to_markdown()}"
        )

        selected_vpls_name = temp_df.iloc[0, temp_df.columns.get_loc("VPLS Name")]
        logging.debug(
            f"{ip_node}: - Got the selected_vpls_name for vpls id {selected_vpls_id}.\n{selected_vpls_name}"
        )

        vpls_found = False
        print(f"{ip_node}: - {len(vpls_section_filter_lines_list) = }")
        logging.info(
            f"{ip_node}: - checking for vpls {selected_vpls_id} in {'\n'.join(vpls_section_filter_lines_list)}"
        )
        j = 0
        while j < len(vpls_section_filter_lines_list):
            logging.info(f"{ip_node}: - checking for vpls {selected_vpls_id} in {vpls_section_filter_lines_list[j]}")
            if vpls_section_filter_lines_list[j].strip().startswith(f"vpls {selected_vpls_id} "):
                logging.debug(f"{ip_node}: - vpls {selected_vpls_id} found in {vpls_section_filter_lines_list[j]}")
                vpls_found = True
                break
            j += 1

        if vpls_found:
            logging.info(
                f"{ip_node}: - adding S.No. for {selected_vpls_id} for \'ADD\' action for ip node \'{ip_node}\'"
                f"\n{temp_df["S.No."].astype(float).astype(int)}"
            )
            if reason not in add_action_result_dictionary:
                add_action_result_dictionary[reason] = []
                add_action_result_dictionary[reason].extend(temp_df["S.No."].astype(float).astype(int))
            else:
                add_action_result_dictionary[reason].extend(temp_df["S.No."].astype(float).astype(int))

        vpls_name_found = False
        j = 0
        while j < len(service_file_lines_list_block):
            if service_file_lines_list_block[j].strip().__contains__(f"\"{selected_vpls_name}\""):
                vpls_name_found = True
                break
            j += 1

        if vpls_name_found:
            if reason2 not in add_action_result_dictionary:
                add_action_result_dictionary[reason] = []
                add_action_result_dictionary[reason].extend(temp_df["S.No."].astype(float).astype(int))
            else:
                add_action_result_dictionary[reason].extend(temp_df["S.No."].astype(float).astype(int))

        i += 1

    logging.info(
        f"{ip_node}: - Returning the result dictionary of {__name__} method execution " +
        f"\n{'\n'.join(
            [f'{key} : {
                ', '.join(str(value) for value in values)
            }' for key, values in add_action_result_dictionary.items()]
        )}"
    )

    return add_action_result_dictionary


def modify_action_checks(ip_node: str, dataframe: pd.DataFrame) -> dict:
    """Performs the checks for \'MODIFY\' action filtered dataframe.

    Args:
        ip_node (str): ip node for which the checks are being performed.
        dataframe (pd.DataFrame): \'MODIFY\' action filtered dataframe

    Returns:
        dict: dictionary containing reason for error and list for serial numbers of rows for which the error is triggered.
    """

    logging.info(f"{ip_node}: - Starting {__name__}")

    reason = "Action:Modify VPLS ID not found"

    global service_file_lines_list_block

    modify_action_result_dictionary = {}

    unique_vpls_ids = dataframe["VPLS ID"].unique().astype(float).astype(int)

    i = 0
    while i < unique_vpls_ids.size:
        selected_vpls_id = unique_vpls_ids[i]
        temp_df = dataframe.loc[dataframe['VPLS ID'] == selected_vpls_id]
        # selected_vpls_name = temp_df.iloc[0, temp_df.columns.get_loc("VPLS Name")]

        vpls_found = False
        j = 0
        while j < len(vpls_section_filter_lines_list):
            if vpls_section_filter_lines_list[j].strip().startswith(f"vpls {selected_vpls_id} "):
                vpls_found = True
                break
            j += 1

        if not vpls_found:
            if reason not in modify_action_result_dictionary:
                modify_action_result_dictionary[reason] = []
                modify_action_result_dictionary[reason].extend(temp_df["S.No."].astype(float).astype(int).to_list())
            else:
                modify_action_result_dictionary[reason].extend(temp_df["S.No."].astype(float).astype(int).to_list())

        i += 1

    logging.info(
        f"{ip_node}: - Returning the result dictionary of {__name__} method execution "
        f"\n{'\n'.join(
            [f'{key} : {
                ', '.join(str(value) for value in values)
            }' for key, values in modify_action_result_dictionary.items()]
        )}"
    )

    return modify_action_result_dictionary


def vsd_controller_mapping_yes_checks(ip_node: str, dataframe: pd.DataFrame) -> dict:
    """Performs the checks for \'VSD Controller Mapping\' \'Yes\' filtered dataframe.

    Args:
        ip_node (str): ip node for which the checks are being performed
        dataframe (pd.DataFrame): \'VSD Controller Mapping\' \'YES\' filtered dataframe

    Returns:
        dict: dictionary containing reason for error and list for serial numbers of rows for which the error is triggered.
    """

    logging.info(f"{ip_node}:- Starting {__name__}")

    vsd_controller_mapping_yes_checks_result_dictionary = {}
    global service_file_lines_list_block

    filtered_lines_starting_with_domain = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
                                                                          start_word="domain ")

    logging.info(
        f"{ip_node}:- filtered lines starting with domain \n"
        f"{'\n'.join(filtered_lines_starting_with_domain)}"
    )

    filtered_lines_starting_with_vsd_domain = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
                                                                              start_word="vsd-domain ")

    logging.info(
        f"{ip_node}:- filtered lines starting with vsd-domain \n"
        f"{'\n'.join(filtered_lines_starting_with_vsd_domain)}"
    )

    reason = "VSD Domain Name configuration not found"
    reason2 = "VSD Domain Name binding already found"

    unique_domain_names = dataframe["Vsd-domain Name"].unique()

    i = 0
    while i < unique_domain_names.size:
        selected_domain_name = unique_domain_names[i]
        temp_df = dataframe.loc[dataframe["Vsd-domain Name"].str.strip().str.endswith(selected_domain_name)]

        if selected_domain_name != "TempNA":
            domain_name_found = False

            j = 0
            while j < len(filtered_lines_starting_with_domain):
                if filtered_lines_starting_with_domain[j].startswith(f"domain \"{selected_domain_name}\" "):
                    domain_name_found = True
                    break
                j += 1

            if not domain_name_found:
                if reason not in vsd_controller_mapping_yes_checks_result_dictionary:
                    vsd_controller_mapping_yes_checks_result_dictionary[reason] = []
                    vsd_controller_mapping_yes_checks_result_dictionary[reason].extend(temp_df["S.No."].astype(float).astype(int).to_list())
                else:
                    vsd_controller_mapping_yes_checks_result_dictionary[reason].extend(temp_df["S.No."].astype(float).astype(int).to_list())

            vsd_domain_name_found = False

            j = 0
            while j < len(filtered_lines_starting_with_vsd_domain):
                if filtered_lines_starting_with_vsd_domain[j].startswith(f"vsd-domain \"{selected_domain_name}\" "):
                    vsd_domain_name_found = True
                    break
                j += 1

            if vsd_domain_name_found:
                if reason2 not in vsd_controller_mapping_yes_checks_result_dictionary:
                    vsd_controller_mapping_yes_checks_result_dictionary[reason2] = []
                    vsd_controller_mapping_yes_checks_result_dictionary[reason2].extend(temp_df["S.No."].astype(float).astype(int).to_list())
                else:
                    vsd_controller_mapping_yes_checks_result_dictionary[reason2].extend(temp_df["S.No."].astype(float).astype(int).to_list())
        i += 1

    global global_running_config_backup_file_lines

    reason2 = "VSI Export policy is not configured"
    reason3 = "VSI Import policy is not configured"

    vsi_export_and_vsi_import_filtered_df = dataframe.loc[(~dataframe["VSI-Export"].str.strip().str.endswith("TempNA")) &
                                                          (~dataframe["VSI-Import"].str.strip().str.endswith("TempNA"))]

    logging.info(
        f"{ip_node}:- Got the vsi_export_and_vsi_import_filtered_df\n{vsi_export_and_vsi_import_filtered_df.to_markdown()}\n"
    )

    if vsi_export_and_vsi_import_filtered_df.shape[0] > 0:

        filtered_lines_for_echo_policy = flh().file_lines_chunk_divisor(file_lines_list=global_running_config_backup_file_lines,
                                                                        start_string="echo \"Policy Configuration\"",
                                                                        end_string_pattern=r"^echo\s*\"[\w,\s]+\"\s*")

        logging.info(
            f"{ip_node}: - filtered lines for echo policy \n"
            f"{'\n'.join(filtered_lines_for_echo_policy)}"
        )

        unique_vsi_export_names = vsi_export_and_vsi_import_filtered_df["VSI-Export"].unique()
        unique_vsi_export_names = np.delete(unique_vsi_export_names, np.where(unique_vsi_export_names == "TempNA"))

        unique_vsi_import_names = vsi_export_and_vsi_import_filtered_df["VSI-Import"].unique()
        unique_vsi_import_names = np.delete(unique_vsi_import_names, np.where(unique_vsi_import_names == "TempNA"))

        i = 0
        while i < unique_vsi_export_names.size:
            temp_df = vsi_export_and_vsi_import_filtered_df.loc[
                vsi_export_and_vsi_import_filtered_df["VSI-Export"].str.strip().str.endswith(unique_vsi_export_names[i])
            ]

            vsi_export_name_found = False

            j = 0
            while j < len(filtered_lines_for_echo_policy):
                line = filtered_lines_for_echo_policy[j]
                if line.__contains__(unique_vsi_export_names[i]):
                    vsi_export_name_found = True
                    break
                j += 1

            if not vsi_export_name_found:
                if reason2 not in vsd_controller_mapping_yes_checks_result_dictionary:
                    vsd_controller_mapping_yes_checks_result_dictionary[reason2] = []
                    vsd_controller_mapping_yes_checks_result_dictionary[reason2].extend(temp_df["S.No."].astype(float).astype(int).to_list())
                else:
                    vsd_controller_mapping_yes_checks_result_dictionary[reason2].extend(temp_df["S.No."].astype(float).astype(int).to_list())

            i += 1

        i = 0
        while i < unique_vsi_import_names.size:
            temp_df = vsi_export_and_vsi_import_filtered_df.loc[
                vsi_export_and_vsi_import_filtered_df["VSI-Import"].str.strip().str.endswith(unique_vsi_import_names[i])
            ]

            vsi_import_name_found = False

            j = 0
            while j < len(filtered_lines_for_echo_policy):
                line = filtered_lines_for_echo_policy[j]
                if line.__contains__(unique_vsi_import_names[i]):
                    vsi_import_name_found = True
                    break
                j += 1

            if not vsi_import_name_found:
                if reason3 not in vsd_controller_mapping_yes_checks_result_dictionary:
                    vsd_controller_mapping_yes_checks_result_dictionary[reason3] = []
                    vsd_controller_mapping_yes_checks_result_dictionary[reason3].extend(temp_df["S.No."].astype(float).astype(int).to_list())
                else:
                    vsd_controller_mapping_yes_checks_result_dictionary[reason3].extend(temp_df["S.No."].astype(float).astype(int).to_list())
            i += 1

    logging.info(
        f"{ip_node}: - Returning the result dictionary of {__name__} method execution " +
        f"\n{'\n'.join([f'{key} : {', '.join(str(value) for value in values)}' for key, values in vsd_controller_mapping_yes_checks_result_dictionary.items()])}"
    )

    return vsd_controller_mapping_yes_checks_result_dictionary


def vni_checks(ip_node: str, dataframe: pd.DataFrame) -> dict:
    """Perform VNI checks on the given IP node and dataframe and return the results as a dictionary.
        :param ip_node: IP node for which the checks are being performed
        :param dataframe: filtered dataframe with non-blank VNI column
        :return (dict): dictionary containing reason for error and list for serial numbers of rows for which the error is triggered
    """

    logging.info(f"{ip_node}: - Starting {__name__}")

    reason = "VNI ID Clash found"
    result_dictionary_with_vni_clashes = {}

    logging.debug(
        f"{ip_node}: - Got the dataframe\n{dataframe.to_markdown()}"
    )

    global service_file_lines_list_block

    filtered_lines_starting_with_vxlan_instance = flh().file_lines_starter_filter(file_lines_list=service_file_lines_list_block,
                                                                                  start_word="vxlan instance ")

    logging.info(
        f"{ip_node}: - Got the filtered_lines_starting_with_vxlan_instance\n" +
        f"{'\n'.join(filtered_lines_starting_with_vxlan_instance)}"
    )

    unique_vnis = dataframe["VNI ID"].unique().astype(float).astype(int)

    i = 0
    while i < unique_vnis.size:
        selected_vni = unique_vnis[i]
        temp_df = dataframe.loc[dataframe['VNI ID'] == selected_vni]

        vni_found = False

        j = 0
        while j < len(filtered_lines_starting_with_vxlan_instance):
            line = filtered_lines_starting_with_vxlan_instance[j]
            if line.__contains__(str(selected_vni)):
                vni_found = True
                break
            j += 1

        if vni_found:
            if reason not in result_dictionary_with_vni_clashes:
                result_dictionary_with_vni_clashes[reason] = []
                result_dictionary_with_vni_clashes[reason].extend(temp_df["S.No."].astype(float).astype(int).to_list())
            else:
                result_dictionary_with_vni_clashes[reason].extend(temp_df["S.No."].astype(float).astype(int).to_list())
        i += 1

    logging.info(
        f"{ip_node}: - Returning the result dictionary of {__name__} method execution " +
        f"\n{'\n'.join([f'{key} : {', '.join(str(value) for value in values)}' for key, values in result_dictionary_with_vni_clashes.items()])}"
    )

    return result_dictionary_with_vni_clashes


def main_func(dataframe: pd.DataFrame, ip_node: str, running_config_backup_file_lines: list) -> dict:
    """
        Performs the Node Checks for VPLS 2

        Arguments : (dataframe, ip_node, running_config_backup_file_lines)
            dataframe ===> pandas.DataFrame
                description ======> contains the dataframe(tabular data) for the VPLS-2 Section of given ip_node for running_config checks

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

    # from __init__ import nokia_config_check_start
    # nokia_config_check_start()

    # print(f"inside vpls-2 node checks:\n{'\n'.join(sys.path)}")

    # global log_file;
    # log_file = rf"C:/Ericsson_Application_Logs/CLI_Automation_Logs/Running_Config_Checks(Node_Checks).log"
    #
    # logging.basicConfig(filename=log_file,
    #                     filemode='a',
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt="%d-%b-%Y %I:%M:%S %p",
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)
    global result_dictionary
    result_dictionary = {}

    dataframe = dataframe.where(~dataframe.isna(), "TempNA")
    logging.debug(f"Got the dataframe after getting all the null values replaced with \'TempNA\' ==> {dataframe.to_markdown()}")

    # from file_lines_handler import File_lines_handler as flh
    global vpls_section_filter_lines_list
    vpls_section_filter_lines_list = flh().file_lines_starter_filter(file_lines_list=running_config_backup_file_lines,
                                                                     start_word="vpls")

    logging.debug(
        f"{ip_node}: - Got the filter of all the lines starting with \'vpls\'\n{'\n'.join(vpls_section_filter_lines_list)}"
    )

    global global_running_config_backup_file_lines
    global_running_config_backup_file_lines = running_config_backup_file_lines

    service_file_lines_list_block_thread = CustomThread(target=flh().file_lines_chunk_divisor,
                                                        args=(running_config_backup_file_lines,
                                                              'echo \"Service Configuration\"',
                                                              r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration\"$'))

    service_file_lines_list_block_thread.start()
    logging.debug(
        f"{ip_node}: - Created the thread for the filter of lines \'Service Configuration\'"
    )

    port_details_file_lines_list_block_thread = CustomThread(target=flh().file_lines_chunk_divisor,
                                                             args=(running_config_backup_file_lines,
                                                                   'echo \"Port Configuration\"',
                                                                   r'^echo\s([a-z,A-Z,\s,\"]\w+)\sConfiguration"$'))

    port_details_file_lines_list_block_thread.start()

    logging.debug(
        f"{ip_node}: - Creating a thread for the filter of lines \'Port Configuration\'"
    )

    global service_file_lines_list_block
    service_file_lines_list_block = service_file_lines_list_block_thread.join()

    if isinstance(service_file_lines_list_block, list):
        logging.debug(
            f"{ip_node}: - Got the block of lines from \'echo \"Service Configuration\"\' block\n{'\n'.join(service_file_lines_list_block)}"
        )

    global port_details_file_lines_list
    port_details_file_lines_list = port_details_file_lines_list_block_thread.join()

    if isinstance(port_details_file_lines_list, list):
        logging.debug(
            f"{ip_node}: - Got the block of lines from \'echo \"Port Configuration\"\' block\n{'\n'.join(port_details_file_lines_list)}"
        )

    dataframe = dataframe.where(~dataframe.isna(), "TempNA")
    add_action_dataframe = dataframe.loc[dataframe['Action'].str.upper().str.contains("ADD")]

    logging.info(
        f"{ip_node}: - Created the filtered dataframe for Action \'ADD\' for VPLS-2 Section\n{add_action_dataframe.to_markdown()}"
    )

    modify_action_dataframe = dataframe.loc[dataframe['Action'].str.upper().str.contains("MODIFY")]

    logging.info(
        f"{ip_node}: - Created the filtered dataframe for Action \'MODIFY\' for VPLS-2 Section\n{modify_action_dataframe.to_markdown()}"
    )

    try:
        if add_action_dataframe.shape[0] > 0:
            add_action_result_dictionary_from_main_func = add_action_checks(ip_node=ip_node,
                                                                            dataframe=add_action_dataframe)

            if isinstance(add_action_result_dictionary_from_main_func, dict):
                if len(add_action_result_dictionary_from_main_func) > 0:
                    result_dictionary.update(add_action_result_dictionary_from_main_func)

            common_checks_for_sequence_add(ip_node=ip_node,
                                           dataframe=add_action_dataframe)

        if modify_action_dataframe.shape[0] > 0:
            modify_action_result_dictionary_from_main_func = modify_action_checks(ip_node=ip_node,
                                                                                  dataframe=modify_action_dataframe)
            if isinstance(modify_action_result_dictionary_from_main_func, dict):
                if len(modify_action_result_dictionary_from_main_func) > 0:
                    result_dictionary.update(modify_action_result_dictionary_from_main_func)

            modify_action_sequence_add_filtered_df = modify_action_dataframe.loc[modify_action_dataframe["Sequence"].str.upper().str.endswith("ADD")]

            if modify_action_sequence_add_filtered_df.shape[0] > 0:
                logging.info(
                    f"{ip_node}: - Got the filtered df for modify_action_sequence_add_filtered_df :\n{modify_action_sequence_add_filtered_df.to_markdown()}"
                )

                common_checks_for_sequence_add(ip_node= ip_node,
                                               dataframe=modify_action_sequence_add_filtered_df)

        vsd_controller_mapping_yes_filtered_df = dataframe.loc[dataframe["VSD Controller Mapping"].str.upper().str.strip().str.endswith("YES")]

        logging.info(
            f"{ip_node}: - Got the filtered df for vsd_controller_mapping_yes_filtered_df :\n{vsd_controller_mapping_yes_filtered_df.to_markdown()}"
        )

        if vsd_controller_mapping_yes_filtered_df.shape[0] > 0:
            vsd_controller_mapping_yes_result_dictionary_from_main_func = vsd_controller_mapping_yes_checks(ip_node=ip_node,
                                                                                                            dataframe=vsd_controller_mapping_yes_filtered_df)

            if isinstance(vsd_controller_mapping_yes_result_dictionary_from_main_func, dict):
                if len(vsd_controller_mapping_yes_result_dictionary_from_main_func) > 0:
                    result_dictionary.update(vsd_controller_mapping_yes_result_dictionary_from_main_func)

        filtered_df_with_non_blank_vni_field = dataframe.loc[(dataframe["VNI ID"].str.strip() != "TempNA") & (dataframe["VXLAN Instance"].str.strip() != "TempNA")]

        logging.info(
            f"{ip_node}: - Got the filtered df for filtered_df_with_non_blank_vni_field :\n{filtered_df_with_non_blank_vni_field.to_markdown()}"
        )

        if filtered_df_with_non_blank_vni_field.shape[0] > 0:
            vni_result_dictionary_from_main_func = vni_checks(ip_node=ip_node,
                                                              dataframe=filtered_df_with_non_blank_vni_field)

            if isinstance(vni_result_dictionary_from_main_func, dict):
                if len(vni_result_dictionary_from_main_func) > 0:
                    result_dictionary.update(vni_result_dictionary_from_main_func)

    except ValueError as ve:
        # exception_raised = True
        logging.error(f"{traceback.format_exc()}\nException Occurred!==>\n Title ==> {type(ve)}\n Message ==> {str(ve)}")
        title = str(type(ve))
        message = str(ve)
        messagebox.showerror(title=title,
                             message=message)
        result_dictionary = {}

    except Exception as e:
        # exception_raised = True
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

# main_func(dataframe= pd.read_excel(io= r"C:\Users\emaienj\Downloads\VPLS_CLI_Design_Documents\VPLS_CLI_Design_Documents\Nokia_Input.xlsx",
#                                    sheet_name="172.31.72.93"),
#           ip_node="172.31.72.93",
#           running_config_backup_file_lines= open(r"C:\Users\emaienj\Downloads\VPLS_CLI_Design_Documents\VPLS_CLI_Design_Documents\Switch_1 traditional_backup.txt","r").readlines())
