import logging
import traceback
import os
# import multiprocessing
from Custom_Exception import CustomException
from tkinter import messagebox

flag = ""


def main_func(**kwargs) -> str:
    """
    Main method to call the vendor-wise cli preparation
    :param kwargs: dictionary containing the key-word arguments from the main GUI Method
                    kwargs --> {'vendor_selected': str}
    :return: str : string communicating the execution status as 'Successful' or 'Unsuccessful'
    """
    global flag
    print(kwargs)
    vendor_selected = kwargs['vendor_selected']

    try:

        if vendor_selected.strip().upper() == 'NOKIA':
            design_input_file = ""
            print(vendor_selected)
            from Nokia.Nokia_CLI_Preparation import main_func
            flag = main_func()

        if vendor_selected.strip().upper() == 'ERICSSON':
            pass

        if vendor_selected.strip().upper() == 'HUAWEI':
            pass

        if vendor_selected.strip().upper() == 'CISCO':
            pass

    except PermissionError as e:
        logging.error(f"Permission Error occurred!\n{traceback.format_exc()}\n{str(e)}")
        flag = 'Unsuccessful'
        messagebox.showerror(title="Permission Error!",
                             message=str(e))

    except CustomException as e:
        logging.error(f"CustomException Occurred!\n{traceback.format_exc()}\n\ttitle-->{type(e)}\n\t\tmessage-->{str(e)}")
        flag = 'Unsuccessful'

    except Exception as e:
        logging.error(f"{traceback.format_exc()}\n\tException Occurred!===>\nTitle==>{type(e)}\n\t\tMessage==>{str(e)}")
        flag = 'Unsuccessful'
        messagebox.showerror(title="Exception Occurred!",
                             message=str(e))

    finally:
        logging.info(f"Returning the status {flag}")
        logging.shutdown()
        return flag
