# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_ApplicationJBgFjZ.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QVBoxLayout,
    QWidget)
import Application_GUI_rc

class Ui_Main_Application_Window(object):
    def setupUi(self, Main_Application_Window):
        if not Main_Application_Window.objectName():
            Main_Application_Window.setObjectName(u"Main_Application_Window")
        Main_Application_Window.resize(1080, 675)
        Main_Application_Window.setMinimumSize(QSize(1080, 675))
        Main_Application_Window.setMaximumSize(QSize(1080, 675))
        font = QFont()
        font.setFamilies([u"Ericsson Hilda"])
        font.setPointSize(12)
        Main_Application_Window.setFont(font)
        icon = QIcon()
        icon.addFile(u":/Main_Application_window/ericsson-blue-icon-logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        Main_Application_Window.setWindowIcon(icon)
        Main_Application_Window.setStyleSheet(u"background-image: url(:/Main_Application_window/wp3610575-automation-wallpapers-1080x675-copy.png);")
        self.gridLayout = QGridLayout(Main_Application_Window)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Main_Application_Window)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background:transparent;\n"
"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        font1 = QFont()
        font1.setFamilies([u"Ericsson Hilda"])
        font1.setPointSize(25)
        font1.setBold(True)
        self.groupBox.setFont(font1)
        self.groupBox.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.table_verticalLayout = QVBoxLayout()
        self.table_verticalLayout.setObjectName(u"table_verticalLayout")
        self.task_database_tableview = QTableView(self.groupBox)
        self.task_database_tableview.setObjectName(u"task_database_tableview")
        font2 = QFont()
        font2.setFamilies([u"Ericsson Hilda"])
        self.task_database_tableview.setFont(font2)
        self.task_database_tableview.setStyleSheet(u"#task_database_tableview{\n"
"color:black;\n"
"	background-color: rgb(190, 190, 190);\n"
"	alternate-background-color: rgb(210, 210, 210);\n"
"}\n"
"")
        self.task_database_tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.task_database_tableview.setDragDropMode(QAbstractItemView.InternalMove)
        self.task_database_tableview.setAlternatingRowColors(True)
        self.task_database_tableview.setSelectionMode(QAbstractItemView.NoSelection)
        self.task_database_tableview.setGridStyle(Qt.NoPen)

        self.table_verticalLayout.addWidget(self.task_database_tableview)


        self.gridLayout_3.addLayout(self.table_verticalLayout, 4, 0, 1, 1)

        self.selected_host_details_horizontal_layout = QHBoxLayout()
        self.selected_host_details_horizontal_layout.setObjectName(u"selected_host_details_horizontal_layout")
        self.selected_host_details_label = QLabel(self.groupBox)
        self.selected_host_details_label.setObjectName(u"selected_host_details_label")
        font3 = QFont()
        font3.setFamilies([u"Ericsson Hilda"])
        font3.setPointSize(16)
        font3.setBold(True)
        font3.setUnderline(True)
        self.selected_host_details_label.setFont(font3)

        self.selected_host_details_horizontal_layout.addWidget(self.selected_host_details_label)

        self.selected_host_details_line_edit = QLineEdit(self.groupBox)
        self.selected_host_details_line_edit.setObjectName(u"selected_host_details_line_edit")
        self.selected_host_details_line_edit.setMinimumSize(QSize(0, 30))
        font4 = QFont()
        font4.setFamilies([u"Ericsson Hilda"])
        font4.setPointSize(12)
        font4.setBold(True)
        self.selected_host_details_line_edit.setFont(font4)
        self.selected_host_details_line_edit.setAutoFillBackground(False)
        self.selected_host_details_line_edit.setStyleSheet(u"#selected_host_details_line_edit{\n"
"background-color: rgb(220, 220, 220);\n"
"color: rgb(124, 124, 124);\n"
"border-radius: 8px;\n"
"padding:2px;}\n"
"")
        self.selected_host_details_line_edit.setReadOnly(True)

        self.selected_host_details_horizontal_layout.addWidget(self.selected_host_details_line_edit)


        self.gridLayout_3.addLayout(self.selected_host_details_horizontal_layout, 0, 0, 1, 1)

        self.frame_for_session_buttons = QFrame(self.groupBox)
        self.frame_for_session_buttons.setObjectName(u"frame_for_session_buttons")
        self.frame_for_session_buttons.setFrameShape(QFrame.StyledPanel)
        self.frame_for_session_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_for_session_buttons)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.new_session_button = QPushButton(self.frame_for_session_buttons)
        self.new_session_button.setObjectName(u"new_session_button")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.new_session_button.sizePolicy().hasHeightForWidth())
        self.new_session_button.setSizePolicy(sizePolicy)
        self.new_session_button.setMinimumSize(QSize(1000, 40))
        self.new_session_button.setMaximumSize(QSize(1000, 40))
        self.new_session_button.setLayoutDirection(Qt.LeftToRight)
        self.new_session_button.setStyleSheet(u"#new_session_button{\n"
"color:white;\n"
"background:solid;\n"
"background-color: rgb(22, 15, 121);\n"
"padding:2px;\n"
"border:1px solid;\n"
"border-color: white;\n"
"border-radius:12px;\n"
"	font: 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#new_session_button:hover{\n"
"background-color:rgb(255,255,255);\n"
"border:1px solid;\n"
"border-color:rgb(22, 15,121 );\n"
"color:rgb(22, 15, 121);\n"
"	font: 700 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#new_session_button:pressed{\n"
"background-color:rgb(220, 220, 220);\n"
"border:1px solid;\n"
"border-color:rgb(15, 13, 125);\n"
"color:rgb(22, 15, 121);\n"
"	font: 800 14pt \"Ericsson Hilda\";\n"
"}")

        self.verticalLayout.addWidget(self.new_session_button)


        self.gridLayout_7.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_for_session_buttons, 5, 0, 1, 1)

        self.frame_for_vendor = QFrame(self.groupBox)
        self.frame_for_vendor.setObjectName(u"frame_for_vendor")
        self.frame_for_vendor.setFrameShape(QFrame.StyledPanel)
        self.frame_for_vendor.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_for_vendor)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.vendor_selection_details_horizontal_layout = QHBoxLayout()
        self.vendor_selection_details_horizontal_layout.setObjectName(u"vendor_selection_details_horizontal_layout")
        self.vendor_selection_details_horizontal_layout.setContentsMargins(-1, -1, -1, 10)
        self.vendor_details_selection_combobox = QComboBox(self.frame_for_vendor)
        self.vendor_details_selection_combobox.addItem("")
        self.vendor_details_selection_combobox.addItem("")
        self.vendor_details_selection_combobox.setObjectName(u"vendor_details_selection_combobox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.vendor_details_selection_combobox.sizePolicy().hasHeightForWidth())
        self.vendor_details_selection_combobox.setSizePolicy(sizePolicy1)
        self.vendor_details_selection_combobox.setMinimumSize(QSize(220, 30))
        self.vendor_details_selection_combobox.setMaximumSize(QSize(220, 20))
        self.vendor_details_selection_combobox.setBaseSize(QSize(200, 20))
        font5 = QFont()
        font5.setFamilies([u"Ericsson Hilda"])
        font5.setPointSize(14)
        font5.setStyleStrategy(QFont.PreferDefault)
        font5.setHintingPreference(QFont.PreferFullHinting)
        self.vendor_details_selection_combobox.setFont(font5)
        self.vendor_details_selection_combobox.setFocusPolicy(Qt.WheelFocus)
        self.vendor_details_selection_combobox.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.vendor_details_selection_combobox.setAcceptDrops(False)
        self.vendor_details_selection_combobox.setLayoutDirection(Qt.LeftToRight)
        self.vendor_details_selection_combobox.setAutoFillBackground(False)
        self.vendor_details_selection_combobox.setStyleSheet(u"#vendor_details_selection_combobox{\n"
"color:black;\n"
"border-radius:5px;\n"
"border:1px solid;\n"
"background:transparent;\n"
"	background-color: rgb(215, 215, 215);\n"
"	alternate-background-color: rgb(189, 189, 189);\n"
"}\n"
"\n"
"#vendor_details_selection_combobox::drop-down:button{\n"
"border-top-radius:5px;\n"
"border-bottom-radius:5px;\n"
"	border-image: url(:/Main_Application_window/drop-downarrow.png);\n"
"}\n"
"\n"
"#vendor_details_selection_combobox QAbstractItemView{\n"
"outline:none;\n"
"background-style:solid;\n"
"}\n"
"\n"
"#vendor_details_selection_combobox QListView{\n"
"color:black;\n"
"}\n"
"\n"
"#vendor_details_selection_combobox QListView:item{\n"
"color:black;\n"
"background-color: rgb(190, 190, 190);\n"
"}\n"
"\n"
"#vendor_details_selection_combobox QListView:item:selected{\n"
"color:black;\n"
"background-style:solid;\n"
"background-color: rgb(220, 220, 220);\n"
"outline:none;}\n"
"\n"
"")
        self.vendor_details_selection_combobox.setFrame(True)
        self.vendor_details_selection_combobox.setModelColumn(0)

        self.vendor_selection_details_horizontal_layout.addWidget(self.vendor_details_selection_combobox)


        self.gridLayout_6.addLayout(self.vendor_selection_details_horizontal_layout, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_for_vendor, 2, 0, 1, 1)

        self.sheet_Creater_status_frame = QFrame(self.groupBox)
        self.sheet_Creater_status_frame.setObjectName(u"sheet_Creater_status_frame")
        self.sheet_Creater_status_frame.setFrameShape(QFrame.StyledPanel)
        self.sheet_Creater_status_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.sheet_Creater_status_frame)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.sheet_creater_status_vertical_layout = QVBoxLayout()
        self.sheet_creater_status_vertical_layout.setObjectName(u"sheet_creater_status_vertical_layout")
        self.sheet_creater_status_button_label = QLabel(self.sheet_Creater_status_frame)
        self.sheet_creater_status_button_label.setObjectName(u"sheet_creater_status_button_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.sheet_creater_status_button_label.sizePolicy().hasHeightForWidth())
        self.sheet_creater_status_button_label.setSizePolicy(sizePolicy2)
        self.sheet_creater_status_button_label.setMinimumSize(QSize(500, 40))
        self.sheet_creater_status_button_label.setMaximumSize(QSize(500, 16777215))
        self.sheet_creater_status_button_label.setStyleSheet(u"#sheet_creater_status_button_label{\n"
"color:white;\n"
"background:solid;\n"
"background-color: rgb(22, 15, 121);\n"
"padding:2px;\n"
"border:1px solid;\n"
"border-color: white;\n"
"border-radius:12px;\n"
"	font: 14pt \"Ericsson Hilda\";\n"
"}\n"
"")
        self.sheet_creater_status_button_label.setAlignment(Qt.AlignCenter)

        self.sheet_creater_status_vertical_layout.addWidget(self.sheet_creater_status_button_label)

        self.sheet_creater_task_status_label = QLabel(self.sheet_Creater_status_frame)
        self.sheet_creater_task_status_label.setObjectName(u"sheet_creater_task_status_label")
        font6 = QFont()
        font6.setFamilies([u"Ericsson Hilda"])
        font6.setPointSize(14)
        font6.setBold(True)
        self.sheet_creater_task_status_label.setFont(font6)
        self.sheet_creater_task_status_label.setAlignment(Qt.AlignCenter)

        self.sheet_creater_status_vertical_layout.addWidget(self.sheet_creater_task_status_label)


        self.gridLayout_5.addLayout(self.sheet_creater_status_vertical_layout, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)


        self.gridLayout_3.addWidget(self.sheet_Creater_status_frame, 1, 0, 1, 1)

        self.frame_for_buttons_and_their_status = QFrame(self.groupBox)
        self.frame_for_buttons_and_their_status.setObjectName(u"frame_for_buttons_and_their_status")
        self.frame_for_buttons_and_their_status.setFrameShape(QFrame.StyledPanel)
        self.frame_for_buttons_and_their_status.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_for_buttons_and_their_status)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.buttons_and_status_vertical_status = QVBoxLayout()
        self.buttons_and_status_vertical_status.setObjectName(u"buttons_and_status_vertical_status")
        self.buttons_horizontal_layout = QHBoxLayout()
        self.buttons_horizontal_layout.setObjectName(u"buttons_horizontal_layout")
        self.template_checks_btn = QPushButton(self.frame_for_buttons_and_their_status)
        self.template_checks_btn.setObjectName(u"template_checks_btn")
        self.template_checks_btn.setMinimumSize(QSize(0, 40))
        self.template_checks_btn.setStyleSheet(u"#template_checks_btn{\n"
"color:white;\n"
"background:solid;\n"
"background-color: rgb(22, 15, 121);\n"
"padding:2px;\n"
"border:1px solid;\n"
"border-color: white;\n"
"border-radius:12px;\n"
"	font: 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#template_checks_btn:hover{\n"
"background-color:rgb(255,255,255);\n"
"border:1px solid;\n"
"border-color:rgb(22, 15,121 );\n"
"color:rgb(22, 15, 121);\n"
"	font: 700 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#template_checks_btn:pressed{\n"
"background-color:rgb(220, 220, 220);\n"
"border:1px solid;\n"
"border-color:rgb(15, 13, 125);\n"
"color:rgb(22, 15, 121);\n"
"	font: 800 14pt \"Ericsson Hilda\";\n"
"}")

        self.buttons_horizontal_layout.addWidget(self.template_checks_btn)

        self.running_config_pre_checks_btn = QPushButton(self.frame_for_buttons_and_their_status)
        self.running_config_pre_checks_btn.setObjectName(u"running_config_pre_checks_btn")
        self.running_config_pre_checks_btn.setMinimumSize(QSize(260, 40))
        self.running_config_pre_checks_btn.setMaximumSize(QSize(260, 16777215))
        font7 = QFont()
        font7.setFamilies([u"Ericsson Hilda"])
        font7.setPointSize(14)
        font7.setBold(False)
        font7.setItalic(False)
        self.running_config_pre_checks_btn.setFont(font7)
        self.running_config_pre_checks_btn.setStyleSheet(u"#running_config_pre_checks_btn{\n"
"color:white;\n"
"background:solid;\n"
"background-color: rgb(22, 15, 121);\n"
"padding:2px;\n"
"border:1px solid;\n"
"border-color: white;\n"
"border-radius:12px;\n"
"	font: 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#running_config_pre_checks_btn:hover{\n"
"background-color:rgb(255,255,255);\n"
"border:1px solid;\n"
"border-color:rgb(22, 15,121 );\n"
"color:rgb(22, 15, 121);\n"
"	font: 700 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#running_config_pre_checks_btn:pressed{\n"
"background-color:rgb(220, 220, 220);\n"
"border:1px solid;\n"
"border-color:rgb(15, 13, 125);\n"
"color:rgb(22, 15, 121);\n"
"	font: 800 14pt \"Ericsson Hilda\";\n"
"}")

        self.buttons_horizontal_layout.addWidget(self.running_config_pre_checks_btn)

        self.cli_preparation_btn = QPushButton(self.frame_for_buttons_and_their_status)
        self.cli_preparation_btn.setObjectName(u"cli_preparation_btn")
        self.cli_preparation_btn.setMinimumSize(QSize(0, 40))
        self.cli_preparation_btn.setStyleSheet(u"#cli_preparation_btn{\n"
"color:white;\n"
"background:solid;\n"
"background-color: rgb(22, 15, 121);\n"
"padding:2px;\n"
"border:1px solid;\n"
"border-color: white;\n"
"border-radius:12px;\n"
"	font: 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#cli_preparation_btn:hover{\n"
"background-color:rgb(255,255,255);\n"
"border:1px solid;\n"
"border-color:rgb(22, 15,121 );\n"
"color:rgb(22, 15, 121);\n"
"	font: 700 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#cli_preparation_btn:pressed{\n"
"background-color:rgb(220, 220, 220);\n"
"border:1px solid;\n"
"border-color:rgb(15, 13, 125);\n"
"color:rgb(22, 15, 121);\n"
"	font: 800 14pt \"Ericsson Hilda\";\n"
"}")

        self.buttons_horizontal_layout.addWidget(self.cli_preparation_btn)

        self.running_config_post_checks_btn = QPushButton(self.frame_for_buttons_and_their_status)
        self.running_config_post_checks_btn.setObjectName(u"running_config_post_checks_btn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.running_config_post_checks_btn.sizePolicy().hasHeightForWidth())
        self.running_config_post_checks_btn.setSizePolicy(sizePolicy3)
        self.running_config_post_checks_btn.setMinimumSize(QSize(260, 40))
        self.running_config_post_checks_btn.setMaximumSize(QSize(260, 16777215))
        self.running_config_post_checks_btn.setStyleSheet(u"#running_config_post_checks_btn{\n"
"color:white;\n"
"background:solid;\n"
"background-color: rgb(22, 15, 121);\n"
"padding:2px;\n"
"border:1px solid;\n"
"border-color: white;\n"
"border-radius:12px;\n"
"	font: 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#running_config_post_checks_btn:hover{\n"
"background-color:rgb(255,255,255);\n"
"border:1px solid;\n"
"border-color:rgb(22, 15,121 );\n"
"color:rgb(22, 15, 121);\n"
"	font: 700 14pt \"Ericsson Hilda\";\n"
"}\n"
"\n"
"#running_config_post_checks_btn:pressed{\n"
"background-color:rgb(220, 220, 220);\n"
"border:1px solid;\n"
"border-color:rgb(15, 13, 125);\n"
"color:rgb(22, 15, 121);\n"
"	font: 800 14pt \"Ericsson Hilda\";\n"
"}")

        self.buttons_horizontal_layout.addWidget(self.running_config_post_checks_btn)


        self.buttons_and_status_vertical_status.addLayout(self.buttons_horizontal_layout)

        self.status_labels_horizontal_layout = QHBoxLayout()
        self.status_labels_horizontal_layout.setObjectName(u"status_labels_horizontal_layout")
        self.template_checks_label = QLabel(self.frame_for_buttons_and_their_status)
        self.template_checks_label.setObjectName(u"template_checks_label")
        self.template_checks_label.setFont(font6)
        self.template_checks_label.setAlignment(Qt.AlignCenter)

        self.status_labels_horizontal_layout.addWidget(self.template_checks_label)

        self.running_config_pre_checks_label = QLabel(self.frame_for_buttons_and_their_status)
        self.running_config_pre_checks_label.setObjectName(u"running_config_pre_checks_label")
        self.running_config_pre_checks_label.setMinimumSize(QSize(0, 25))
        self.running_config_pre_checks_label.setFont(font6)
        self.running_config_pre_checks_label.setAlignment(Qt.AlignCenter)

        self.status_labels_horizontal_layout.addWidget(self.running_config_pre_checks_label)

        self.cli_preparation_status_label = QLabel(self.frame_for_buttons_and_their_status)
        self.cli_preparation_status_label.setObjectName(u"cli_preparation_status_label")
        self.cli_preparation_status_label.setFont(font6)
        self.cli_preparation_status_label.setAlignment(Qt.AlignCenter)

        self.status_labels_horizontal_layout.addWidget(self.cli_preparation_status_label)

        self.running_config_post_checks_label = QLabel(self.frame_for_buttons_and_their_status)
        self.running_config_post_checks_label.setObjectName(u"running_config_post_checks_label")
        self.running_config_post_checks_label.setFont(font6)
        self.running_config_post_checks_label.setAlignment(Qt.AlignCenter)

        self.status_labels_horizontal_layout.addWidget(self.running_config_post_checks_label)


        self.buttons_and_status_vertical_status.addLayout(self.status_labels_horizontal_layout)


        self.gridLayout_4.addLayout(self.buttons_and_status_vertical_status, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_for_buttons_and_their_status, 3, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Main_Application_Window)

        self.vendor_details_selection_combobox.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Main_Application_Window)
    # setupUi

    def retranslateUi(self, Main_Application_Window):
        Main_Application_Window.setWindowTitle(QCoreApplication.translate("Main_Application_Window", u"CLI Automation", None))
        self.groupBox.setTitle(QCoreApplication.translate("Main_Application_Window", u"MPBN Nokia CLI Automation", None))
        self.selected_host_details_label.setText(QCoreApplication.translate("Main_Application_Window", u"Selected Host Details :", None))
#if QT_CONFIG(whatsthis)
        self.selected_host_details_line_edit.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.selected_host_details_line_edit.setText(QCoreApplication.translate("Main_Application_Window", u" Host Details: -", None))
        self.new_session_button.setText(QCoreApplication.translate("Main_Application_Window", u"New Session", None))
        self.vendor_details_selection_combobox.setItemText(0, QCoreApplication.translate("Main_Application_Window", u"New Item", None))
        self.vendor_details_selection_combobox.setItemText(1, QCoreApplication.translate("Main_Application_Window", u"New Item", None))

        self.vendor_details_selection_combobox.setPlaceholderText(QCoreApplication.translate("Main_Application_Window", u"Select the vendor", None))
        self.sheet_creater_status_button_label.setText(QCoreApplication.translate("Main_Application_Window", u"Sheet Creater Task Status", None))
        self.sheet_creater_task_status_label.setText(QCoreApplication.translate("Main_Application_Window", u"TextLabel", None))
        self.template_checks_btn.setText(QCoreApplication.translate("Main_Application_Window", u"Template Checks", None))
        self.running_config_pre_checks_btn.setText(QCoreApplication.translate("Main_Application_Window", u"Running Config Pre Checks", None))
        self.cli_preparation_btn.setText(QCoreApplication.translate("Main_Application_Window", u"CLI Preparation", None))
        self.running_config_post_checks_btn.setText(QCoreApplication.translate("Main_Application_Window", u"Running Config Post Checks", None))
        self.template_checks_label.setText(QCoreApplication.translate("Main_Application_Window", u"Hello", None))
        self.running_config_pre_checks_label.setText(QCoreApplication.translate("Main_Application_Window", u"Hello", None))
        self.cli_preparation_status_label.setText(QCoreApplication.translate("Main_Application_Window", u"Hello", None))
        self.running_config_post_checks_label.setText(QCoreApplication.translate("Main_Application_Window", u"Hello", None))
    # retranslateUi

