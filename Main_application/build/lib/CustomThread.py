# Importing Thread Class
from threading import Thread


# Defining CustomThread, because the original class doesn't return anything.
class CustomThread(Thread):
    def __init__(self,
                 group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        # self._target = None
        self._returnvalue = None  # variable returning value after executing

    def run(self):
        if (self._target is not None):
            self._returnvalue = self._target(*self._args, **self._kwargs)

    def join(self) -> object:
        Thread.join(self)
        return self._returnvalue
