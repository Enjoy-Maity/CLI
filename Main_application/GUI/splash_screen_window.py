import sys
from ui_splash_screen import Ui_splash_screen
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import QMainWindow, QApplication

class Splash_screen(QMainWindow):
    def __init__(self,main_window):
        QMainWindow.__init__(self)
        self.main_window = main_window
        self.ui = Ui_splash_screen()
        self.ui.setupUi(self)
        
        ## Removing the Title Bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        
        ## Qtimer ===> start
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        
        # Timer in milliseconds
        self.timer.start(35)
        self.counter = 0
    
    def progress(self):
        self.ui.progressBar.setValue(self.counter)
        
        # Set Value to Progress Bar
        if(self.counter > 100):
            # Stop Timer
            self.timer.stop()
        self.counter+=1
