from pathlib import Path
import sys
import os
import logging
import pickle
import importlib
import traceback
from tkinter import messagebox


def section_wise_input(dictionary: dict, ip_node: str) -> dict:
    """
        Creates thread for calling section wise modules for Template Checks

        Arguments : (dictionary,ip_node)
            dictionary ===> dict
                description =====> {'Section Name' : dataframe containing data for the Section}
                                    'Section Name' ======> Section name, Example -> VPLS-1, VPLS-2, Layer3, etc.
                                    dataframe      ======> Dataframe containing the data in the ip node sheet pertaining to corresponding section key.
            
            ip_node ===> str
                description =====> node ip for which the dictionary is passed as argument.
        
        return thread_result_dictionary
            thread_result_dictionary =====> dict
                description =====> {'Section Name' : [list of 'S.No.' where there is any problem in template checks in any of the section] } 
                                        or
                                    empty dictionary ===> {}
    """
    # print(log_file)
    logging.basicConfig(filename=log_file,
                            filemode="a",
                            format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                            datefmt='%d-%b-%Y %I:%M:%S %p',
                            encoding= "UTF-8",
                            level=logging.DEBUG)
    
    
    sections = list(dictionary.keys())
    thread_dictionary = {}
    i = 0
    while(i < len(sections)):
        try:
            if((len(dictionary[sections[i]])> 0) and (sections[i] in section_dictionary.keys())):
                # Creating a variable to call the module according to section selected in particular iteration
                module_to_be_called = section_dictionary[sections[i]]

                # Creating Thread to call the main_func() of the module corresponding to selected iteration section.
                thread_dictionary[sections[i]] = CustomThread(target= module_to_be_called.main_func,
                                    args= (dictionary[sections[i]],ip_node))
                thread_dictionary[sections[i]].daemon = True
                thread_dictionary[sections[i]].start()
            i+=1
        
        except ImportError as e:
            temp_flag = 'Unsuccessful'
            logging.error(f"ImportError Occurred!======>\n\n{traceback.format_exc()}{e}")
            # messagebox.showerror("Exception Occurred!",e)

        except Exception as e:
            temp_flag = 'Unsuccessful'
            logging.error(f"Exception Occured!======>\n\n{traceback.format_exc()}{e}")
            # messagebox.showerror("Exception Occurred!",e)
    
    thread_result_dictionary = {}
    i = 0
    while(i < len(sections)):
        if(sections[i] in section_dictionary.keys()):
            thread_result_dictionary[sections[i]] = thread_dictionary[sections[i]].join()
        i+=1

    return thread_result_dictionary


def nokia_main_func(**kwargs) -> str:
    """
        Performs the Template Checks for Sections pertaining to 'Nokia' vendor

        Arguments : (**kwargs) ==> arguments in a dictionary
            kwargs ==> 'log_file' : str
                            description =====> path of file containing logs for the module
                        'parent_folder' : str
                            description =====> path of the directory where 'Nokia_Design_Input_Sheet.xlsx' is located
        
        return flag
            flag : str
                description =====> contains 'Unsuccessful' or 'Successful' string corresponding the status of execution completion
    
    """
    
    global flag; flag = ""
    
    global section_dictionary; section_dictionary ={
        'VPLS-1' : importlib.import_module("Nokia.Nokia_Section_Running_Config_Checks.VPLS_1"),
        'VPLS-2' : importlib.import_module("Nokia.Nokia_Section_Running_Config_Checks.VPLS_2")
    }
    
    try:
        # print(kwargs)
        global log_file; log_file = kwargs['log_file']
        parent_folder = kwargs['parent_folder']
        logging.basicConfig(filename=log_file,
                            filemode="a",
                            format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                            datefmt='%d-%b-%Y %I:%M:%S %p',
                            encoding= "UTF-8",
                            level=logging.DEBUG)

        global flag;
        username = os.popen(r'cmd.exe /C "echo %username%"').read()
        path_for_pickle_files = f"C:\\Users\\{username.strip()}\\AppData\\Local\\CLI_Automation\\NOKIA.pickle"
        
        logging.debug("Loading the vendor design input data from pickle")
        f = open(path_for_pickle_files,"rb")
        vendor_design_input_data = pickle.load(f,encoding="UTF-8")
        f.close()

        logging.debug(f"Loaded Nokia design input data =====>\n\n{vendor_design_input_data}")
        
        ip_nodes = list(vendor_design_input_data.keys()) # Getting a list of all the ip node names
        try:
            logging.debug("Started the loop for creation of ip nodes threads")
            thread_dictionary = {}
            i = 0
            while(i< len(ip_nodes)):
                thread_dictionary[ip_nodes[i]] = CustomThread(target = section_wise_input,
                                                            args = (vendor_design_input_data[ip_nodes[i]],ip_nodes[i]))
                thread_dictionary[ip_nodes[i]].daemon = True
                thread_dictionary[ip_nodes[i]].start()
                i+=1

            logging.debug("Completed creation of ip nodes threads")
            i =0
            while(i < len(thread_dictionary)):
                thread_dictionary[ip_nodes[i]] = thread_dictionary[ip_nodes[i]].join()
                i+=1

            error_message_dict = {}
            logging.debug("Checking the entry of the return values of the thread.")
            i =0 
            while(i < len(thread_dictionary)):
                result_from_thread = thread_dictionary[ip_nodes[i]]
                logging.debug(f"Nokia ===> {ip_nodes[i]} ===> {result_from_thread =}")
                
                if(result_from_thread == None):
                    logging.error(f"Result from thread for {ip_nodes[i]} ==> {result_from_thread}")
                    raise CustomException("Exception Occurred!", "Could not parse data!")
                
                if(isinstance(result_from_thread,dict)):
                    error_message_dict[ip_nodes[i]] = result_from_thread
                
                if(isinstance(result_from_thread,str)):
                    if(result_from_thread == 'Unsuccessful'):
                        error_message_dict[ip_nodes[i]] = "Could Not Parse the data for Specific Template Checks"
                    else:
                        error_message_dict[ip_nodes[i]] = result_from_thread
                
                i+=1
            
            """
                error_message_dict = {
                    node_ip : {
                        Section : { reasons : [list of serial numbers with error in template checks]}
                    }
                }
            """
            
            if(len(error_message_dict) > 0):
                error_folder = os.path.join(os.path.join(parent_folder,"Error_Folder"),"Design_Input_Checks_Results")
                Path(error_folder).mkdir(exist_ok= True, parents=True)
                
                logging.debug(f"Creating the folder for Template checks namely for Nokia template checks\n{error_folder}")
                error_file = os.path.join(error_folder,"Nokia_Nodes_Design_Input_Checks_Error.txt")

                """
                    error_message = "<================<<Errors Found in Template checks of "Nokia" Vendor Design Input sheet workbook>>================>
                                    Node IP : 'x.x.x.x'
                                    'Section'
                                    'Reason for 'S.No.' ==>> a, b, c, .........
                                    
                                    'Section'
                                    .......................................'"
                """
                logging.debug(f"Got the error_message_dict =====>{error_message_dict}\n")
                error_message = "<================<<Design Input Errors Observed in Below Uploaded Nodes for \"Nokia\" Vendor>>================>"
                
                node_ips = list(error_message_dict.keys())

                logging.debug(f"Node ips with errors ======>\n{node_ips}")
                
                i = 0
                while(i < len(node_ips)):
                    sections = list(error_message_dict[node_ips[i]].keys())
                    error_message = f"{error_message}\nNode IP : \"{node_ips[i]}\""
                    j = 0
                    while(j < len(sections)):
                        error_message = f"{error_message}\nSection : \'{sections[j]}\'" 
                        reasons = list(error_message_dict[node_ips[i]][sections[j]].keys())
                        k = 0 
                        while(k < len(reasons)):
                            reason = reasons[k]
                            sr_no_list = error_message_dict[node_ips[i]][sections[j]][reason]
                            
                            if(reason.endswith(")")):
                                error_message = f"{error_message}\n\t{k+1}.) {reason} ==>> {', '.join(str(element) for element in sr_no_list)}"
                            
                            else:
                                error_message = f"{error_message}\n\t{k+1}.) {reason} for \'S.No.\' ==>> ({', '.join(str(int(element)) for element in sr_no_list)})"
                            k+=1
                        
                        error_message = f"{error_message}\n"
                        j+=1
                    error_message = f"{error_message}\n\n"

                    i+=1

                with open(error_file,'w') as f:
                    f.write(error_message)
                    f.close()
                

                raise CustomException('Wrong Input for Uploaded Template!',f"Section-wise Wrong Input observed in uploaded 'Design Input Sheet' for node ips :\n\n({', '.join(element for element in node_ips)})\n\nPlease Check the Error Input File \'Template_Checks_error_Vendor_wise.txt\' for further details!")

                
    
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

# nokia_main_func(log_file = r"C:/Ericsson_Application_Logs/CLI_Automation_Logs/Test_File.log", parent_folder = r"C:/Users/emaienj/Downloads/VPLS_CLI_Design_Documents/VPLS_CLI_Design_Documents")