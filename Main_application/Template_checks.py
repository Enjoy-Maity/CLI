import logging
import pickle
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



def pickling_func(dictionary:dict, vendor_selected:str) -> None:
    username = os.popen(r'cmd.exe /C "echo %username%"').read()
    path_for_pickle_files = f"C:\\Users\\{username.strip()}\\AppData\\Local\\CLI_Automation\\Vendor_pickles\\{vendor_selected.upper()}.pickle"
    parent_dir = os.path.dirname(path_for_pickle_files)

    logging.debug("Creating the folder for the Application in Appdata if not exists")
    Path(parent_dir).mkdir(parents=True,exist_ok=True)

    
    with open(path_for_pickle_files,'wb') as f:
        pickle.dump(dictionary,f)
        f.close()
    
    logging.debug("Checking the pickle file thus created")
    with open(path_for_pickle_files,'rb') as f:
        logging.debug(f"Pickle file =====>\n\t{pickle.load(f)}")
        f.close()
        
    del f



def action_blank_check(*args) -> list:
    
    try:
        assert isinstance(args[0],pd.DataFrame)
        dataframe = args[0]
        result = list()
        
        # dataframe.fillna("TempNA", inplace = True)
        dataframe = dataframe.where(~dataframe.isna(),"TempNA")
        
        i = 0

        while(i < len(dataframe)):
            if(dataframe.iloc[i,dataframe.columns.get_loc('Action')] == "TempNA"):
                result.append(str(dataframe.iloc[i,dataframe.columns.get_loc('S.No.')]))
            i+=1
            
        return result
    
    except AssertionError as e:
        logging.debug(f"Assertion Error====>\n{traceback.format_exc()}\n{e}")
        messagebox.showerror('Wrong Data Type!',e)

def main_func(**kwargs) -> str:
    """
        Performs the Initial General Template checks and then calls the module specific to the vendor to perform further Template checks.

        Arguments : (**kwargs) ===> provides a dictionary of arguments.
            kwargs ===>  'filename' : str
                            description =====> path for file containing 'Host Details'
                         
                         'vendor_selected' : str
                            description =====> selected vendor by the user in GUI
        
        return flag
            flag : str
                description ===> contains 'Unsuccessful' or 'Successful' string corresponding the status of execution completion
    """
    
    log_file_path = "C:/Ericsson_Application_Logs/CLI_Automation_Logs/"
    Path(log_file_path).mkdir(parents=True,exist_ok=True)

    log_file = os.path.join(log_file_path,"Template_checks.log")

    today = datetime.now()
    today = today.replace(hour=0, minute=0, second=0)

    if(os.path.exists(log_file)):
        #getting the creation time of the log file
        log_file_create_time= datetime.fromtimestamp(os.path.getctime(log_file))

        if(log_file_create_time < today):
            os.remove(log_file)

    global flag; flag = ''

    logging.basicConfig(filename=log_file,
                                 filemode="a",
                                 format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({'%(module)s'}): {'%(message)s'}",
                                 datefmt='%d-%b-%Y %I:%M:%S %p',
                                 encoding= "UTF-8",
                                 level=logging.DEBUG)
    logging.captureWarnings(capture=True)
    filename = str(kwargs['filename'])     # File containing the host details
    
    username = (os.popen('cmd.exe /C "echo %username%"').read()).strip()
    pickle_path = rf"C:\Users\{username}\AppData\Local\CLI_Automation\Host_details_Pickle_file\Host_details.pkl"
    file_name = pd.read_pickle()
    logging.info("#######################################################<<Starting the Root Template Checks Process>>########################################################################")

    try:
        logging.debug("Checking whether the file uploaded by the user is an excel file or not")
        assert ((len(file_name) > 0) and (file_name.strip().endswith('.xlsx'))), 'Please Select the Host details Excel Workbook!'
        
        parent_folder = os.path.dirname(file_name)
        input_design_file_name = "{}_Design_Input_Sheet.xlsx"

        logging.info("Reading the file selected by the user")
        # host_details_excelfile = pd.ExcelFile(file_name)
        # host_details_sheet     = pd.read_excel(host_details_excelfile,
        #                                        sheet_name='Host Details',
        #                                        engine='openpyxl')
        
        host_details_sheet      = file_name
        
        logging.info(f"Read the Host Details ====>\n{host_details_sheet}")
        
        logging.info("Checking out the unique vendors mentioned in the Host Details")
        unique_vendors_mentioned = host_details_sheet['Vendor'].dropna().unique()
        
        logging.debug(f"Entering the loop for checking specific vendors Design Input workbooks mentioned:\n {'\n'.join(unique_vendors_mentioned)}")
        i = 0
        while(i < unique_vendors_mentioned.size):
            if(not Path(os.path.join(parent_folder,input_design_file_name.format(unique_vendors_mentioned[i]))).exists()):
                # host_details_excelfile.close()
                # del host_details_excelfile
                raise CustomException("Design Input File Missing!",
                                      f"{input_design_file_name.format(unique_vendors_mentioned[i])} not found in {parent_folder}, Kindly Check!")
            i+=1
        
        vendor_selected = kwargs['vendor_selected']
        logging.debug(f"Looping through selected vendor {vendor_selected} design input workbook")
        
        selected_vendor_book_excel_file = pd.ExcelFile(os.path.join(parent_folder,input_design_file_name.format(vendor_selected.strip())))
        selected_vendor_book_excel_sheetnames = selected_vendor_book_excel_file.sheet_names
        
        logging.debug(f"Sheets Found in the {input_design_file_name.format(vendor_selected)} are :\n\t{'\n\t'.join(selected_vendor_book_excel_sheetnames)}")

        logging.debug("Getting the list of unique node ips present in the host details")
        unique_host_ips_present_in_the_host_details_sheet = host_details_sheet['Host_IP'].dropna().unique()

        logging.info("Creating a list for the getting the host details not present in the host details sheet inside in vendor workbook.")
        host_details_not_present_in_the_workbook = []
        host_details_present_in_workbook_but_not_in_host_details = []

        i = 0
        while(i < len(selected_vendor_book_excel_sheetnames)):
            if(not selected_vendor_book_excel_sheetnames[i] in unique_host_ips_present_in_the_host_details_sheet):
                host_details_present_in_workbook_but_not_in_host_details.append(selected_vendor_book_excel_sheetnames[i])
            i+=1

        i = 0
        while(i < unique_host_ips_present_in_the_host_details_sheet.size):
            if(not unique_host_ips_present_in_the_host_details_sheet[i] in selected_vendor_book_excel_sheetnames):
                host_details_not_present_in_the_workbook.append(unique_host_ips_present_in_the_host_details_sheet[i])
            i+=1

        response = None

        if((len(host_details_not_present_in_the_workbook) > 0) and 
           (len(host_details_present_in_workbook_but_not_in_host_details) > 0)):
            response = messagebox.askyesno("Wrong Data Input!",f"Host Details not found in {input_design_file_name.format(vendor_selected)} workbook:\n\n{', '.join(host_details_not_present_in_the_workbook)}\n\nand\n\n extra Host IP details found :\n\n{', '.join(host_details_present_in_workbook_but_not_in_host_details)}\n\nDo You want to proceed?",icon = 'warning')
        
        else:
            if(len(host_details_not_present_in_the_workbook) > 0):
                response = messagebox.askyesno("Host Details Missing!",f"Host Details IPs Missing in {input_design_file_name.format(vendor_selected)}:\n\n{', '.join(host_details_not_present_in_the_workbook)}\n\nDo You want to proceed?",icon = 'warning')
            
            if(len(host_details_present_in_workbook_but_not_in_host_details) > 0):
                response = messagebox.askyesno("Extra Host Details Found!",f"Extra Host IP details found in {input_design_file_name.format(vendor_selected)} but not present in uploaded Host Details:\n\n{', '.join(host_details_not_present_in_the_workbook)}\n\nDo You want to proceed?",icon = 'warning')

        if((response != None) and (not response)):
            selected_vendor_book_excel_file.close()
            del selected_vendor_book_excel_file
            # host_details_excelfile.close()
            # del selected_vendor_book_excel_file

            raise CustomException("User Selected 'No'!","The User Have Selected 'No', so stopping the execution!")
        
        logging.info("Now calling the section splitter in a try except block.")

        try:
            logging.info("Creating a thread list")
            thread_list = []
            i = 0
            while(i < len(selected_vendor_book_excel_sheetnames)):
                df = pd.read_excel(selected_vendor_book_excel_file,
                                   selected_vendor_book_excel_sheetnames[i],
                                   engine = 'openpyxl')
                temp_thread = CustomThread(target=section_splitter,args = (df,'Template_checks'))
                temp_thread.daemon = True
                thread_list.append(temp_thread)
                temp_thread.start()
                i+=1
            
            node_to_section_dictionary = {}
            logging.debug("Ending all the threads and getting their return Values")
            i = 0
            while(i < len(selected_vendor_book_excel_sheetnames)):
                node_to_section_dictionary[selected_vendor_book_excel_sheetnames[i]] = thread_list[i].join()
                i+=1
        
        except CustomException:
            # global flag;
            flag = 'Unsuccessful'
            logging.error(f"{traceback.format_exc()}\n\nraised CustomException==>\ntitle = {e.title}\nmessage = {e.message}")

        except Exception as e:
            flag = 'Unsuccessful'
            logging.error(f"{traceback.format_exc()}\n\nException:==>{e}")
            messagebox.showerror("Exception Occurred!",e)

        logging.info("Checking whether there is any worksheet, which contains no data for any of the sections")

        i = 0
        list_of_sheet_with_empty_section_data = []
        keys_pertaining_nodes = list(node_to_section_dictionary.keys())
        while(i < len(keys_pertaining_nodes)):
            selected_node = keys_pertaining_nodes[i]
            
            if(len(node_to_section_dictionary[selected_node]) == 0):
                list_of_sheet_with_empty_section_data.append(selected_node)
            i+=1

        logging.debug("Raising exception if any sheet without any section data found!")
        
        if(len(list_of_sheet_with_empty_section_data) > 0):
            raise CustomException("Empty Worksheet Found!",
                                      f"Worksheet with No Section data found, Kindly Check {input_design_file_name.format(vendor_selected)} for the below mentioned nodes:\n\n\t{'\n\t'.join(list_of_sheet_with_empty_section_data)}\n\nKindly Ckeck!")

        
        
        logging.debug("Checking if any section of any node ip sheet has blank value in the 'Action' column.")
        try:
            i = 0
            thread_list = []
            while(i < len(keys_pertaining_nodes)):
                selected_node = keys_pertaining_nodes[i]
                sections      = list(node_to_section_dictionary[selected_node].keys())

                j = 0
                while(j < len(sections)):
                    selected_section = sections[j]
                    dataframe = node_to_section_dictionary[selected_node][selected_section]
                    temp_thread = CustomThread(target = action_blank_check,
                                               args = (dataframe,))
                    temp_thread.daemon = True
                    thread_list.append(temp_thread)
                    temp_thread.start()
                    j+=1
                i+=1

            thread_return_list = []
            thread_list_len = len(thread_list)
            k  = 0                              # Incrementer for the thread_list

            dictionary_for_message = {}

            logging.debug("Getting all the return values from the section thread list for checking blank 'Action' value.")
            i = 0
            while(i < thread_list_len):
                thread_return_list.append(thread_list[i].join())
                i+=1

            logging.debug(f"Got the thread_return_list :-\n{thread_return_list}")
            i = 0
            while(i < len(keys_pertaining_nodes)):
                selected_node = keys_pertaining_nodes[i]
                sections      = list(node_to_section_dictionary[selected_node].keys())
                
                section_dictionary_for_message = {}
                j = 0
                while(j < len(sections)):
                    selected_section = sections[j]
                    try:
                        if(len(thread_return_list[k]) != 0):
                            section_dictionary_for_message[selected_section] = thread_return_list[k]
                    except:
                        if(thread_return_list[k] != None):
                            section_dictionary_for_message[selected_section] = thread_return_list[k]
                    k+=1
                    j+=1
                
                if(len(section_dictionary_for_message) != 0):
                    dictionary_for_message[selected_node] = section_dictionary_for_message

                i+=1
            
            error_folder = os.path.join(os.path.join(parent_folder,"Error_Folder"),"Design_Input_Checks_Results")
            logging.info(f"Created '{error_folder}' if not existed, if existed did not raised an exception")
            
            logging.debug("Creating the path for the folder for getting errors")
            Path(error_folder).mkdir(parents=True,exist_ok=True)
            
            
            logging.info("Creating the Error File path for writing into the exceptions")
            error_file = os.path.join(error_folder,"General_Design_Input_Checks_Errors.txt")
            
            if(len(dictionary_for_message) > 0):
                dictionary_for_message_keys_list = list(dictionary_for_message.keys())

                message_to_be_written = f"General Check Issues:\n\nIssues have been found for below '{vendor_selected}' nodes for Sr.No on {datetime.now().strftime('%d-%b-%Y %H:%M %A')}\n\n"
                i = 0 
                while(i < len(dictionary_for_message.keys())):
                    node_selected = dictionary_for_message_keys_list[i]
                    sections_in_dictionary_for_message = list(dictionary_for_message[node_selected].keys())

                    message_to_be_written = f"{message_to_be_written}Node :- '{node_selected}'\n"
                    j = 0
                    while(j < len(sections_in_dictionary_for_message)):
                        section_selected = sections_in_dictionary_for_message[j]
                        message_to_be_written = f"{message_to_be_written}Section : '{section_selected}' :- Sr.No.: ({','.join(str(element) for element in dictionary_for_message[node_selected][section_selected])})\n"
                        j+=1
                    
                    message_to_be_written = f"{message_to_be_written}\n\n"
                    i+=1

                
                with open(error_file,'w') as f:
                    f.write(message_to_be_written)
                    f.close()
                
                raise CustomException("Input Issue!",
                                     f"Issues have been observed in uploaded input sheet. To find the issue in detail, Please! check the 'Template_Checks_error_Vendor_wise' inside 'Error_Folder'")
            
            # with open(error_file, 'w') as f:
            #     f.write('')
            #     f.close()

        except CustomException:
            # global flag;
            flag = 'Unsuccessful'
            logging.error(f"{traceback.format_exc()}\n\nraised CustomException==>\ntitle = {e.title}\nmessage = {e.message}")

        except Exception as e:
            flag = 'Unsuccessful'
            logging.error(f"{traceback.format_exc()}\n\nException:==>{e}")
            messagebox.showerror("Exception Occurred!",e)

        else:
            # logging.info(f"Deleting host_details_excelfile")
            # host_details_excelfile.close()
            # del host_details_excelfile

            logging.debug("Calling the Pickling Function to create pickles")
            pickling_func(dictionary=node_to_section_dictionary,
                        vendor_selected=vendor_selected)
            
            logging.info("Going to perform template checks on 'Nokia' Design Template")
            if(vendor_selected.upper() == 'NOKIA'):
                from Nokia.Nokia_Template_Checks import nokia_main_func
                flag = nokia_main_func(log_file = log_file,
                                        parent_folder = parent_folder)
            
            logging.info("Going to perform template checks on 'Cisco' Design Template")
            if(vendor_selected.upper() == 'CISCO'):
                pass
            
            logging.info("Going to perform template checks on 'Huawei' Design Template")
            if(vendor_selected.upper() == 'HUAWEI'):
                pass
            
            logging.info("Going to perform template checks on 'Ericsson' Design Template")
            if(vendor_selected.upper() == 'ERICSSON'):
                pass
        
        if(flag == ''):
            flag = 'Unsuccessful'

        if(flag != 'Unsuccessful'):
            flag = 'Successful'
    
    except CustomException as e:
        # global flag;
        flag = 'Unsuccessful'
        logging.error(f"{traceback.format_exc()}\n\nraised CustomException==>\ntitle = {e.title}\nmessage = {e.message}")
    
    except AssertionError as e:
        flag = 'Unsuccessful'
        logging.error(f"{traceback.format_exc()}\n\nraised AssertionError==>\ntitle = {e.title}\nmessage = {e.message}")
        messagebox.showerror("Wrong Input File",e)


    except Exception as e:
        flag = 'Unsuccessful'
        logging.error(f"{traceback.format_exc()}\n\nException:==>{e}")
        messagebox.showerror("Exception Occurred!",e)
    
    finally:
        logging.info(f"Returning {flag =}")
        logging.shutdown()
        return flag

# main_func(filename=r"C:\Users\emaienj\Downloads\VPLS_CLI_Design_Documents\VPLS_CLI_Design_Documents\Nokia_Design Input_Template.xlsx", vendor_selected = 'Nokia')