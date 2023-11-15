from pathlib import Path
import sys
import os
import logging
import pickle
import importlib
import traceback
# Getting the parent directory of the folder
# parent_directory = str(Path(__file__).resolve().parents[1])
#or
parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_directory)   #Adding the parent in system path

# sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Custom_Exception import CustomException
from CustomThread import CustomThread

flag = ''
section_dictionary = {
    'VPLS-1' : importlib.import_module('Nokia_Section_Template.VPLS_1'),
    'VPLS-2' : importlib.import_module('Nokia_Section_Template.VPLS_2')
}

def section_wise_input(dictionary: dict, ip_node: str) -> dict:
    sections = list(dictionary.keys())
    thread_dictionary = {}
    i = 0
    while(i < len(sections)):
        if(len(dictionary[sections[i]])> 0):
            module_to_be_called = section_dictionary[sections[i]]
            thread_dictionary[sections[i]] = CustomThread(target=module_to_be_called.main_func,
                                args=(dictionary[sections[i]],ip_node))
            thread_dictionary[sections[i]].daemon = True
            thread_dictionary[sections[i]].start()
        i+=1
    
    thread_result_dictionary = {}
    i = 0
    while(i < len(sections)):
        temp_flag = ''
        try:
            thread_result_dictionary[sections[i]] = thread_dictionary[sections[i]].join()
        
        except ImportError as e:
            temp_flag = 'Unsuccessful'
            logging.error(f"ImportError Occurred!======>\n\n{traceback.format_exc()}{e}")
            # messagebox.showerror("Exception Occurred!",e)

        except Exception as e:
            temp_flag = 'Unsuccessful'
            logging.error(f"Exception Occured!======>\n\n{traceback.format_exc()}{e}")
            # messagebox.showerror("Exception Occurred!",e)
        
        if(temp_flag == 'Unsuccessful'):
            thread_result_dictionary[sections[i]] = "Unsuccessful"
        i+=1

    return thread_result_dictionary


def nokia_main_func(**kwargs) -> str:
    """
        Performs the Template Checks for Sections pertaining to 'Nokia' vendor

        Arguments : (**kwargs) ==> arguments in a dictionary
            kwargs ==> 'log_file' : str
                            description =====> path of file containing logs for the module
        
        return flag
            flag : str
                description =====> contains 'Unsuccessful' or 'Successful' string corresponding the status of execution completion
    
    """
    log_file = kwargs['log_file']
    logging.basicConfig(filename=log_file,
                        filemode="a",
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt='%d-%b-%Y %I:%M:%S %p',
                        encoding= "UTF-8",
                        level=logging.DEBUG)

    try:
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
                logging.debug(f"Nokia ===> {ip_nodes[i]} ===> {result_from_thread}")
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
            
            error_message = 'f'
            if(len(error_message_dict) > 0):
                pass
        
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

# main_func(filename="Test File")