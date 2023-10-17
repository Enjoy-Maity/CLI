import sys
import os
# Getting the parent directory of the folder
# parent_directory = str(Path(__file__).resolve().parents[1])
#or
parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_directory)   #Adding the parent in system path

# sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import Custom_Exception as ce 

try:
    raise ce.CustomException("Test Title","Test message")

except ce.CustomException:
    pass