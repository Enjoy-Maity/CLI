from tkinter import messagebox

class CustomException(Exception):
    def __init__(self,title,msg):
        self.title = title
        self.message = msg
        super().__init__()
        messagebox.showerror(self.title, self.message)