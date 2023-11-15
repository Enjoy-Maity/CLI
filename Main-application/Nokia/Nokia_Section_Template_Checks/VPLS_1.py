import numpy as np
import pandas as pd
import logging

log_file_path = "C:/Ericsson_Application_Logs/CLI_Automation_Logs/"
Path(log_file_path).mkdir(parents=True,exist_ok=True)

log_file = os.path.join(log_file_path,"Template_checks.log")

logging.basicConfig(filename=log_file,
                        filemode="a",
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt='%d-%b-%Y %I:%M:%S %p',
                        encoding= "UTF-8",
                        level=logging.DEBUG)

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
           description ====> contains the dictionary with the list of all errors found in Template Checks with reason as keys.
    """

    logging.debug(f"Created the empty dictionary for returning as result for IP Node: -{ip_node} for VPLS 1 section")
    
    result_dictionary           = {}
    df                          = dataframe.fillna("TempNA")
    logging.debug(f"Created a copy of dataframe passed for node_ip({ip_node}) for VPLS-1:-\n{df.to_markdown()}")
    
    df_add                      = df[df['Action'] == 'A:Add']
    logging.debug(f"Created the filtered copy of the Dataframe for Action 'A:Add' for node_ip({ip_node}) for VPLS-1:-\n{df_add.to_markdown()}")
    
    df_delete_modify            = df[df['Action'].isin(['A:Delete','A:Modify'])]
    logging.debug(f"Created the filtered copy of the Dataframe for Action 'A:Modify/A:Delete' for node_ip({ip_node}) for VPLS-1:-\n{df_delete_modify.to_markdown()}")

    logging.debug(f"Going to check the VPLS ID for VPLS-1 of node_ip({ip_node})")
    
    if(len(df) > 0):
        reason = ''

        i = 0
        while(i < len(df)):
            if(df.iloc[i,'VPLS ID'] == "TempNA"):
                reason = "Blank VPLS ID"

                if(not reason in result_dictionary.keys()):
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(df.iloc[i,df.columns.get_loc('S.No.')])

                else:
                    result_dictionary[reason].append(df.iloc[i,df.columns.get_loc('S.No.')])
            i+=1
        logging.debug(f"Entered the enteries for 'Blank VPLS ID' for node ip {ip_node} for VPLS 1 ==>\n{result_dictionary}")
    
    if(len(df_add) > 0):
        i = 0
        reason = 'Blank VPLS Name for Add Action'
        while(i < len(df_add)):
            if((df_add.iloc[i, df_add.columns.get_loc('Action')].strip().upper() == 'A:ADD') and (df_add.iloc[i, df_add.columns.get_loc('Action')])):
                if(not reason in result_dictionary.keys()):
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(df_add.iloc[i,df.columns.get_loc('S.No.')])
                
                else:
                    result_dictionary[reason].append(df_add.iloc[i,df.columns.get_loc('S.No.')])
            i+=1
        logging.debug(f"Entered the enteries for 'Blank VPLS Name' for node ip {ip_node} for VPLS 1 ==>\n{result_dictionary}")

    reason = 'VPLS ID of Action \'Add\' present in Action \'Modify/Delete\''
    
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

    logging.debug("Finding the setintersection for the df_add and df_delete for VPLS-1 ")
    set_intersection_between_Add_and_Modify_Delete_dfs = np.intersect1d(df_add_unique_VPLS_IDs,df_delete_modify_VPLS_IDs)
    
    if(set_intersection_between_Add_and_Modify_Delete_dfs.size > 0):
        reason = f"{reason} ==> for VPLS IDs : {', '.join([str(elements) for elements in set_intersection_between_Add_and_Modify_Delete_dfs])}"
        result_dictionary[reason] = list((df_add[df_add['VPLS ID'].isin(list(set_intersection_between_Add_and_Modify_Delete_dfs))])['S.No.'])
        logging.debug(f"Entered the  enteries for 'Common VPLS IDs in Add and Modify/Delete Actions' for node ip {ip_node} for VPLS-1 ==>\n{result_dictionary}")

    logging.debug(f"The result_dictionary for node_ip({ip_node}) for VPLS-1 ==>\n {result_dictionary}")
    
    logging.shutdown()
    return result_dictionary