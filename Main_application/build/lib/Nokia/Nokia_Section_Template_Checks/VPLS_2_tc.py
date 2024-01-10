import logging
import os
from pathlib import Path

import numpy as np
import pandas as pd


def main_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """
        Performs the Template checks for the VPLS 2 Section (VPLS with VSD/VNI)
        
        Arguments : (dataframe, ip_node)
            dataframe => pd.DataFrame,  
            description ====> contains the section dataframe in this case for VPLS 2, obtained from Input Design workbook.
            
            ip_node   => str,  
            description ====> contains the name of the 'IP Node' worksheet, being checked.
        
        returns : result_dictionary 
            result_dictionary => dict, 
            description ====> contains the dictionary with the list of all errors found in Template Checks with reason as keys.
    """
    log_file_path = "C:/Ericsson_Application_Logs/CLI_Automation_Logs/"
    Path(log_file_path).mkdir(parents=True, exist_ok=True)

    log_file = os.path.join(log_file_path, "Template_checks.log")

    logging.basicConfig(filename=log_file,
                        filemode="a",
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt='%d-%b-%Y %I:%M:%S %p',
                        encoding="UTF-8",
                        level=logging.DEBUG)

    # logging.debug(
    #     f"Adding the system path for the Nokia main folder so that the NameError is not encountered in Nokia.Nokia_Section_Template_Checks.VPLS_1.same_vpls_id_found_error_message in VPLS-2 Section Checks")

    # path_for_nokia_main_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # sys.path.append(path_for_nokia_main_folder)
    # logging.debug(f"Path entered from VPLS_2 Section_Template_Checks module for ====> \n{path_for_nokia_main_folder}\n")

    logging.debug(f"Created the empty dictionary for returning as result for IP Node: -{ip_node} for VPLS 2 section")

    result_dictionary = {}
    # df                          = dataframe.fillna("TempNA")
    df = dataframe.where(~dataframe.isna(), "TempNA")
    logging.debug(f"Created a copy of dataframe passed for node_ip({ip_node}) for VPLS-2:-\n{df.to_markdown()}\n\n")

    df_add = df[df['Action'].str.strip().str.upper() == 'A:ADD']
    logging.debug(f"Created the filtered copy of the Dataframe for Action 'A:Add' for node_ip({ip_node}) for VPLS-2:-\n{df_add.to_markdown()}\n\n")

    df_delete_modify = df[df['Action'].str.strip().str.upper().isin(['A:DELETE', 'A:MODIFY'])]
    logging.debug(f"Created the filtered copy of the Dataframe for Action 'A:Modify/A:Delete' for node_ip({ip_node}) for VPLS-2:-\n{df_delete_modify.to_markdown()}\n\n")

    logging.debug(f"Going to check the VPLS ID for VPLS-2 of node_ip({ip_node})")

    if len(df) > 0:
        reason = ''

        i = 0
        while i < len(df):
            if df.iloc[i, df.columns.get_loc('VPLS ID')] == "TempNA":
                reason = "Blank VPLS ID found"

                if reason not in result_dictionary.keys():
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(df.iloc[i, df.columns.get_loc('S.No.')])

                else:
                    result_dictionary[reason].append(df.iloc[i, df.columns.get_loc('S.No.')])
            i += 1
        logging.debug(f"Entered the entries for 'Blank VPLS ID' for node ip {ip_node} for VPLS 2 ==>\n{result_dictionary}\n\n")

        reason = 'Space found in VPLS Name'
        temp_df = df[df['VPLS Name'].str.strip().str.contains(' ')]

        logging.debug(f"Finding the {reason} in VPLS - 2 for node_ip {ip_node} ===>\n{temp_df.to_markdown()}")

        if len(temp_df) > 0:
            result_dictionary[reason] = list(temp_df['S.No.'])

        reason = 'Space found in Vsd-domain Name'
        temp_df = df[df['Vsd-domain Name'].str.strip().str.contains(' ')]

        logging.debug(f"Finding the {reason} in VPLS - 2 for node_ip {ip_node} ===>\n{temp_df.to_markdown()}")

        if len(temp_df) > 0:
            result_dictionary[reason] = list(temp_df['S.No.'])

    if len(df_add) > 0:
        i = 0
        reason = 'Blank VPLS Name found'
        while i < len(df_add):
            if df_add.iloc[i, df_add.columns.get_loc('VPLS Name')] == 'TempNA':
                if reason not in result_dictionary.keys():
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(df_add.iloc[i, df.columns.get_loc('S.No.')])

                else:
                    result_dictionary[reason].append(df_add.iloc[i, df.columns.get_loc('S.No.')])
            i += 1
        logging.debug(f"Entered the entries for 'Blank VPLS Name' for node ip {ip_node} for VPLS 2 ==>\n{result_dictionary}\n\n")

        temp_df = df_add[df_add.duplicated(subset=['VPLS ID'], keep=False)]
        if len(temp_df) > 0:
            logging.debug(f"Found duplicate VPLS IDs for VPLS-2 for node_ip ({ip_node})==>\n{temp_df.to_markdown()}\n\n")
            reason = 'Same VPLS ID found ==> for VPLS IDs(S.Nos.)'
            from Nokia.Nokia_Section_Template_Checks.VPLS_1_tc import same_vpls_id_found_error_message_generator
            result_dictionary[reason] = same_vpls_id_found_error_message_generator(dataframe=temp_df, common_vpls_ids=temp_df['VPLS ID'].unique().astype(int))
            del temp_df

    # reason = 'VPLS ID of Action \'Add\' present in Action \'Modify/Delete\''
    # reason = 'Same VPLS ID found'

    reason = 'Same VPLS ID found ==> for VPLS IDs(S.Nos.)'
    if len(df_add) > 0:
        df_add_unique_VPLS_IDs = df_add['VPLS ID'].unique()

        if "TempNA" in df_add_unique_VPLS_IDs:
            df_add_unique_VPLS_IDs = np.delete(df_add_unique_VPLS_IDs, np.argwhere(df_add_unique_VPLS_IDs == 'TempNA'))
            df_add_unique_VPLS_IDs = df_add_unique_VPLS_IDs.astype(int)

        logging.debug(f"df_add_unique_VPLS_IDs for node_ip({ip_node}) for VPLS-2 ==>\n{df_add_unique_VPLS_IDs}\n\n")

    if len(df_delete_modify) > 0:
        df_delete_modify_VPLS_IDs = df_delete_modify['VPLS ID'].unique()

        if "TempNA" in df_delete_modify_VPLS_IDs:
            df_delete_modify_VPLS_IDs = np.delete(df_delete_modify_VPLS_IDs, np.argwhere(df_delete_modify_VPLS_IDs == "TempNA"))
            df_delete_modify_VPLS_IDs = df_delete_modify_VPLS_IDs.astype(int)

        logging.debug(f"df_delete_modify_VPLS_IDs for node_ip({ip_node}) for VPLS-2 ==>\n{df_delete_modify_VPLS_IDs}\n\n")

    logging.debug(f"Finding the set-intersection for the df_add and df_delete for node_ip ({ip_node}) for VPLS-2 {np.intersect1d(df_add_unique_VPLS_IDs, df_delete_modify_VPLS_IDs).astype(int)}")
    set_intersection_between_Add_and_Modify_Delete_dfs = np.intersect1d(df_add_unique_VPLS_IDs, df_delete_modify_VPLS_IDs).astype(int)

    if set_intersection_between_Add_and_Modify_Delete_dfs.size > 0:
        # reason = f"{reason} ==> for VPLS IDs : ({', '.join([str(int(elements)) for elements in set_intersection_between_Add_and_Modify_Delete_dfs])})"

        logging.debug(f"{df_add[df_add['VPLS ID'].isin(list(set_intersection_between_Add_and_Modify_Delete_dfs))]}")

        logging.debug(
            f"Got the filtered data from intersection between add and modify_delete dfs in VPLS-1 for node ip ('{ip_node}') ==> \n{df[df['VPLS ID'].isin(list(set_intersection_between_Add_and_Modify_Delete_dfs))].to_markdown()}\n")
        # result_dictionary[reason] = list((df[df['VPLS ID'].isin(list(set_intersection_between_Add_and_Modify_Delete_dfs))])['S.No.'])

        # Importing function from the VPLS_1 module for same_vpls_id_found_error_message_generator
        from Nokia.Nokia_Section_Template_Checks.VPLS_1_tc import same_vpls_id_found_error_message_generator
        result_dictionary[reason] = same_vpls_id_found_error_message_generator(dataframe=df, common_vpls_ids=set_intersection_between_Add_and_Modify_Delete_dfs)

        logging.debug(f"Entered the  entries for 'Common VPLS IDs in Add and Modify/Delete Actions' for node ip {ip_node} for VPLS-2 ==>\n{result_dictionary}\n\n")

    logging.debug(f"Checking whether there is any entry for the 'VSD Controller Mapping' empty or not for VPLS-2 of node ip {ip_node}\n\n")
    i = 0
    reason = 'Blank \'VSD Controller Mapping\' entry'
    while i < len(df):
        if df.iloc[i, df.columns.get_loc('VSD Controller Mapping')] == "TempNA":
            if reason not in result_dictionary.keys():
                result_dictionary[reason] = []
                result_dictionary[reason].append(df.iloc[i, df.columns.get_loc('S.No.')])
            else:
                result_dictionary[reason].append(df.iloc[i, df.columns.get_loc('S.No.')])
        i += 1

    if reason in result_dictionary.keys():
        logging.debug(f"Created entries for the 'Blank VSD Controller Mapping' in the result_dictionary for node ip '{ip_node}' for VPLS-2 ==>\n{result_dictionary}\n\n")

    logging.debug(f"Checking for the 'VSD Controller Mapping' specific checks in the dataframe for VPLS-2 for node ip {ip_node}\n\n")
    df_with_vsd_controller_yes = df[df['VSD Controller Mapping'].str.strip().str.upper() == 'YES']
    df_with_vsd_controller_no = df[df['VSD Controller Mapping'].str.strip().str.upper() == 'NO']

    if len(df_with_vsd_controller_yes) > 0:
        logging.debug(
            f"Checking for the entries of the \'Vsd-domain Name\', \'Vsd-domain Description\', and \'Vsd-domain Type\' for value of \'VSD-Controller Mapping\' equal to \'Yes\' for VPLS-2 for node ip \'{ip_node}\'")

        i = 0
        while i < len(df_with_vsd_controller_yes):
            if df_with_vsd_controller_yes.iloc[i, df_with_vsd_controller_yes.columns.get_loc('Vsd-domain Name')] == 'TempNA':
                reason1 = 'Blank \'Vsd-domain Name\' found'
                if reason1 not in result_dictionary.keys():
                    result_dictionary[reason1] = []
                    result_dictionary[reason1].append(df_with_vsd_controller_yes.iloc[i, df_with_vsd_controller_yes.columns.get_loc('S.No.')])
                else:
                    result_dictionary[reason1].append(df_with_vsd_controller_yes.iloc[i, df_with_vsd_controller_yes.columns.get_loc('S.No.')])

            if df_with_vsd_controller_yes.iloc[i, df_with_vsd_controller_yes.columns.get_loc('Vsd-domain Description')] == 'TempNA':
                reason2 = 'Blank \'Vsd-domain Description\' found'
                if reason2 not in result_dictionary.keys():
                    result_dictionary[reason2] = []
                    result_dictionary[reason2].append(df_with_vsd_controller_yes.iloc[i, df_with_vsd_controller_yes.columns.get_loc('S.No.')])
                else:
                    result_dictionary[reason2].append(df_with_vsd_controller_yes.iloc[i, df_with_vsd_controller_yes.columns.get_loc('S.No.')])

            if df_with_vsd_controller_yes.iloc[i, df_with_vsd_controller_yes.columns.get_loc('Vsd-domain Type')] == 'TempNA':
                reason3 = 'Blank \'Vsd-domain Type\' found'
                if not reason3 in result_dictionary.keys():
                    result_dictionary[reason3] = []
                    result_dictionary[reason3].append(df_with_vsd_controller_yes.iloc[i, df_with_vsd_controller_yes.columns.get_loc('S.No.')])
                else:
                    result_dictionary[reason3].append(df_with_vsd_controller_yes.iloc[i, df_with_vsd_controller_yes.columns.get_loc('S.No.')])
            i += 1

        logging.debug(f"Created entries for the 'VSD Controller Mapping' equal to \'Yes\' status in the result_dictionary for node ip '{ip_node}' for VPLS-2 ==>\n{result_dictionary}\n\n")

    if len(df_with_vsd_controller_no) > 0:
        logging.debug(
            f"Checking for the entries of the \'Vsd-domain Name\', \'Vsd-domain Description\', and \'Vsd-domain Type\' for value of \'VSD-Controller Mapping\' equal to \'No\' for VPLS-2 for node ip \'{ip_node}\'")

        i = 0
        while i < len(df_with_vsd_controller_no):
            if df_with_vsd_controller_no.iloc[i, df_with_vsd_controller_no.columns.get_loc('Vsd-domain Name')] != 'TempNA':
                reason1 = 'Non-Blank \'Vsd-domain Name\' found'
                if reason1 not in result_dictionary.keys():
                    result_dictionary[reason1] = []
                    result_dictionary[reason1].append(df_with_vsd_controller_no.iloc[i, df_with_vsd_controller_no.columns.get_loc('S.No.')])
                else:
                    result_dictionary[reason1].append(df_with_vsd_controller_no.iloc[i, df_with_vsd_controller_no.columns.get_loc('S.No.')])

            if df_with_vsd_controller_no.iloc[i, df_with_vsd_controller_no.columns.get_loc('Vsd-domain Description')] != 'TempNA':
                reason2 = 'Non-Blank \'Vsd-domain Description\' found'
                if reason2 not in result_dictionary.keys():
                    result_dictionary[reason2] = []
                    result_dictionary[reason2].append(df_with_vsd_controller_no.iloc[i, df_with_vsd_controller_no.columns.get_loc('S.No.')])
                else:
                    result_dictionary[reason2].append(df_with_vsd_controller_no.iloc[i, df_with_vsd_controller_no.columns.get_loc('S.No.')])

            if df_with_vsd_controller_no.iloc[i, df_with_vsd_controller_no.columns.get_loc('Vsd-domain Type')] != 'TempNA':
                reason3 = 'Non-Blank \'Vsd-domain Type\' found'
                if reason3 not in result_dictionary.keys():
                    result_dictionary[reason3] = []
                    result_dictionary[reason3].append(df_with_vsd_controller_no.iloc[i, df_with_vsd_controller_no.columns.get_loc('S.No.')])
                else:
                    result_dictionary[reason3].append(df_with_vsd_controller_no.iloc[i, df_with_vsd_controller_no.columns.get_loc('S.No.')])
            i += 1

        logging.debug(f"Created entries for the 'VSD Controller Mapping' equal to \'No\' status in the result_dictionary for node ip '{ip_node}' for VPLS-2 ==>\n{result_dictionary}\n\n")

    filtered_df_for_rt_export_for_string_length_greater_than_32 = df[df['RT-Export'].map(len) > 32]
    filtered_df_for_rt_import_for_string_length_greater_than_32 = df[df['RT-Import'].map(len) > 32]
    filtered_df_for_VSI_export_for_string_length_greater_than_32 = df[df['VSI-Export'].map(len) > 32]
    filtered_df_for_VSI_import_for_string_length_greater_than_32 = df[df['VSI-Import'].map(len) > 32]

    # Entry checking for RT-Export Character length
    if len(filtered_df_for_rt_export_for_string_length_greater_than_32) > 0:
        reason = 'RT-Export Field Entry Length Greater than 32 characters'
        result_dictionary[reason] = filtered_df_for_rt_export_for_string_length_greater_than_32['S.No.'].tolist()
        logging.debug(f"Created entries for the '{reason}' in the result_dictionary for node ip '{ip_node}' for VPLS-2 ==>\n{result_dictionary}\n\n")

    # Entry checking for RT-Import Character length
    if len(filtered_df_for_rt_import_for_string_length_greater_than_32) > 0:
        reason = 'RT-Import Field Entry Length Greater than 32 characters'
        result_dictionary[reason] = filtered_df_for_rt_import_for_string_length_greater_than_32['S.No.'].tolist()
        logging.debug(f"Created entries for the '{reason}' in the result_dictionary for node ip '{ip_node}' for VPLS-2 ==>\n{result_dictionary}\n\n")

    # Entry checking for VSI-Export Character length
    if len(filtered_df_for_VSI_export_for_string_length_greater_than_32) > 0:
        reason = 'VSI-Export Field Entry Length Greater than 32 characters'
        result_dictionary[reason] = filtered_df_for_VSI_export_for_string_length_greater_than_32['S.No.'].tolist()
        logging.debug(f"Created entries for the '{reason}' in the result_dictionary for node ip '{ip_node}' for VPLS-2 ==>\n{result_dictionary}\n\n")

    # Entry checking for VSI-Import Character length
    if len(filtered_df_for_VSI_import_for_string_length_greater_than_32) > 0:
        reason = 'VSI-Import Field Entry Length Greater than 32 characters'
        result_dictionary[reason] = filtered_df_for_VSI_import_for_string_length_greater_than_32['S.No.'].tolist()
        logging.debug(f"Created entries for the '{reason}' in the result_dictionary for node ip '{ip_node}' for VPLS-2 ==>\n{result_dictionary}\n\n")

    logging.debug(f"The result_dictionary for node_ip({ip_node}) for VPLS-2 ==>\n {result_dictionary}\n\n")

    logging.shutdown()
    return result_dictionary
