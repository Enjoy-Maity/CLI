# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_start_dialog_box.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QSizePolicy, QTextEdit, QWidget)

class Ui_application_start_dialog(object):
    def setupUi(self, application_start_dialog):
        if not application_start_dialog.objectName():
            application_start_dialog.setObjectName(u"application_start_dialog")
        application_start_dialog.resize(640, 480)
        self.gridLayout = QGridLayout(application_start_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(application_start_dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.textEdit = QTextEdit(self.frame)
        self.textEdit.setObjectName(u"textEdit")

        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(application_start_dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(application_start_dialog)

        QMetaObject.connectSlotsByName(application_start_dialog)
    # setupUi

    def retranslateUi(self, application_start_dialog):
        application_start_dialog.setWindowTitle(QCoreApplication.translate("application_start_dialog", u"Dialog", None))
    # retranslateUi

