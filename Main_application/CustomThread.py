# Importing Thread Class
from threading import Thread
from Custom_Exception import CustomException
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
        if self._target is not None:
            self._returnValue = self._target(*self._args, **self._kwargs)

    def join(self) -> object:
        Thread.join(self)
        return self._returnValue


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
