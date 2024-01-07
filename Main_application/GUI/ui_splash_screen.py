# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splash_screennOGuXs.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QProgressBar, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import Application_GUI_rc

class Ui_splash_screen(object):
    def __init__(self):
        self.label_3_text='loading......'
    
    def setupUi(self, splash_screen):
        if not splash_screen.objectName():
            splash_screen.setObjectName(u"splash_screen")
        splash_screen.resize(640, 365)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(splash_screen.sizePolicy().hasHeightForWidth())
        splash_screen.setSizePolicy(sizePolicy)
        splash_screen.setMaximumSize(QSize(640, 480))
        icon = QIcon()
        icon.addFile(u":/Main_Application_window/ericsson-blue-icon-logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        splash_screen.setWindowIcon(icon)
        splash_screen.setStyleSheet(u"#splash_screen{\n"
"	background-image: url(:/Main_Application_window/wp3610575-automation-wallpapers-1080x675-copy.png);\n"
"}")
        self.gridLayout_2 = QGridLayout(splash_screen)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame = QFrame(splash_screen)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"#frame{\n"
"background:transparent;}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"#frame{\n"
"background:transparent;\n"
"}")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"#label_3{\n"
"color:white;\n"
"text-align:center;\n"
"}")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.progressBar = QProgressBar(self.frame_2)
        self.progressBar.setObjectName(u"progressBar")
        font = QFont()
        font.setKerning(True)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet(u"#progressBar{\n"
"border-style:none;\n"
"border-radius:8px;\n"
"text-align:center;\n"
"color:rgb(2,2,2);\n"
"}\n"   
"\n"
"#progressBar::chunk{\n"
"border-top-left-radius:8px;\n"
"border-top-right-radius:8px;\n"
"border-bottom-right-radius:8px;\n"
"border-bottom-left-radius:8px;\n"
"	background-color: qlineargradient(spread:pad, x1:0.0738636, y1:0.585227, x2:0.914773, y2:0.5625, stop:0 rgba(0, 170, 0, 255), stop:1 rgba(170, 255, 0, 255));\n"
"}")
        self.progressBar.setValue(10)

        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"Ericsson Hilda"])
        font1.setPointSize(24)
        font1.setWeight(QFont.ExtraBold)
        font1.setItalic(False)
        font1.setUnderline(True)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"#label{\n"
"color:white;\n"
"background:transparent;\n"
"	font: 800 24pt \"Ericsson Hilda\";\n"
"}")
        self.label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"#label_2{\n"
"color:white;\n"
"background:transparent;\n"
"	font: 700 18pt \"Ericsson Hilda\";\n"
"}")
        self.label_2.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.verticalSpacer_4 = QSpacerItem(20, 46, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_4)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 54, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_2, 0, 0, 3, 3)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(splash_screen)

        QMetaObject.connectSlotsByName(splash_screen)
    # setupUi

    def retranslateUi(self, splash_screen):
        # Using pixmap to set the background of the QWidget Main_Application_Window
        pixmap = QPixmap(":/Main_Application_window/wp3610575-automation-wallpapers-1080x675-copy.png")
        palette = QPalette()
        palette.setBrush(QPalette.Window, pixmap)
        splash_screen.setPalette(palette)
        
        
        splash_screen.setWindowTitle(QCoreApplication.translate("splash_screen", u"CLI Automation", None))
        self.label_3.setText(QCoreApplication.translate("splash_screen", self.label_3_text, None))
        self.progressBar.setFormat("")
        self.label.setText(QCoreApplication.translate("splash_screen", u"MPBN CLI Automation", None))
        self.label_2.setText(QCoreApplication.translate("splash_screen", u"Welcome!", None))
    # retranslateUi

