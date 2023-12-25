# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_start_dialog_boxxPWSbP.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QPushButton, QSizePolicy, QTextEdit,
    QWidget)
import Application_GUI_rc

class Ui_application_start_dialog(object):
    def setupUi(self, application_start_dialog):
        if not application_start_dialog.objectName():
            application_start_dialog.setObjectName(u"application_start_dialog")
        application_start_dialog.resize(640, 291)
        application_start_dialog.setMinimumSize(QSize(640, 291))
        font = QFont()
        font.setFamilies([u"Ericsson Hilda"])
        application_start_dialog.setFont(font)
        icon = QIcon()
        icon.addFile(u":/Main_Application_window/ericsson-blue-icon-logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        application_start_dialog.setWindowIcon(icon)
        application_start_dialog.setStyleSheet(u"background-image: url(:/Main_Application_window/wp3610575-automation-wallpapers-1080x675-copy.png);")
        self.gridLayout = QGridLayout(application_start_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_for_dialog = QFrame(application_start_dialog)
        self.frame_for_dialog.setObjectName(u"frame_for_dialog")
        self.frame_for_dialog.setFrameShape(QFrame.StyledPanel)
        self.frame_for_dialog.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_for_dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.textEdit = QTextEdit(self.frame_for_dialog)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(0, 121))
        font1 = QFont()
        font1.setFamilies([u"Ericsson Hilda"])
        font1.setPointSize(24)
        font1.setBold(False)
        font1.setItalic(False)
        self.textEdit.setFont(font1)
        self.textEdit.setStyleSheet(u"#textEdit{color: rgb(255, 255, 255);\n"
"background:transparent;\n"
"border:none;}\n"
"")
        self.textEdit.setReadOnly(True)

        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_for_dialog, 0, 0, 1, 1)

        self.frame_for_button = QFrame(application_start_dialog)
        self.frame_for_button.setObjectName(u"frame_for_button")
        self.frame_for_button.setStyleSheet(u"#frame_for_button{\n"
"background:transparent;}")
        self.frame_for_button.setFrameShape(QFrame.StyledPanel)
        self.frame_for_button.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_for_button)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.message_horizontalLayout = QHBoxLayout()
        self.message_horizontalLayout.setObjectName(u"message_horizontalLayout")
        self.existing_session_push_button = QPushButton(self.frame_for_button)
        self.existing_session_push_button.setObjectName(u"existing_session_push_button")
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        gradient = QLinearGradient(0, 0, 1, 0.00568182)
        gradient.setSpread(QGradient.PadSpread)
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient.setColorAt(0, QColor(0, 84, 211, 235))
        gradient.setColorAt(1, QColor(0, 84, 211, 228))
        brush1 = QBrush(gradient)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        gradient1 = QLinearGradient(0, 0, 1, 0.00568182)
        gradient1.setSpread(QGradient.PadSpread)
        gradient1.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient1.setColorAt(0, QColor(0, 84, 211, 235))
        gradient1.setColorAt(1, QColor(0, 84, 211, 228))
        brush2 = QBrush(gradient1)
        palette.setBrush(QPalette.Active, QPalette.Base, brush2)
        gradient2 = QLinearGradient(0, 0, 1, 0.00568182)
        gradient2.setSpread(QGradient.PadSpread)
        gradient2.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient2.setColorAt(0, QColor(0, 84, 211, 235))
        gradient2.setColorAt(1, QColor(0, 84, 211, 228))
        brush3 = QBrush(gradient2)
        palette.setBrush(QPalette.Active, QPalette.Window, brush3)
        brush4 = QBrush(QColor(209, 209, 209, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush4)
        brush5 = QBrush(QColor(66, 66, 66, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.HighlightedText, brush5)
        brush6 = QBrush(QColor(255, 255, 255, 128))
        brush6.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush6)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        gradient3 = QLinearGradient(0, 0, 1, 0.00568182)
        gradient3.setSpread(QGradient.PadSpread)
        gradient3.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient3.setColorAt(0, QColor(0, 84, 211, 235))
        gradient3.setColorAt(1, QColor(0, 84, 211, 228))
        brush7 = QBrush(gradient3)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        gradient4 = QLinearGradient(0, 0, 1, 0.00568182)
        gradient4.setSpread(QGradient.PadSpread)
        gradient4.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient4.setColorAt(0, QColor(0, 84, 211, 235))
        gradient4.setColorAt(1, QColor(0, 84, 211, 228))
        brush8 = QBrush(gradient4)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush8)
        gradient5 = QLinearGradient(0, 0, 1, 0.00568182)
        gradient5.setSpread(QGradient.PadSpread)
        gradient5.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient5.setColorAt(0, QColor(0, 84, 211, 235))
        gradient5.setColorAt(1, QColor(0, 84, 211, 228))
        brush9 = QBrush(gradient5)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush9)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush5)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush6)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        gradient6 = QLinearGradient(0, 0, 1, 0.00568182)
        gradient6.setSpread(QGradient.PadSpread)
        gradient6.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient6.setColorAt(0, QColor(0, 84, 211, 235))
        gradient6.setColorAt(1, QColor(0, 84, 211, 228))
        brush10 = QBrush(gradient6)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        gradient7 = QLinearGradient(0, 0, 1, 0.00568182)
        gradient7.setSpread(QGradient.PadSpread)
        gradient7.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient7.setColorAt(0, QColor(0, 84, 211, 235))
        gradient7.setColorAt(1, QColor(0, 84, 211, 228))
        brush11 = QBrush(gradient7)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush11)
        gradient8 = QLinearGradient(0, 0, 1, 0.00568182)
        gradient8.setSpread(QGradient.PadSpread)
        gradient8.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient8.setColorAt(0, QColor(0, 84, 211, 235))
        gradient8.setColorAt(1, QColor(0, 84, 211, 228))
        brush12 = QBrush(gradient8)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush12)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush5)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush6)
#endif
        self.existing_session_push_button.setPalette(palette)
        font2 = QFont()
        font2.setFamilies([u"Ericsson Hilda"])
        font2.setPointSize(12)
        self.existing_session_push_button.setFont(font2)
        self.existing_session_push_button.setMouseTracking(True)
        self.existing_session_push_button.setAcceptDrops(True)
        self.existing_session_push_button.setStyleSheet(u"#existing_session_push_button{selection-color: rgb(66, 66, 66);\n"
"background:solid;\n"
"border:1px solid;\n"
"border-color:rgb(255,255,255);\n"
"color:rgb(255, 255, 255);\n"
"border-radius:8px;\n"
"height:30px;\n"
"}\n"
"#existing_session_push_button:hover{\n"
"	font: 700 12pt \"Ericsson Hilda\";\n"
"	border-color: rgb(15, 13, 125);\n"
"	color: rgb(15, 13, 125);\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"#existing_session_push_button:pressed{\n"
"	font: 800 12pt \"Ericsson Hilda\";\n"
"	border-color: rgb(15, 13, 125);\n"
"	color: rgb(15, 13, 125);\n"
"	background-color: rgb(190, 190, 190);\n"
"}")
        self.existing_session_push_button.setAutoDefault(False)
        self.existing_session_push_button.setFlat(True)

        self.message_horizontalLayout.addWidget(self.existing_session_push_button)

        self.new_session_push_button = QPushButton(self.frame_for_button)
        self.new_session_push_button.setObjectName(u"new_session_push_button")
        self.new_session_push_button.setFont(font2)
        self.new_session_push_button.setStyleSheet(u"#new_session_push_button{\n"
"selection-color: rgb(66, 66, 66);\n"
"background:solid;\n"
"border:1px solid;\n"
"border-color:rgb(255,255,255);\n"
"color:rgb(255, 255, 255);\n"
"border-radius:8px;\n"
"height:30px;}\n"
"\n"
"#new_session_push_button:hover{\n"
"	font: 700 12pt \"Ericsson Hilda\";\n"
"	border-color: rgb(15, 13, 125);\n"
"	color: rgb(15, 13, 125);\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"#new_session_push_button:pressed{\n"
"	font: 800 12pt \"Ericsson Hilda\";\n"
"	border-color: rgb(15, 13, 125);\n"
"	color: rgb(15, 13, 125);\n"
"	background-color: rgb(190, 190, 190);\n"
"}\n"
"")

        self.message_horizontalLayout.addWidget(self.new_session_push_button)


        self.gridLayout_3.addLayout(self.message_horizontalLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_for_button, 1, 0, 1, 1)


        self.retranslateUi(application_start_dialog)

        self.existing_session_push_button.setDefault(True)


        QMetaObject.connectSlotsByName(application_start_dialog)
    # setupUi

    def retranslateUi(self, application_start_dialog):
        application_start_dialog.setWindowTitle(QCoreApplication.translate("application_start_dialog", u"Existing Session Detected!", None))
        self.textEdit.setDocumentTitle(QCoreApplication.translate("application_start_dialog", u"Existing Session Detected", None))
        self.textEdit.setHtml(QCoreApplication.translate("application_start_dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><title>Existing Session Detected</title><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ericsson Hilda'; font-size:24pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Existing Session was detected! Do you want to continue with the E</span><span style=\" font-family:'Segoe UI'; font-size:12pt; font-weight:700;\">xisting Session</span><span style=\" font-family:'Segoe UI'; font-size:12pt;\"> or want to create a </span><span style=\" font-family:'Se"
                        "goe UI'; font-size:12pt; font-weight:700;\">New Session</span><span style=\" font-family:'Segoe UI'; font-size:12pt;\">?</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Press &quot;</span><span style=\" font-family:'Segoe UI'; font-size:12pt; font-weight:700;\">Existing Session</span><span style=\" font-family:'Segoe UI'; font-size:12pt;\">&quot; button to continue the existing session.</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">or</span></p>\n"
"<p align=\"center\" style=\""
                        " margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Press &quot;</span><span style=\" font-family:'Segoe UI'; font-size:12pt; font-weight:700;\">New Session</span><span style=\" font-size:12pt;\">&quot; button to start a new session.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:700;\">Note: - New Session will overwrite the 'Existing Session' Database!</span></p></body></html>", None))
        self.existing_session_push_button.setText(QCoreApplication.translate("application_start_dialog", u"Existing Session", None))
        self.new_session_push_button.setText(QCoreApplication.translate("application_start_dialog", u"New Session", None))
    # retranslateUi

