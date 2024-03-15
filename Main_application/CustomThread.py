# Importing Thread Class
from threading import Thread
from Custom_Exception import CustomException
import logging
from tkinter import messagebox
from PySide6.QtCore import QThread, Signal


# Defining CustomThread, because the original class doesn't return anything.
class CustomThread(Thread):
    def __init__(self,
                 group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        """
        :type args: tuple
        :type kwargs: dict
        """
        Thread.__init__(self, group, target, name, args, kwargs)
        # self._target = None
        self._returnValue = None  # variable returning value after executing

    def run(self):
        # try:
        if self._target is not None:
            self._returnValue = self._target(*self._args, **self._kwargs)
        # except Exception as e:
        #     logging.error(f"Got Exception '{type(e)}' in {str(e)}")
        #     messagebox.showerror(title=str(type(e)),
        #                          message=str(e))

    def join(self) -> object | int | float | str | list | dict | set | tuple:
        Thread.join(self)
        return self._returnValue

class WorkerProcess:
    def wrapper_method(self, *args):
        self._args =  args
        self._kwargs = {}
        self._neo_args = ()
        self.return_value = None
        
        if len(self._args) > 0:
            self._target = self._args[0]
            
            if len(self._args) == 2:
                if isinstance(args[1], dict):
                    self._kwargs = self._args[1]
                
                    self.return_value = self._target(**self._kwargs)
                
                else:
                    self._neo_args = self._args[1]
                    self.return_value = self._target(*self._neo_args)
            
            if len(self._args) == 3:
                
                i = 1
                while i <= 2:
                    if isinstance(self._args[i], dict):
                        self._kwargs = self._args[i]
                        
                    if isinstance(self._args[i], (list, tuple)):
                        self._neo_args = tuple(self._args[i])
                        
                    i += 1
                    
                self.return_value = self._target(*self._neo_args, **self._kwargs)
                
            return self.return_value
            
        else:
            return None

class CustomQthread(QThread):
    finished_signal = Signal(object)

    def __init__(self,
                 target=None, args=(), kwargs={}):
        super().__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self._returnValue = ''

    def run(self):
        if len(self.args) > 0:
            self._returnValue = self.target(*self.args)

        if len(self.kwargs) > 0:
            self._returnValue = self.target(**self.kwargs)

        self.finished_signal.emit(self._returnValue)
        self.finished.connect(self.quit)
        self.exec()
        # self.quit()

    # def get_result(self):
    #     self.wait()
    #     return self._returnValue

# class Worker(QObject):
#     def __init__(self):
#         super().__init__()
#
#     @Slot
#     def long_running_task(self, input):
