# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sub_pub_msg.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(655, 404)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.btn_pub_start = QPushButton(self.centralwidget)
        self.btn_pub_start.setObjectName(u"btn_pub_start")
        self.btn_pub_start.setGeometry(QRect(120, 40, 89, 25))
        self.btn_pub_cancel = QPushButton(self.centralwidget)
        self.btn_pub_cancel.setObjectName(u"btn_pub_cancel")
        self.btn_pub_cancel.setGeometry(QRect(230, 40, 89, 25))
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(360, 30, 256, 301))
        self.btn_sub_cancel = QPushButton(self.centralwidget)
        self.btn_sub_cancel.setObjectName(u"btn_sub_cancel")
        self.btn_sub_cancel.setGeometry(QRect(230, 90, 89, 25))
        self.btn_sub_start = QPushButton(self.centralwidget)
        self.btn_sub_start.setObjectName(u"btn_sub_start")
        self.btn_sub_start.setGeometry(QRect(120, 90, 89, 25))
        self.lbl_pub = QLabel(self.centralwidget)
        self.lbl_pub.setObjectName(u"lbl_pub")
        self.lbl_pub.setGeometry(QRect(40, 40, 67, 17))
        self.lbl_sub = QLabel(self.centralwidget)
        self.lbl_sub.setObjectName(u"lbl_sub")
        self.lbl_sub.setGeometry(QRect(40, 90, 67, 17))
        self.lbl_sub.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 655, 28))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_pub_start.setText(QCoreApplication.translate("MainWindow", u"Subscribe", None))
        self.btn_pub_cancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.btn_sub_cancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.btn_sub_start.setText(QCoreApplication.translate("MainWindow", u"Publish", None))
        self.lbl_pub.setText(QCoreApplication.translate("MainWindow", u"Subscribe", None))
        self.lbl_sub.setText(QCoreApplication.translate("MainWindow", u"Publisher", None))
    # retranslateUi

