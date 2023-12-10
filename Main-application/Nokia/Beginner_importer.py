import os
import sys

def start_func():
    parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(parent_directory)   #Adding the parent in system path
    from Custom_Exception import CustomException
    from CustomThread import CustomThread
    
    global CustomException; CustomException = CustomException
    global CustomThread; CustomThread = CustomThread