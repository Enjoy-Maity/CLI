# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_Application_GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QWidget)
import Icons_rc

class Ui_CLI_Automation_Main_Window(object):
    def setupUi(self, CLI_Automation_Main_Window):
        if not CLI_Automation_Main_Window.objectName():
            CLI_Automation_Main_Window.setObjectName(u"CLI_Automation_Main_Window")
        CLI_Automation_Main_Window.resize(1080, 650)
        CLI_Automation_Main_Window.setMinimumSize(QSize(1080, 650))
        CLI_Automation_Main_Window.setMaximumSize(QSize(1080, 650))
        font = QFont()
        font.setFamilies([u"Ericsson Hilda"])
        font.setPointSize(12)
        CLI_Automation_Main_Window.setFont(font)
        icon = QIcon()
        icon.addFile(u":/Main_Application_UI/Images/ericsson-blue-icon-logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        CLI_Automation_Main_Window.setWindowIcon(icon)
        CLI_Automation_Main_Window.setAutoFillBackground(False)
        CLI_Automation_Main_Window.setStyleSheet(u"background-image: url(:/Main_Application_UI/Images/MPBN PLANNING TASK_3_3.png) 0,0,0,0 stretch stretch;\n"
"")
        self.gridLayout = QGridLayout(CLI_Automation_Main_Window)
        self.gridLayout.setObjectName(u"gridLayout")

        self.retranslateUi(CLI_Automation_Main_Window)

        QMetaObject.connectSlotsByName(CLI_Automation_Main_Window)
    # setupUi

    def retranslateUi(self, CLI_Automation_Main_Window):
        CLI_Automation_Main_Window.setWindowTitle(QCoreApplication.translate("CLI_Automation_Main_Window", u"CLI Automation", None))
    # retranslateUi

