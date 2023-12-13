import numpy as np
import pandas as pd
import logging
import os
from pathlib import Path



def same_vpls_id_found_error_message_generator(dataframe:pd.DataFrame, common_vpls_ids:np.array)->list:
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
    while(i < common_vpls_ids.size):
        selected_vpls_id = common_vpls_ids[i]
        result_list.append(f"{selected_vpls_id} ({','.join(str(int(element)) for element in (dataframe[dataframe['VPLS ID'] == selected_vpls_id])['S.No.'])})")
        i+=1
    
    return result_list

def main_func(dataframe : pd.DataFrame, ip_node: str) -> dict:
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
    log_file_path = "C:/Ericsson_Application_Logs/CLI_Automation_Logs/"
    Path(log_file_path).mkdir(parents=True,exist_ok=True)

    log_file = os.path.join(log_file_path,"Template_checks.log")

    logging.basicConfig(filename=log_file,
                            filemode="a",
                            format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                            datefmt='%d-%b-%Y %I:%M:%S %p',
                            encoding= "UTF-8",
                            level=logging.DEBUG)
    logging.debug(f"Created the empty dictionary for returning as result for IP Node: -{ip_node} for VPLS 1 section")
    
    result_dictionary           = {}
    df                          = dataframe.fillna("TempNA")
    logging.debug(f"Created a copy of dataframe passed for node_ip({ip_node}) for VPLS-1:-\n{df.to_markdown()}\n\n")
    
    df_add                      = df[df['Action'].str.strip().str.upper() == 'A:ADD']
    logging.debug(f"Created the filtered copy of the Dataframe for Action 'A:Add' for node_ip({ip_node}) for VPLS-1:-\n{df_add.to_markdown()}\n\n")
    
    df_delete_modify            = df[df['Action'].str.strip().str.upper().isin(['A:DELETE','A:MODIFY'])]
    logging.debug(f"Created the filtered copy of the Dataframe for Action 'A:Modify/A:Delete' for node_ip({ip_node}) for VPLS-1:-\n{df_delete_modify.to_markdown()}\n\n")

    logging.debug(f"Going to check the VPLS ID for VPLS-1 of node_ip({ip_node})")
    
    if(len(df) > 0):
        reason = ''

        i = 0
        while(i < len(df)):
            if(df.iloc[i,df.columns.get_loc('VPLS ID')] == "TempNA"):
                reason = "Blank VPLS ID found"

                if(not reason in result_dictionary.keys()):
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(df.iloc[i,df.columns.get_loc('S.No.')])

                else:
                    result_dictionary[reason].append(df.iloc[i,df.columns.get_loc('S.No.')])
            i+=1
        logging.debug(f"Entered the enteries for 'Blank VPLS ID' for node ip {ip_node} for VPLS 1 ==>\n{result_dictionary}\n\n")
        
        reason = 'Blank Sequence entry found'
        temp_df = df[df['Sequence'] == 'TempNA']
        
        logging.debug(f"Finding the blank Sequence entry in VPLS -1 for node_ip {ip_node} ===>\n{temp_df.to_markdown()}")
        
        if(len(temp_df) > 0):
            result_dictionary[reason] = list(temp_df['S.No.'])
        
        reason = 'Blank MPBN Node Type found'
        
        temp_df = df[df['MPBN Node Type ( Router/Switch )'] == 'TempNA']
        logging.debug(f"Finding the blank MPBN Node Type ( Router/Switch ) entry in VPLS -1 for node_ip {ip_node} ===>\n{temp_df.to_markdown()}")
        
        if(len(temp_df) > 0):
            result_dictionary[reason] = list(temp_df['S.No.'])
        
        reason = 'Space found in VPLS Name'
        temp_df = df[df['VPLS Name'].str.strip().str.contains(' ')]
        logging.debug(f"Finding the {reason} in VPLS -1 for node_ip {ip_node} ===>\n{temp_df.to_markdown()}")
        if(len(temp_df) > 0):
            result_dictionary[reason] = list(temp_df['S.No.'])
    
    if(len(df_add) > 0):
        i = 0
        reason = 'Blank VPLS Name found'
        while(i < len(df_add)):
            if(df_add.iloc[i, df_add.columns.get_loc('VPLS Name')] == 'TempNA'):
                if(not reason in result_dictionary.keys()):
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(df_add.iloc[i,df.columns.get_loc('S.No.')])
                
                else:
                    result_dictionary[reason].append(df_add.iloc[i,df.columns.get_loc('S.No.')])
            i+=1
        logging.debug(f"Entered the enteries for 'Blank VPLS Name' for node ip {ip_node} for VPLS 1 ==>\n{result_dictionary}\n\n")

        temp_df = df_add[df_add.duplicated(subset = ['VPLS ID'],keep = False)]
        if(len(temp_df) > 0):
            logging.debug(f"Found duplicate VPLS IDs for VPLS-1 for node_ip ({ip_node})==>\n{temp_df.to_markdown()}\n\n")
            reason = 'Same VPLS ID found ==> for VPLS IDs(S.No. group)'
            result_dictionary[reason] = same_vpls_id_found_error_message_generator(dataframe=temp_df, common_vpls_ids= temp_df['VPLS ID'].unique().astype(int))
            del temp_df

    # reason = 'VPLS ID of Action \'Add\' present in Action \'Modify/Delete\''
    reason = 'Same VPLS ID found ==> for VPLS IDs(S.No. group)'
    
    if(len(df_add) > 0):
        df_add_unique_VPLS_IDs = df_add['VPLS ID'].unique()
        
        if("TempNA" in df_add_unique_VPLS_IDs):
            df_add_unique_VPLS_IDs = np.delete(df_add_unique_VPLS_IDs,np.argwhere(df_add_unique_VPLS_IDs == 'TempNA'))
            df_add_unique_VPLS_IDs = df_add_unique_VPLS_IDs.astype(int)
        
        logging.debug(f"df_add_unique_VPLS_IDs for node_ip({ip_node}) ==>\n{df_add_unique_VPLS_IDs}")


    if(len(df_delete_modify) > 0):
        df_delete_modify_VPLS_IDs = df_delete_modify['VPLS ID'].unique()

        if("TempNA" in df_delete_modify_VPLS_IDs):
            df_delete_modify_VPLS_IDs = np.delete(df_delete_modify_VPLS_IDs, np.argwhere(df_delete_modify_VPLS_IDs == "TempNA"))
            df_delete_modify_VPLS_IDs = df_delete_modify_VPLS_IDs.astype(int)
            
        logging.debug(f"df_delete_modify_VPLS_IDs for node_ip({ip_node}) ==>\n{df_delete_modify_VPLS_IDs}")

    logging.debug(f"Finding the setintersection for the df_add and df_delete for node_ip ({ip_node}) for VPLS-1 {np.intersect1d(df_add_unique_VPLS_IDs,df_delete_modify_VPLS_IDs).astype(int)}")
    set_intersection_between_Add_and_Modify_Delete_dfs = np.intersect1d(df_add_unique_VPLS_IDs,df_delete_modify_VPLS_IDs).astype(int)
    
    if(set_intersection_between_Add_and_Modify_Delete_dfs.size > 0):
        # reason = f"{reason} {', '.join([str(int(elements)) for elements in set_intersection_between_Add_and_Modify_Delete_dfs])}"

        # result_dictionary[reason] = list((df[df['VPLS ID'].isin(list(set_intersection_between_Add_and_Modify_Delete_dfs))])['S.No.'])
        result_dictionary[reason] = same_vpls_id_found_error_message_generator(dataframe=df, common_vpls_ids=set_intersection_between_Add_and_Modify_Delete_dfs )
        logging.debug(f"Got the filtered data from intersection between add and modify_delete dfs in VPLS-1 for node ip ('{ip_node}') ==> \n{df[df['VPLS ID'].isin(list(set_intersection_between_Add_and_Modify_Delete_dfs))].to_markdown()}\n")

        logging.debug(f"Entered the enteries for 'Common VPLS IDs in Add and Modify/Delete Actions' for node ip {ip_node} for VPLS-1 ==>\n{result_dictionary}\n\n")

    logging.debug(f"The result_dictionary for node_ip({ip_node}) for VPLS-1 ==>\n {result_dictionary}")
    
    logging.shutdown()
    return result_dictionary
