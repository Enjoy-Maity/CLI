# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splash_screenvrFvfY.ui'
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
    QProgressBar, QSizePolicy, QVBoxLayout, QWidget)
import Application_GUI_rc

class Ui_splash_screen(object):
    def setupUi(self, splash_screen):
        if not splash_screen.objectName():
            splash_screen.setObjectName(u"splash_screen")
        splash_screen.resize(640, 480)
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
        self.progressBar = QProgressBar(splash_screen)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(70, 290, 531, 23))
        font = QFont()
        font.setKerning(True)
        self.progressBar.setFont(font)
        self.progressBar.setValue(10)
        self.frame = QFrame(splash_screen)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(30, 30, 591, 221))
        self.frame.setStyleSheet(u"#frame{\n"
"background:transparent;\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.frame)
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

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"#label_2{\n"
"color:white;\n"
"background:transparent;\n"
"	font: 700 18pt \"Ericsson Hilda\";\n"
"}")
        self.label_2.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.verticalLayout.addWidget(self.label_2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(splash_screen)

        QMetaObject.connectSlotsByName(splash_screen)
    # setupUi

    def retranslateUi(self, splash_screen):
        splash_screen.setWindowTitle(QCoreApplication.translate("splash_screen", u"CLI Automation", None))
        self.progressBar.setFormat("")
        self.label.setText(QCoreApplication.translate("splash_screen", u"MPBN Nokia CLI Automation", None))
        self.label_2.setText(QCoreApplication.translate("splash_screen", u"Welcome!", None))
    # retranslateUi

