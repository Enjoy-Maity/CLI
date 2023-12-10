import os
import sys

def starter_func() -> None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from Custom_Exception import CustomException
    from CustomThread import CustomThread
    
    global CustomException; CustomException = CustomException()
    global CustomThread; CustomThread = CustomThread()
    