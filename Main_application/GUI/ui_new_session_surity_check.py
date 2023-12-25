# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_session_surity_checkLlUBkv.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QPushButton, QSizePolicy, QTextEdit, QWidget)
import Application_GUI_rc

class Ui_surity_Dialog(object):
    def setupUi(self, surity_Dialog):
        if not surity_Dialog.objectName():
            surity_Dialog.setObjectName(u"surity_Dialog")
        surity_Dialog.resize(500, 150)
        surity_Dialog.setMinimumSize(QSize(500, 150))
        surity_Dialog.setMaximumSize(QSize(500, 150))
        icon = QIcon()
        icon.addFile(u":/Main_Application_window/ericsson-blue-icon-logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        surity_Dialog.setWindowIcon(icon)
        surity_Dialog.setStyleSheet(u"background-image: url(:/Main_Application_window/wp3610575-automation-wallpapers.png);")
        self.gridLayout = QGridLayout(surity_Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.yes_pushButton = QPushButton(surity_Dialog)
        self.yes_pushButton.setObjectName(u"yes_pushButton")
        self.yes_pushButton.setMinimumSize(QSize(200, 33))
        self.yes_pushButton.setMaximumSize(QSize(60, 30))
        self.yes_pushButton.setStyleSheet(u"#yes_pushButton{\n"
"border:1px solid;\n"
"color:white;\n"
"border-radius:8px;\n"
"border-color:rgb(255,255,255);\n"
"font: 12pt \"Ericsson Hilda\";\n"
"background:solid;\n"
"}\n"
"#yes_pushButton:hover{\n"
"background:solid;\n"
"background-color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(255, 255, 255) solid;\n"
"border:1px solid;\n"
"color:rgb(1, 67, 167);\n"
"border-radius:8px;\n"
"border-color:rgb(1, 67, 167);\n"
"font: 700 12pt \"Ericsson Hilda\";\n"
"}\n"
"#yes_pushButton:pressed{\n"
"background:solid;\n"
"background-color:rgb(190, 190, 190);\n"
"	font: 800 12pt \"Ericsson Hilda\";\n"
"}")

        self.horizontalLayout.addWidget(self.yes_pushButton)

        self.no_pushButton = QPushButton(surity_Dialog)
        self.no_pushButton.setObjectName(u"no_pushButton")
        self.no_pushButton.setMinimumSize(QSize(200, 33))
        self.no_pushButton.setMaximumSize(QSize(60, 30))
        self.no_pushButton.setAutoFillBackground(False)
        self.no_pushButton.setStyleSheet(u"#no_pushButton{\n"
"border: 1px solid;\n"
"border-radius:8px;\n"
"border-color:white;\n"
"color:white;\n"
"	font: 12pt \"Ericsson Hilda\";\n"
"background:solid;\n"
"}\n"
"\n"
"#no_pushButton:hover{\n"
"background-color: white;\n"
"border: 1px solid;\n"
"border-radius:8px;\n"
"color:rgb(1, 67, 167);\n"
"border-color:rgb(1, 67, 167);\n"
"	font: 700 12pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#no_pushButton:pressed{\n"
"background:solid;\n"
"background-color:rgb(190, 190, 190);\n"
"	font: 800 12pt \"Ericsson Hilda\";\n"
"}")

        self.horizontalLayout.addWidget(self.no_pushButton)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)

        self.messagetextEdit = QTextEdit(surity_Dialog)
        self.messagetextEdit.setObjectName(u"messagetextEdit")
        self.messagetextEdit.setStyleSheet(u"#messagetextEdit{color:white;\n"
"background:transparent;\n"
"border:none;}")
        self.messagetextEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.messagetextEdit, 0, 0, 1, 1)


        self.retranslateUi(surity_Dialog)

        QMetaObject.connectSlotsByName(surity_Dialog)
    # setupUi

    def retranslateUi(self, surity_Dialog):
        surity_Dialog.setWindowTitle(QCoreApplication.translate("surity_Dialog", u"Are you Sure?", None))
        self.yes_pushButton.setText(QCoreApplication.translate("surity_Dialog", u"Yes", None))
        self.no_pushButton.setText(QCoreApplication.translate("surity_Dialog", u"No", None))
        self.messagetextEdit.setHtml(QCoreApplication.translate("surity_Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Ericsson Hilda'; font-size:12pt;\">Are you sure you want to create a </span><span style=\" font-family:'Ericsson Hilda'; font-size:12pt; font-weight:700;\">New Session</span><span style=\" font-family:'Ericsson Hilda'; font-size:12pt;\">?</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-bl"
                        "ock-indent:0; text-indent:0px;\"><span style=\" font-family:'Ericsson Hilda'; font-size:12pt;\">Press &quot;</span><span style=\" font-family:'Ericsson Hilda'; font-size:12pt; font-weight:700;\">Yes</span><span style=\" font-family:'Ericsson Hilda'; font-size:12pt;\">&quot; for </span><span style=\" font-family:'Ericsson Hilda'; font-size:12pt; font-weight:700;\">New Session</span><span style=\" font-family:'Ericsson Hilda'; font-size:12pt;\">.</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Ericsson Hilda'; font-size:12pt;\">Press &quot;</span><span style=\" font-family:'Ericsson Hilda'; font-size:12pt; font-weight:700;\">No</span><span style=\" font-family:'Ericsson Hilda'; font-size:12pt;\">&quot; to go back.</span></p></body></html>", None))
    # retranslateUi

