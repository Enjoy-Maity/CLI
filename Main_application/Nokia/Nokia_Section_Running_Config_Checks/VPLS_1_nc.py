import os
import logging
import pandas as pd
import re


def starter_func() -> None:
    from beginner_importer import starter_func
    starter_func()
    from file_lines_handler import File_lines_handler as flh
    # global flag; flag = ''

# def binary_search(file_lines_list: list, left_index: int, right_index: int, key_to_searched: str) -> bool:
#     """
#         Performs Binary search to find strin
#     """
#     result = False
    
#     return result

def add_action_checks(dataframe: pd.DataFrame, running_config_backup_file_lines: list, ip_node: str, vpls_id_starter_lines_filter : list) -> dict:
    """
        Performs the Checks for the presence of VPLS ID in the running config backup files
        
        Arguments : (dataframe, running_config_backup_file_lines,ip_node)
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
    
    result_dictionary = {}
    
    reason = "Action:Add VPLS ID Clash found"
    i = 0
    while(i < len(dataframe)):
        vpls_id_to_be_searched = int(dataframe.iloc[i,dataframe.columns.get_loc("VPLS ID")])
        j = 0
        while(j < len(vpls_id_starter_lines_filter)):
            if(vpls_id_starter_lines_filter[j].startswith(f"vpls {vpls_id_to_be_searched} ")):
                if(not reason in result_dictionary):
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(dataframe.iloc[i,dataframe.columns.get_loc("S.No.")])
                
                else:
                    result_dictionary[reason].append(dataframe)
                break
            j+=1
        i+=1
        
    
    reason = "Action:Add VPLS Name Clash found"
    service_name_lines_filter_list = flh().file_lines_starter_filter(file_lines_list=running_config_backup_file_lines,
                                                                     start_word = "service-name")
    
    i = 0
    while(i < len(dataframe)):
        vpls_name_to_be_searched = str(dataframe.iloc[i,dataframe.columns.get_loc("VPLS Name")])
        j = 0
        while(j < len(service_name_lines_filter_list)):
            if(vpls_id_starter_lines_filter[j].startswith(f"service-name \"{vpls_name_to_be_searched}\"")):
                if(not reason in result_dictionary):
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(dataframe.iloc[i,dataframe.columns.get_loc("S.No.")])
                
                else:
                    result_dictionary[reason].append(dataframe)
                break
            j+=1
        i+=1
    
    return result_dictionary

def modify_delete_action_checks(dataframe: pd.DataFrame, running_config_backup_file_lines: list, ip_node: str, vpls_id_starter_lines_filter : list) -> dict:
    """
        Performs the checks for the presence of SDP variable in the running config backup files
        
        Arguments : (dataframe, running_config_backup_file_lines,ip_node)
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
    
    result_dictionary = {}
    
    reason = "Action:Modify/Delete VPLS ID not found"
    i = 0
    while(i < len(dataframe)):
        vpls_id_to_be_searched = int(dataframe.iloc[i,dataframe.columns.get_loc("VPLS ID")])
        j = 0
        flag = False
        while(j < len(vpls_id_starter_lines_filter)):
            if(vpls_id_starter_lines_filter[j].startswith(f"vpls {vpls_id_to_be_searched} ")):
                flag = True
                break
            j+=1
        
        if(not flag):
            if(not reason in result_dictionary):
                    result_dictionary[reason] = []
                    result_dictionary[reason].append(dataframe.iloc[i,dataframe.columns.get_loc("S.No.")])
                
            else:
                result_dictionary[reason].append(dataframe)
        i+=1
    


def main_func(dataframe: pd.DataFrame, ip_node: str, running_config_backup_file_lines: list) -> dict:
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
    
    global log_file; log_file = rf"C:/Ericsson_Application_Logs/CLI_Automation_Logs/Running_Config_Checks(Node_Checks).log"
    
    logging.basicConfig(filename= log_file,
                        filemode='a',
                        format= f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: (Main-application/Nokia/{os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt= "%d-%b-%Y %I:%M:%S %p",
                        encoding="UTF-8",
                        level=logging.DEBUG)
    logging.debug(f"Ran the importer Function for {ip_node}")
    
    dataframe = dataframe.fillna("TempNA")
    
    i = 0
    starter_func()
    result_dictionary = {}
    
    # global flag;
    
    try:
        add_action_dataframe = dataframe[dataframe['Action'].str.upper().str.contains("ADD")]
        add_action_dataframe_checks = {}
        
        vpls_id_starter_lines_filter = flh().file_lines_starter_filter(file_lines_list = running_config_backup_file_lines,
                                                                  start_word = "vpls")
        
        add_action_thread = ""
        if(len(add_action_dataframe) > 0):
            logging.debug(f"Creating the thread for checking the presence of VPLS ID for {ip_node} for the dataframe\n{add_action_dataframe.to_markdown()}\n")
            add_action_thread = CustomThread(target = add_action_checks,
                                             args=(add_action_dataframe,running_config_backup_file_lines,ip_node,vpls_id_starter_lines_filter))
            add_action_thread.daemon = True
            add_action_thread.start()
            
        modify_delete_thread = ""
        modify_delete_action_dataframe = dataframe[dataframe['Action'].str.upper().str.contains("MODIFY|DELETE")]
        if(len(modify_delete_action_dataframe) > 0):
            logging.debug(f"Creating the thread for checking the sdp variable for {ip_node} for the dataframe\n{modify_delete_action_dataframe.to_markdown()}\n")
            modify_delete_thread = CustomThread(target = modify_delete_action_checks,
                                                args = (modify_delete_action_dataframe,running_config_backup_file_lines,ip_node,vpls_id_starter_lines_filter))
            modify_delete_thread.daemon = True
            modify_delete_thread.start()
            
        
        if((add_action_thread in locals()) or (add_action_thread in globals())):
            if(isinstance(add_action_thread,CustomThread)):
                    result_dictionary = add_action_thread.join()
                
        
        if((modify_delete_thread in locals()) or (modify_delete_thread in globals())):
            if(isinstance(modify_delete_thread,CustomThread)):
                if(len(result_dictionary) == 0):
                    result_dictionary = modify_delete_thread.join()
                
                else:
                    result_dictionary.update(modify_delete_thread.join())
    
    except CustomException as e:
        
        pass
    
    except Exception as e:
        pass
    
    finally:
        logging.shutdown()
        return result_dictionary