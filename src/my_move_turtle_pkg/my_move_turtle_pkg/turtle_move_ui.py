# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'turtle_move.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QListWidget, QPushButton, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(656, 288)
        self.btn_go = QPushButton(Form)
        self.btn_go.setObjectName(u"btn_go")
        self.btn_go.setGeometry(QRect(150, 50, 61, 51))
        self.btn_back = QPushButton(Form)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setGeometry(QRect(150, 190, 61, 51))
        self.btn_left = QPushButton(Form)
        self.btn_left.setObjectName(u"btn_left")
        self.btn_left.setGeometry(QRect(60, 120, 61, 51))
        self.btn_right = QPushButton(Form)
        self.btn_right.setObjectName(u"btn_right")
        self.btn_right.setGeometry(QRect(240, 120, 61, 51))
        self.btn_stop = QPushButton(Form)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setGeometry(QRect(150, 120, 61, 51))
        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(350, 50, 256, 192))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_go.setText(QCoreApplication.translate("Form", u"Go", None))
        self.btn_back.setText(QCoreApplication.translate("Form", u"Back", None))
        self.btn_left.setText(QCoreApplication.translate("Form", u"Left", None))
        self.btn_right.setText(QCoreApplication.translate("Form", u"Right", None))
        self.btn_stop.setText(QCoreApplication.translate("Form", u"STOP", None))
    # retranslateUi

