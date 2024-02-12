import numpy as np
import pandas as pd
import logging
import os
import pickle
from pathlib import Path
import re


def same_vpls_id_found_error_message_generator(dataframe: pd.DataFrame, common_vpls_ids: np.array) -> list:
    """
        Generates list to be entered into the dictionary of result_dictionary in main_func for same vpls
        
        Arguments : (dataframe, common_vpls_ids)
            dataframe ===> pd.DataFrame
                description =====> Dataframe with all the duplicated data
            
            common_vpls_ids ===> np.array
                description =====> array containing the VPLS IDs for which duplicated data is present

        return result_list
            result_list ===> list
                description =====> formatted list in the format >> 'VPLS ID ('S.No.' group)'
    """
    result_list = []

    i = 0
    while i < common_vpls_ids.size:
        selected_vpls_id = common_vpls_ids[i]
        result_list.append(f"{selected_vpls_id} ({','.join(str(int(element)) for element in (dataframe[dataframe['VPLS ID'] == selected_vpls_id])['S.No.'])})")
        i += 1

    return result_list

def sdp_checks_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """Checks for the sdp enteries with sdp section dataframe.

    Args:
        dataframe (pd.DataFrame): dataframe containing data to be checked
        ip_node (str): ip_node

    Returns:
        result_dict_of_sdp_checks(dict): dictionary containing corresponding reasons with list of all the serial numbers pertaining to that error reason
    """
    result_dict_of_sdp_checks = {}
    reason = 'SDP details are missing'
    reason2 = 'We have found that \'New\' SDP {} inputs are missing in \'SDP\' Section'

    dataframe = dataframe.loc[(~dataframe['Sequence'].str.strip().str.startswith('TempNA')) & (~dataframe['Action'].str.strip().str.startswith('TempNA'))]
    logging.info(f"{ip_node}: -Got the dataframe after filling blanks with \'TempNA\'=>\n{dataframe.to_markdown()}")

    dataframe_with_mesh_sdp = dataframe.loc[(~dataframe["Mesh-sdp"].str.startswith("TempNA"))]
    logging.info(f"{ip_node}: - Got the dataframe after filtering rows with \'Mesh-sdp\' data present =>\n{dataframe_with_mesh_sdp.to_markdown()}")

    # Entering the values of dataframe where 'Mesh-sdp' column is non-empty and 'SDP(New/Exist)' is empty.
    result_dict_of_sdp_checks[reason] = [
                                            int(element) for element in (dataframe_with_mesh_sdp.loc[(dataframe_with_mesh_sdp['SDP(New/Exist)'].str.strip() == 'TempNA') &
                                                                                                     (dataframe_with_mesh_sdp['Sequence'].str.strip().str.startswith('ADD'))])['S.No.']
                                        ]
    logging.debug(f"{ip_node}: - Got the result dictionary as=>\n{'\n'.join([f'{key}: [ {', '.join([str(element) for element in value])} ]' for key, value in result_dict_of_sdp_checks.items()])}")

    add_sequence_dataframe = dataframe_with_mesh_sdp.loc[dataframe_with_mesh_sdp['Sequence'].str.strip().str.startswith('ADD')]
    logging.info(f"{ip_node}: - Got the filtered datframe from Mesh-sdp df for sequence action \'Add\'=>\n{add_sequence_dataframe.to_markdown()}")
    
    delete_sequence_dataframe = dataframe_with_mesh_sdp.loc[dataframe_with_mesh_sdp['Sequence'].str.strip().str.startswith('DELETE')]
    logging.info(f"{ip_node}: - Got the filtered datframe from Mesh-sdp df for sequence action \'Delete\'=>\n{delete_sequence_dataframe.to_markdown()}")
    
    sdp_existence_entry_given_as_new_df = add_sequence_dataframe.loc[add_sequence_dataframe['SDP(New/Exist)'].str.strip().str.upper() == 'NEW']
    logging.info(f"{ip_node}: - Got the data for the sdp_existence_entry_given_as_new_df as =>\n{sdp_existence_entry_given_as_new_df.to_markdown()}")
    
    sdp_existence_entry_given_as_exist_df = add_sequence_dataframe.loc[add_sequence_dataframe['SDP(New/Exist)'].str.strip().str.upper() == 'EXIST']
    logging.info(f"{ip_node}: - Got the data for the sdp_existence_entry_given_as_exist_df as =>\n{sdp_existence_entry_given_as_exist_df.to_markdown()}")

    username = os.popen(cmd= r'cmd.exe /C "echo %username%"').read().strip()
    pickle_file_path = f"C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\Vendor_pickles\\NOKIA.pickle"

    with open(pickle_file_path, 'rb') as f:
        nokia_pickle_dictionary = pickle.load(file=f,
                                              encoding='UTF-8')
        f.close()
    
    logging.info(f"{ip_node}: - Got the dictionary from the NOKIA.pickle as" +
        '\n'.join([f'{node} : {'\n'.join([f'{reason} : {serial_list}' for reason, serial_list in node_value.items()])}' for node, node_value in nokia_pickle_dictionary.items()]) +
    "}")

    del f
    nokia_pickle_dictionary = nokia_pickle_dictionary[ip_node]
    logging.info(f"{ip_node}: - Got the data for {ip_node}=>\n" +
                 '\n'.join([f'{section} : \n\t{df.to_markdown()}\n' for section, df in nokia_pickle_dictionary.items()]))

    error_title = "SDP Section Input missing"
    error_message = "We have found \'New\' sdp cases in vpls section. However, there corresponding inputs are missing in \'SDP\' Section."
    
    if sdp_existence_entry_given_as_new_df.shape[0] > 0:
        if 'SDP' in nokia_pickle_dictionary:
            compiled_pattern = re.compile(r'\d+')
            ip_node_sdp_dataframe = nokia_pickle_dictionary[ip_node]['SDP']
            unique_sdp_enteries = ip_node_sdp_dataframe['sdp'].dropna().unique().char.strip().astype(int)
            unique_mesh_sdp_enteries = sdp_existence_entry_given_as_new_df['Mesh-sdp'].dropna().unique()
            temp_list   = []
            temp_list_2 = []

            i = 0
            while i < unique_mesh_sdp_enteries.size:
                sdp_variable = int( ( re.findall(pattern=compiled_pattern, string=str(unique_mesh_sdp_enteries[i])) )[0].strip() )
                temp_df = sdp_existence_entry_given_as_new_df.loc[sdp_existence_entry_given_as_new_df['Mesh-sdp'] == unique_mesh_sdp_enteries[i]]
                if sdp_variable not in unique_sdp_enteries:
                    temp_list.append(int(sdp_variable))
                    j = 0
                    while j < temp_df.shape[0]:
                        temp_list_2.append(int(temp_df.iloc[j, temp_df.columns.get_loc('S.No.')]))
                        j += 1
                i += 1
            if (len(temp_list) > 0) and (len(temp_list_2) > 0):
                result_dict_of_sdp_checks[reason2.format(tuple(temp_list))] = temp_list_2
        else:
            result_dict_of_sdp_checks[error_title] = error_message
    
    reason3 = 'We have found that \'Exist\' SDP {} inputs are available in \'SDP\' Section'
    if sdp_existence_entry_given_as_exist_df.shape[0] > 0:
        if 'SDP' in nokia_pickle_dictionary:
            compiled_pattern = re.compile(pattern=r'\d+')
            unique_mesh_sdp_enteries = sdp_existence_entry_given_as_exist_df['Mesh-sdp'].dropna().unique()
            ip_node_sdp_dataframe = nokia_pickle_dictionary[ip_node]['SDP']
            unique_sdp_enteries = ip_node_sdp_dataframe['sdp'].dropna().unique().char.strip().astype(int)
            temp_list   = []
            temp_list_2 = []

            i = 0
            while i < unique_mesh_sdp_enteries.size:
                sdp_variable = int( (re.findall(pattern=compiled_pattern, string= str(unique_mesh_sdp_enteries[i]))[0]).strip() )
                temp_df = sdp_existence_entry_given_as_exist_df.loc[sdp_existence_entry_given_as_exist_df['Mesh-sdp'] == unique_mesh_sdp_enteries[i]]
                if sdp_variable in unique_sdp_enteries:
                    temp_list.append(sdp_variable)
                    j = 0
                    while j < temp_df.shape[0]:
                        temp_list_2.append(int(temp_df.iloc[j, temp_df.columns.get_loc('S.No.')]))
                        j += 1
                i += 1
            if len(temp_list) > 0:
                result_dict_of_sdp_checks[reason3.format(temp_list)] = temp_list_2
        
        logging.info(f"{ip_node}: - Returning the dictionary result_dict_of_sdp_checks=>\n{'\n'.join([f'{key} : {', '.join(value)}' for key, value in result_dict_of_sdp_checks.items()])}")
        return result_dict_of_sdp_checks


def main_func(dataframe: pd.DataFrame, ip_node: str) -> dict:
    """
        Performs the Template checks for the VPLS 1 Section (VPLS with Mesh-sdp/sap)
        
        Arguments : (dataframe, ip_node)
            dataframe => pd.DataFrame,  
               description ====> contains the section dataframe in this case for VPLS 1, obtained from Input Design workbook.
            
            ip_node   => str,  
               description ====> contains the name of the 'IP Node' worksheet, being checked.
        
        returns : result_dictionary 
            result_dictionary => dict, 
               description ====> {Reasons : [list of Serial Numbers containing the template error in the 'VPLS-1' Section]}
                                    contains the dictionary with the list of all errors found in Template Checks with reason as keys.
    """
    # log_file_path = "C:/Ericsson_Application_Logs/CLI_Automation_Logs/"
    # Path(log_file_path).mkdir(parents=True, exist_ok=True)
    #
    # log_file = os.path.join(log_file_path, "Template_checks.log")
    #
    # logging.basicConfig(filename=log_file,
    #                     filemode="a",
    #                     format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
    #                     datefmt='%d-%b-%Y %I:%M:%S %p',
    #                     encoding="UTF-8",
    #                     level=logging.DEBUG)
    # logging.debug(f"Created the empty dictionary for returning as result for IP Node: -{ip_node} for VPLS 1 section")

    result_dictionary = {}
    # df                          = dataframe.fillna("TempNA")
    df = dataframe.where(~dataframe.isna(), "TempNA")
    logging.debug(f"Created a copy of dataframe passed for node_ip({ip_node}) for VPLS-1:-\n{df.to_markdown()}\n\n")

    df_add = df[df['Action'].str.strip().str.upper() == 'A:ADD']
    logging.debug(f"Created the filtered copy of the Dataframe for Action 'A:Add' for node_ip({ip_node}) for VPLS-1:-\n{df_add.to_markdown()}\n\n")

    df_delete_modify = df[df['Action'].str.strip().str.upper().isin(['A:DELETE', 'A:MODIFY'])]
    logging.debug(f"Created the filtered copy of the Dataframe for Action 'A:Modify/A:Delete' for node_ip({ip_node}) for VPLS-1:-\n{df_delete_modify.to_markdown()}\n\n")

    logging.debug(f"Going to check the VPLS ID for VPLS-1 of node_ip({ip_node})")

    temp_df = df.loc[(df["Sequence"].str.startswith("TempNA"))]

    if len(temp_df) > 0:
        result_dictionary["Blank 'Sequence' Action found"] = list(temp_df["S.No."])

    if len(df) > 0:
        reason = ''

        # df_columns = list(df.columns)
        #
        # if 'MPBN Node Type ( Router/Switch )' in df_columns:
        #     reason = 'MPBN Node Type missing'
        #     if df.iloc[0, df.columns.get_loc('MPBN Node Type ( Router/Switch )')] == 'TempNA':
        #         result_dictionary[reason] = [int(df.iloc[0, df.columns.get_loc('S.No.')])]

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
        logging.debug(f"Entered the entries for 'Blank VPLS ID' for node ip {ip_node} for VPLS 1 ==>\n{result_dictionary}\n\n")

        reason = 'Blank Sequence entry found'
        temp_df = df[df['Sequence'] == 'TempNA']

        logging.debug(f"Finding the blank Sequence entry in VPLS -1 for node_ip {ip_node} ===>\n{temp_df.to_markdown()}")

        if len(temp_df) > 0:
            result_dictionary[reason] = list(temp_df['S.No.'])

        reason = 'Blank MPBN Node Type found'

        temp_df = df[df['MPBN Node Type ( Router/Switch )'] == 'TempNA']
        logging.debug(f"Finding the blank MPBN Node Type ( Router/Switch ) entry in VPLS -1 for node_ip {ip_node} ===>\n{temp_df.to_markdown()}")

        if len(temp_df) > 0:
            result_dictionary[reason] = list(temp_df['S.No.'])

        reason = 'Space found in VPLS Name'
        temp_df = df[df['VPLS Name'].str.strip().str.contains(' ')]
        logging.debug(f"Finding the {reason} in VPLS -1 for node_ip {ip_node} ===>\n{temp_df.to_markdown()}")
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
        logging.debug(f"Entered the entries for 'Blank VPLS Name' for node ip {ip_node} for VPLS 1 ==>\n{result_dictionary}\n\n")

        # temp_df = df_add[df_add.duplicated(subset=['VPLS ID'], keep=False)]
        # if len(temp_df) > 0:
        #     logging.debug(f"Found duplicate VPLS IDs for VPLS-1 for node_ip ({ip_node})==>\n{temp_df.to_markdown()}\n\n")
        #     reason = 'Same VPLS ID found ==> for VPLS IDs(S.No. group)'
        #     result_dictionary[reason] = same_vpls_id_found_error_message_generator(dataframe=temp_df, common_vpls_ids=temp_df['VPLS ID'].unique().astype(int))
        #     del temp_df

    # reason = 'VPLS ID of Action \'Add\' present in Action \'Modify/Delete\''
    reason = 'Same VPLS ID found ==> for VPLS IDs(S.Nos.)'

    if (len(df_delete_modify) > 0) and (len(df_add) > 0):
        df_add_unique_VPLS_IDs = df_add['VPLS ID'].unique()

        if "TempNA" in df_add_unique_VPLS_IDs:
            df_add_unique_VPLS_IDs = np.delete(df_add_unique_VPLS_IDs, np.argwhere(df_add_unique_VPLS_IDs == 'TempNA'))
            df_add_unique_VPLS_IDs = df_add_unique_VPLS_IDs.astype(int)

        logging.debug(f"df_add_unique_VPLS_IDs for node_ip({ip_node}) ==>\n{df_add_unique_VPLS_IDs}")

        df_delete_modify_VPLS_IDs = df_delete_modify['VPLS ID'].unique()

        if "TempNA" in df_delete_modify_VPLS_IDs:
            df_delete_modify_VPLS_IDs = np.delete(df_delete_modify_VPLS_IDs, np.argwhere(df_delete_modify_VPLS_IDs == "TempNA"))
            df_delete_modify_VPLS_IDs = df_delete_modify_VPLS_IDs.astype(int)

        logging.debug(f"df_delete_modify_VPLS_IDs for node_ip({ip_node}) ==>\n{df_delete_modify_VPLS_IDs}")

        logging.debug(f"Finding the set-intersection for the df_add and df_delete for node_ip ({ip_node}) for VPLS-1 {np.intersect1d(df_add_unique_VPLS_IDs, df_delete_modify_VPLS_IDs).astype(int)}")
        set_intersection_between_Add_and_Modify_Delete_dfs = np.intersect1d(df_add_unique_VPLS_IDs, df_delete_modify_VPLS_IDs).astype(int)

        if set_intersection_between_Add_and_Modify_Delete_dfs.size > 0:
            # reason = f"{reason} {', '.join([str(int(elements)) for elements in set_intersection_between_Add_and_Modify_Delete_dfs])}"

            # result_dictionary[reason] = list((df[df['VPLS ID'].isin(list(set_intersection_between_Add_and_Modify_Delete_dfs))])['S.No.'])
            result_dictionary[reason] = same_vpls_id_found_error_message_generator(dataframe=df, common_vpls_ids=set_intersection_between_Add_and_Modify_Delete_dfs)
            logging.debug(
                f"Got the filtered data from intersection between add and modify_delete dfs in VPLS-1 for node ip ('{ip_node}') ==> \n{df[df['VPLS ID'].isin(list(set_intersection_between_Add_and_Modify_Delete_dfs))].to_markdown()}\n")

            logging.debug(f"Entered the entries for 'Common VPLS IDs in Add and Modify/Delete Actions' for node ip {ip_node} for VPLS-1 ==>\n{result_dictionary}\n\n")

    # Results from sdp_checks_func being updated into the result_dictionary
    temp_dictionary = sdp_checks_func(dataframe= df,
                                      ip_node= ip_node)
    if (isinstance(temp_dictionary, dict)) and (len(temp_dictionary) > 0):
        result_dictionary.update(temp_dictionary)
    logging.debug(f"The result_dictionary for node_ip({ip_node}) for VPLS-1 ==>\n {result_dictionary}")

    logging.shutdown()
    return result_dictionary
