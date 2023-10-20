import logging
import os
from pathlib import Path
import pandas as pd
import numpy as np
import traceback
from tkinter import messagebox
from Custom_Exception import CustomException
from datetime import datetime
from CustomThread import CustomThread
from Section_splitter import section_splitter

log_file_path = "C:/Ericsson_Application_Logs/CLI_Automation_Logs/"
Path(log_file_path).mkdir(parents=True,exist_ok=True)

log_file = os.path.join(log_file_path,"Template_checks.log")

today = datetime.now()

if(os.path.exists(log_file)):
    #getting the creation time of the log file
    log_file_create_time= datetime.fromtimestamp(os.path.getctime(log_file))

    if(log_file_create_time < today):
        os.remove(log_file)


logging.basicConfig(filename=log_file,
                             filemode="a",
                             format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({'%(module)s'}): {'%(message)s'}",
                             datefmt='%d-%b-%Y %I:%M:%S %p',
                             encoding= "UTF-8",
                             level=logging.DEBUG)


def main_func(**kwargs):
    file_name = str(kwargs['filename'])
    logging.info("Starting the Root Template Checks Process")

    try:
        logging.info("Reading the file selected by the user")
        if((len(file_name)!=0) and (file_name.endswith('.xlsx'))):
            file_reader = pd.ExcelFile(file_name)
            sheetnames  = file_reader.sheet_names

            if(not 'Host Details' in sheetnames):
                raise CustomException('Host Details Not Found!',
                                      'Host Details in the uploaded sheet not found, Kindly Check!')

            host_details_df = pd.read_excel(file_name,'Host Details')
            unique_host_ips = host_details_df['Host_IP'].unique()

            # if(pd.NA in nan_test ):
            nan_test = any(pd.isna(element) for element in unique_host_ips)
            
            # if(np.nan in nan_test):
            #     nan_test = any(pd.isna(element) for element in unique_host_ips)            
            blank_Sr_no_list = []
            # If nan_test is true
            if(nan_test):
                i = 0
                while(i<len(host_details_df)):
                    if(pd.isna(host_details_df.iloc[i]['Host_IP'])):
                        blank_Sr_no_list.append(host_details_df.iloc[i]['Sr.No'])
                    i+=1
            
            # temp_array = unique_host_ips[~np.isnan(unique_host_ips)]
            temp_array = unique_host_ips[~pd.isna(unique_host_ips)]
            host_details_df.dropna(inplace= True)
            

            # Checking duplicated Host IPs in the Host Details sheet
            duplicate_host_ip_boolean_series = host_details_df.duplicated(subset=['Host_IP'])
            duplicated_host_ip_Sr_no_list = []
            logging.info("Checking duplicated host ip details in the Host Details sheet")
            
            i = 0
            while(i < duplicate_host_ip_boolean_series.size):
                if(duplicate_host_ip_boolean_series[i]):
                    temp_array_list = host_details_df[host_details_df['Host_IP'] == host_details_df.iloc[i]['Host_IP']]
                    duplicated_host_ip_Sr_no_list.extend(list(temp_array_list['Sr.No']))
                i+=1
            
            
            if(len(duplicated_host_ip_Sr_no_list) >0):
                duplicated_host_ip_Sr_no_list = np.unique(np.array(duplicated_host_ip_Sr_no_list))
            
            if((len(blank_Sr_no_list)> 0) and (len(duplicated_host_ip_Sr_no_list) > 0)):
                file_reader.close()
                del file_reader
                logging.error("Blank Host IP and duplicated Host IP details are found!")
                raise CustomException("Host IP Details Incorrect!",
                                      f"Blank IP Details found for Sr no.: {', '.join(str(element) for element in blank_Sr_no_list)}\n\nand \n\nDuplicate Host IPs found for Sr no: {', '.join(str(element) for element in duplicated_host_ip_Sr_no_list)}")
            
            if(len(blank_Sr_no_list) > 0):
                file_reader.close()
                del file_reader
                logging.error("Blank Host IP details are found!")
                raise CustomException("Blank Host IP Details Found!",
                                      f"Blank IP Details found for Sr no.: {', '.join(str(element) for element in blank_Sr_no_list)}")
            
            if(len(duplicated_host_ip_Sr_no_list) > 0):
                file_reader.close()
                del file_reader
                logging.error("Duplicated Host IP details are found!")
                raise CustomException("Host IP Details Incorrect!",
                                      f"Duplicate Host IPs found for Sr no: {', '.join(str(element) for element in duplicated_host_ip_Sr_no_list)}")

            
            # Finding the non_available_ip_sheets mentioned in the 'Host Details' sheet
            sheetnames.remove('Host Details')
            non_available_host_ip_sheets = []
            non_available_sheet_ip_in_unique_host_ips = []
            if(unique_host_ips.size >= (len(sheetnames))):
                i = 0
                while(i<unique_host_ips.size):
                    if(not unique_host_ips[i] in sheetnames):
                        non_available_host_ip_sheets.append(unique_host_ips[i])
                    i+=1
            
            # Raising the custom exception in case the len(non_available_host_ip_sheets) is greater than 0
            if(len(non_available_host_ip_sheets) > 0):
                raise CustomException("Host IP Details Incorrect!",
                                      f"Please cross-check the uploaded workbook as host ip/s '{', '.join(non_available_host_ip_sheets)}' input sheets are missing!")

            if(unique_host_ips.size < len(sheetnames)):
                i = 0
                while(i<len(sheetnames)):
                    if(not sheetnames[i] in unique_host_ips):
                        non_available_sheet_ip_in_unique_host_ips.append(sheetnames[i])
                    i+=1
                
            # Raising the custom exception in case the len(non_available_sheet_ip_in_unique_host_ips) is greater than 0
            if(len(non_available_sheet_ip_in_unique_host_ips) > 0):
                raise CustomException("Host IP Details Not Found!",
                                      f"Please cross-check the uploaded workbook as sheets -ip/s '{', '.join(non_available_sheet_ip_in_unique_host_ips)}' are not found in host details!")
            
            # Calling the section Splitter for splitting the nodes according to the sections and then according to the actions
            thread_list = []
            i = 0
            while(i<len(sheetnames)):
                temp_var_for_thread = CustomThread(target = section_splitter,
                                                args=(pd.read_excel(file_reader,sheetnames[i],engine='openpyxl'),'Template_checks'))
                thread_list.append(temp_var_for_thread)
                temp_var_for_thread.daemon = True
                temp_var_for_thread.start()
                i+=1
            
            dictionary_for_node_to_section = {}
            i = 0
            while(i<len(sheetnames)):
                dictionary_for_node_to_section[sheetnames[i]] = thread_list[i].join()
                print("\n\n\n\n\n\n\n")
                # print(dictionary_for_node_to_section[sheetnames[i]])
                print(sheetnames[i])
                sections = list(dictionary_for_node_to_section[sheetnames[i]].keys())
                j = 0 
                while(j< len(sections)):
                    print(f"{sections[j]} ==> {dictionary_for_node_to_section[sheetnames[i]][sections[j]]}\n\n")
                    j+=1
                i+=1
            
            
            # file_read   = pd.read_excel(file_reader,)
            file_reader.close()
            del file_reader
    
    except CustomException as e:
        logging.error(f"{traceback.format_exc()}\n\nraised CustomException==>\ntiltle = {e.title}\nmessage = {e.message}")

    except Exception as e:
        logging.error(f"{traceback.format_exc()}\n\nException:==>{e}")
        messagebox.showerror("Exception Occurred!",e)
    

main_func(filename=r"C:\Users\emaienj\Downloads\VPLS_CLI_Design_Documents\VPLS_CLI_Design_Documents\Nokia_Design Input_Template.xlsx")