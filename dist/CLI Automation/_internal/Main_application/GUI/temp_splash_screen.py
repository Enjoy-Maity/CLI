from PySide6.QtWidgets import QSplashScreen, QProgressBar, QLabel
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPixmap, QColor, QFont
import GUI.Application_GUI_rc


class Splash_screen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(":/Main_Application_window/wp3610575-automation-wallpapers-1080x675-copy.png")
        super().__init__(pixmap)
        self.setMask(pixmap.mask())
        self.showMessage("loading....",Qt.AlignmentFlag(Qt.AlignBottom|Qt.AlignLeft), QColor(255,255,255,255))
        self.setGeometry(360,150,500,400)
        self.label_3_text = ''
        font_1 = QFont()
        font_1.setFamily("Ericsson Hilda")
        font_1.setWeight(QFont.ExtraBold)
        font_1.setUnderline(True)
        font_1.setPointSize(24)
        font_1.setItalic(False)
        
        self.label = QLabel(self)
        self.label.setText("MPBN CLI Automation")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font_1)
        self.label.setGeometry(30,20,450,200)
        
        
        self.label.setStyleSheet(u"color:white;")
        
        font_2 = QFont()
        font_2.setFamily("Ericsson Hilda")
        font_2.setBold(True)
        font_2.setPointSize(18)
        self.label_2 = QLabel(self)
        self.label_2.setText("Welcome")
        self.label_2.setFont(font_2)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setGeometry(30,65,450,200)
        
        self.label_2.setStyleSheet(u"color:white;")
        
        font_3 = QFont()
        font_3.setFamily("Ericsson Hilda")
        font_3.setPointSize(10)
        
        self.label_3 = QLabel(self)
        self.label_3.setText(self.label_3_text)
        self.label_3.setFont(font_3)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setGeometry(30,140,450,200)
        self.label_3.setStyleSheet(u"color:white;")
        
        self.progressBar = QProgressBar(self)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(50,250,400,20)
    
    def message(self,counter:int, label_text:str) -> None:
        """Updates the Label text

        Args:
            counter (int): _description_ : sets ProgressBar value
            label_text (str): _description_ : sets the Splash Screen label
        """
        self.counter = counter
        self.label_3.setText(label_text)
        self.progressBar.setValue(counter)
        if(counter < 60):
            self.progressBar.setStyleSheet(u"#progressBar{\n"
                                       "    color:rgb(0,0,0);\n"
                                       "text-align:center;\n"
                                       "border-style:none;"
                                       "border-radius:8px;\n"
                                       "}\n"
                                       "\n"
                                       "#progressBar::chunk{\n"
                                       "border-radius:8px;\n"
                                       "background-color: qlineargradient(spread:pad, x1:0.0738636, y1:0.585227, x2:0.914773, y2:0.5625, stop:0 rgba(0, 170, 0, 255), stop:1 rgba(170, 255, 0, 255));\n"
                                       "}")
        if(counter >= 60):
            self.progressBar.setStyleSheet(u"#progressBar{\n"
                                       "color:rgb(255,255,255);\n"
                                       "text-align:center;\n"
                                       "border-style:none;"
                                       "border-radius:8px;\n"
                                       "}\n"
                                       "\n"
                                       "#progressBar::chunk{\n"
                                       "border-radius:8px;\n"
                                       "background-color: qlineargradient(spread:pad, x1:0.0738636, y1:0.585227, x2:0.914773, y2:0.5625, stop:0 rgba(0, 170, 0, 255), stop:1 rgba(170, 255, 0, 255));\n"
                                       "}")
        self.showMessage("loading.....",Qt.AlignmentFlag(Qt.AlignBottom|Qt.AlignLeft), QColor(255,255,255,255))
    
    def finish_(self):
        super().finish(self)
        self.close()

# import sys
# import time
# from PySide6.QtWidgets import QApplication
# app = QApplication(sys.argv)
# window = Splash_screen()
# window.show()

# i = 0
# while(i <= 100):
#     if(i == 50):
#         i+=10
#     window.message(counter=i, label_text= f"Checking {i}")
#     time.sleep(1.5)
#     i+=10

# window.close()
# sys.exit()
# app.exec()