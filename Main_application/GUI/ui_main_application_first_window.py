# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_application_first_windowpQKMDZ.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import Application_GUI_rc

class Ui_CLI_automation_main_application_first_window(object):
    def setupUi(self, CLI_automation_main_application_first_window):
        if not CLI_automation_main_application_first_window.objectName():
            CLI_automation_main_application_first_window.setObjectName(u"CLI_automation_main_application_first_window")
        CLI_automation_main_application_first_window.resize(1080, 675)
        CLI_automation_main_application_first_window.setMinimumSize(QSize(1080, 675))
        CLI_automation_main_application_first_window.setMaximumSize(QSize(1080, 675))
        CLI_automation_main_application_first_window.setBaseSize(QSize(1080, 650))
        icon = QIcon()
        icon.addFile(u":/Main_Application_window/ericsson-blue-icon-logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        CLI_automation_main_application_first_window.setWindowIcon(icon)
        CLI_automation_main_application_first_window.setStyleSheet(u"background-image: url(:/Main_Application_window/wp3610575-automation-wallpapers-1080x675-copy.png);")
        self.gridLayout = QGridLayout(CLI_automation_main_application_first_window)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(CLI_automation_main_application_first_window)
        self.groupBox.setObjectName(u"groupBox")
        font = QFont()
        font.setFamilies([u"Ericsson Hilda"])
        font.setPointSize(25)
        font.setBold(True)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(u"background:transparent;\n"
"color:white;")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame_2 = QFrame(self.groupBox)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(263, 62))
        self.label_4.setStyleSheet(u"margin-left:20px;\n"
"padding-right:10px;")
        self.label_4.setPixmap(QPixmap(u":/vendors_list/nokia-2023-seeklogo.com.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_4)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(205, 120))
        self.label.setBaseSize(QSize(1, 3))
        self.label.setStyleSheet(u"#label{\n"
"margin:10px;\n"
"padding-right:8px;\n"
"padding-left:12px;\n"
"}")
        self.label.setPixmap(QPixmap(u":/vendors_list/cicso-systems-seeklogo.com.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)

        self.horizontalLayout_3.addWidget(self.label)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QSize(193, 154))
        self.label_2.setSizeIncrement(QSize(0, 116))
        self.label_2.setStyleSheet(u"margin:0px;")
        self.label_2.setPixmap(QPixmap(u":/vendors_list/huawei-1.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setIndent(4)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(331, 86))
        self.label_3.setStyleSheet(u"margin-right:20px;")
        self.label_3.setPixmap(QPixmap(u":/vendors_list/Ericsson-1.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_3)


        self.gridLayout_4.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")
        font1 = QFont()
        font1.setFamilies([u"Ericsson Hilda"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_5)


        self.gridLayout_4.addLayout(self.verticalLayout, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 3, 0, 1, 1)

        self.frame = QFrame(self.groupBox)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.file_browser_verticalLayout = QVBoxLayout()
        self.file_browser_verticalLayout.setObjectName(u"file_browser_verticalLayout")
        self.selection_of_file_verticalLayout = QVBoxLayout()
        self.selection_of_file_verticalLayout.setObjectName(u"selection_of_file_verticalLayout")
        self.selection_of_file_label = QLabel(self.frame)
        self.selection_of_file_label.setObjectName(u"selection_of_file_label")
        font2 = QFont()
        font2.setFamilies([u"Ericsson Hilda"])
        font2.setPointSize(20)
        font2.setBold(True)
        self.selection_of_file_label.setFont(font2)
        self.selection_of_file_label.setStyleSheet(u"#selection_of_file_label{\n"
"padding-top:20px;\n"
"padding-bottom: 10px;\n"
"margin-left:20px;\n"
"}")
        self.selection_of_file_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.selection_of_file_verticalLayout.addWidget(self.selection_of_file_label)


        self.file_browser_verticalLayout.addLayout(self.selection_of_file_verticalLayout)

        self.file_browser_horizontalLayout = QHBoxLayout()
        self.file_browser_horizontalLayout.setSpacing(0)
        self.file_browser_horizontalLayout.setObjectName(u"file_browser_horizontalLayout")
        self.file_browser_horizontalLayout.setContentsMargins(-1, -1, -1, 10)
        self.file_browser_path_lineEdit = QLineEdit(self.frame)
        self.file_browser_path_lineEdit.setObjectName(u"file_browser_path_lineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.file_browser_path_lineEdit.sizePolicy().hasHeightForWidth())
        self.file_browser_path_lineEdit.setSizePolicy(sizePolicy1)
        self.file_browser_path_lineEdit.setMinimumSize(QSize(780, 22))
        self.file_browser_path_lineEdit.setMaximumSize(QSize(16777215, 34))
        font3 = QFont()
        font3.setFamilies([u"Ericsson Hilda"])
        font3.setPointSize(12)
        self.file_browser_path_lineEdit.setFont(font3)
        self.file_browser_path_lineEdit.setStyleSheet(u"#file_browser_path_lineEdit{border-radius:8px;\n"
"background-color:white;\n"
"margin-left:10px;\n"
"	color: rgb(35, 35, 35);\n"
"height:28px;}")
        self.file_browser_path_lineEdit.setReadOnly(True)

        self.file_browser_horizontalLayout.addWidget(self.file_browser_path_lineEdit)

        self.file_browser_pushButton = QPushButton(self.frame)
        self.file_browser_pushButton.setObjectName(u"file_browser_pushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.file_browser_pushButton.sizePolicy().hasHeightForWidth())
        self.file_browser_pushButton.setSizePolicy(sizePolicy2)
        self.file_browser_pushButton.setMinimumSize(QSize(175, 40))
        self.file_browser_pushButton.setMaximumSize(QSize(175, 40))
        self.file_browser_pushButton.setBaseSize(QSize(210, 0))
        font4 = QFont()
        font4.setFamilies([u"Ericsson Hilda"])
        font4.setPointSize(14)
        self.file_browser_pushButton.setFont(font4)
        self.file_browser_pushButton.setLayoutDirection(Qt.LeftToRight)
        self.file_browser_pushButton.setStyleSheet(u"#file_browser_pushButton{\n"
"color:white;\n"
"background:solid;\n"
"background-color: rgb(22, 15, 121);\n"
"padding:2px;\n"
"border:1px solid;\n"
"border-color: white;\n"
"border-radius:12px;\n"
"}\n"
"\n"
"#file_browser_pushButton:hover{\n"
"background-color:rgb(255,255,255);\n"
"border:1px solid;\n"
"border-color:rgb(22, 15,121 );\n"
"color:rgb(22, 15, 121);\n"
"	font: 700 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#file_browser_pushButton:pressed{\n"
"background-color:rgb(220, 220, 220);\n"
"border:1px solid;\n"
"border-color:rgb(15, 13, 125);\n"
"color:rgb(22, 15, 121);\n"
"	font: 800 14pt \"Ericsson Hilda\";\n"
"}")
        self.file_browser_pushButton.setIconSize(QSize(210, 40))
        self.file_browser_pushButton.setAutoDefault(True)

        self.file_browser_horizontalLayout.addWidget(self.file_browser_pushButton)


        self.file_browser_verticalLayout.addLayout(self.file_browser_horizontalLayout)

        self.verticalSpacer = QSpacerItem(40, 22, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.file_browser_verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout_3.addLayout(self.file_browser_verticalLayout, 0, 0, 1, 1)

        self.sheet_creator_verticalLayout = QVBoxLayout()
        self.sheet_creator_verticalLayout.setObjectName(u"sheet_creator_verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.sheet_creator_pushButton = QPushButton(self.frame)
        self.sheet_creator_pushButton.setObjectName(u"sheet_creator_pushButton")
        sizePolicy1.setHeightForWidth(self.sheet_creator_pushButton.sizePolicy().hasHeightForWidth())
        self.sheet_creator_pushButton.setSizePolicy(sizePolicy1)
        self.sheet_creator_pushButton.setMinimumSize(QSize(175, 0))
        self.sheet_creator_pushButton.setMaximumSize(QSize(175, 45))
        self.sheet_creator_pushButton.setFont(font4)
        self.sheet_creator_pushButton.setStyleSheet(u"#sheet_creator_pushButton{\n"
"color:white;\n"
"background:solid;\n"
"background-color: rgb(22, 15, 121);\n"
"padding:2px;\n"
"border:1px solid;\n"
"border-color: white;\n"
"border-radius:12px;\n"
"}\n"
"\n"
"#sheet_creator_pushButton:hover{\n"
"background-color:rgb(255,255,255);\n"
"border:1px solid;\n"
"border-color:rgb(22, 15,121 );\n"
"color:rgb(22, 15, 121);\n"
"	font: 700 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#sheet_creator_pushButton:pressed{\n"
"background-color:rgb(220, 220, 220);\n"
"border:1px solid;\n"
"border-color:rgb(15, 13, 125);\n"
"color:rgb(22, 15, 121);\n"
"	font: 800 14pt \"Ericsson Hilda\";\n"
"}")

        self.horizontalLayout.addWidget(self.sheet_creator_pushButton)

        self.horizontalSpacer_5 = QSpacerItem(225, 50, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.submit_button_pushButton = QPushButton(self.frame)
        self.submit_button_pushButton.setObjectName(u"submit_button_pushButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.submit_button_pushButton.sizePolicy().hasHeightForWidth())
        self.submit_button_pushButton.setSizePolicy(sizePolicy3)
        self.submit_button_pushButton.setMinimumSize(QSize(175, 0))
        self.submit_button_pushButton.setMaximumSize(QSize(305, 45))
        self.submit_button_pushButton.setFont(font4)
        self.submit_button_pushButton.setLayoutDirection(Qt.LeftToRight)
        self.submit_button_pushButton.setAutoFillBackground(False)
        self.submit_button_pushButton.setStyleSheet(u"#submit_button_pushButton{\n"
"color:white;\n"
"background:solid;\n"
"background-color: rgb(22, 15, 121);\n"
"padding:2px;\n"
"border:1px solid;\n"
"border-color: white;\n"
"border-radius:12px;\n"
"}\n"
"\n"
"#submit_button_pushButton:hover{\n"
"background-color:rgb(255,255,255);\n"
"border:1px solid;\n"
"border-color:rgb(22, 15,121 );\n"
"color:rgb(22, 15, 121);\n"
"	font: 700 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#submit_button_pushButton:pressed{\n"
"background-color:rgb(220, 220, 220);\n"
"border:1px solid;\n"
"border-color:rgb(15, 13, 125);\n"
"color:rgb(22, 15, 121);\n"
"	font: 800 14pt \"Ericsson Hilda\";\n"
"}")
        self.submit_button_pushButton.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.submit_button_pushButton)

        self.horizontalSpacer_4 = QSpacerItem(215, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.sheet_creator_verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(183, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.sheet_creator_status_label = QLabel(self.frame)
        self.sheet_creator_status_label.setObjectName(u"sheet_creator_status_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.sheet_creator_status_label.sizePolicy().hasHeightForWidth())
        self.sheet_creator_status_label.setSizePolicy(sizePolicy4)
        self.sheet_creator_status_label.setMinimumSize(QSize(200, 100))
        self.sheet_creator_status_label.setMaximumSize(QSize(200, 100))
        font5 = QFont()
        font5.setFamilies([u"Ericsson Hilda"])
        font5.setPointSize(16)
        font5.setBold(True)
        font5.setItalic(False)
        self.sheet_creator_status_label.setFont(font5)
        self.sheet_creator_status_label.setStyleSheet(u"#sheet_creator_status_label{\n"
"padding-bottom:30px;\n"
"margin-bottom:30px;\n"
"	font: 700 16pt \"Ericsson Hilda\";\n"
"\n"
"}")
        self.sheet_creator_status_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.sheet_creator_status_label)

        self.horizontalSpacer = QSpacerItem(590, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.sheet_creator_verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout_3.addLayout(self.sheet_creator_verticalLayout, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)
        self.label_6.setStyleSheet(u"#label_6{\n"
"margin-left:20px;\n"
"}")

        self.horizontalLayout_4.addWidget(self.label_6)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)


        self.retranslateUi(CLI_automation_main_application_first_window)

        QMetaObject.connectSlotsByName(CLI_automation_main_application_first_window)
    # setupUi

    def retranslateUi(self, CLI_automation_main_application_first_window):
        CLI_automation_main_application_first_window.setWindowTitle(QCoreApplication.translate("CLI_automation_main_application_first_window", u"CLI Automation", None))
        self.groupBox.setTitle(QCoreApplication.translate("CLI_automation_main_application_first_window", u"MPBN Nokia CLI Automation", None))
        self.label_4.setText("")
        self.label.setText("")
        self.label_2.setText("")
        self.label_3.setText("")
        self.label_5.setText(QCoreApplication.translate("CLI_automation_main_application_first_window", u"MULTI VENDOR SUPPORT", None))
        self.selection_of_file_label.setText(QCoreApplication.translate("CLI_automation_main_application_first_window", u"Please Select the 'Host Details' from the file browser!", None))
        self.file_browser_path_lineEdit.setText("")
        self.file_browser_path_lineEdit.setPlaceholderText(QCoreApplication.translate("CLI_automation_main_application_first_window", u" Host Details: - ", None))
        self.file_browser_pushButton.setText(QCoreApplication.translate("CLI_automation_main_application_first_window", u"Browse", None))
        self.sheet_creator_pushButton.setText(QCoreApplication.translate("CLI_automation_main_application_first_window", u"Sheet Creator", None))
        self.submit_button_pushButton.setText(QCoreApplication.translate("CLI_automation_main_application_first_window", u"Submit", None))
        self.sheet_creator_status_label.setText(QCoreApplication.translate("CLI_automation_main_application_first_window", u"Hello", None))
        self.label_6.setText(QCoreApplication.translate("CLI_automation_main_application_first_window", u"Note:- Kindly click on 'Submit' button after 'Successful' completion of 'Sheet Creator' Task", None))
    # retranslateUi

