from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QMainWindow
from ui_splash_screen import Ui_splash_screen

class Splash_screen(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.splash_screen_ui = Ui_splash_screen()
        
        self.splash_screen_ui.setupUi(self)
    
    def message(self, message, value):
        self.splash_screen_ui.label_3_text = message
        self.splash_screen_ui.progressBar.setValue(value)
    
    # def finish(self):
    #     self.close()

from PySide6.QtWidgets import QApplication
import sys
import time
app = QApplication(sys.argv)
window = Splash_screen()
window.show()

i = 0
while(i <= 100):
    window.message(message= f"loading -> {i}",
                   value=i)
    time.sleep(1.5)
    i += 10
window.close()
sys.exit(app.exec())