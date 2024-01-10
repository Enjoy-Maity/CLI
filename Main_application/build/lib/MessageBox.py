from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon
import GUI.Application_GUI_rc


class messagebox:
    def __init__(self):
        self.message = QMessageBox()
        self.message.setWindowIcon(QIcon(":/Main_Application_window/ericsson-blue-icon-logo.ico"))

    def showerror(self, title: str, message: str):
        message = str(message)
        self.message.setWindowTitle(title)
        self.message.setText(message)
        self.message.setIcon(QMessageBox.Critical)
        self.message.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.message.setDefaultButton(QMessageBox.StandardButton.Ok)
        self.message.exec()

    def showwarning(self, title: str, message: str):
        message = str(message)
        self.message.setWindowTitle(title)
        self.message.setText(message)
        self.message.setIcon(QMessageBox.Warning)
        self.message.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.message.setDefaultButton(QMessageBox.StandardButton.Ok)
        self.message.exec()

    def showinfo(self, title: str, message: str):
        message = str(message)
        self.message.setWindowTitle(title)
        self.message.setText(message)
        self.message.setIcon(QMessageBox.Information)
        self.message.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.message.setDefaultButton(QMessageBox.StandardButton.Ok)
        self.message.exec()

    def askyesno(self, title: str, message: str):
        message = str(message)
        self.message.setWindowTitle(title)
        self.message.setText(message)
        self.message.setIcon(QMessageBox.Question)
        self.message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return self.message.exec()
