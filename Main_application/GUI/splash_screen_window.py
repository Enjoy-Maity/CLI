from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QMainWindow
from GUI.ui_splash_screen import Ui_splash_screen

class Splash_screen(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_splash_screen()
        self.ui.__init__()
        # self.setCentralWidget(self.ui)
        
        self.ui.setupUi(self)
        
        
        ## Removing the Title Bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        
        # Qtimer ===> start
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.progress)
        
        # # Timer in milliseconds
        # self.timer.start(35)
        self.counter = 0
    
    def progress(self):
        self.ui.progressBar.setValue(self.counter)
        
        # Set Value to Progress Bar
        if(self.counter >= 100):
            
            # Stop Timer
            # self.timer.stop()
            self.close()
        # self.counter+=1

# from PySide6.QtWidgets import QApplication
# import sys
# app = QApplication(sys.argv)
# window = Splash_screen()
# window.show()
# sys.exit(app.exec())