# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designNTnOQr.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(986, 699)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.start_view = QGraphicsView(self.centralwidget)
        self.start_view.setObjectName(u"start_view")
        self.start_view.setGeometry(QRect(20, 60, 961, 601))
        self.start_pushButton = QPushButton(self.centralwidget)
        self.start_pushButton.setObjectName(u"start_pushButton")
        self.start_pushButton.setGeometry(QRect(30, 0, 161, 51))
        self.stop_pushButton = QPushButton(self.centralwidget)
        self.stop_pushButton.setObjectName(u"stop_pushButton")
        self.stop_pushButton.setGeometry(QRect(200, 0, 121, 51))
        self.btncount = QPushButton(self.centralwidget)
        self.btncount.setObjectName(u"btncount")
        self.btncount.setGeometry(QRect(840, 10, 121, 41))
        self.count = QLCDNumber(self.centralwidget)
        self.count.setObjectName(u"count")
        self.count.setGeometry(QRect(630, 10, 199, 39))
        self.total_count = QPushButton(self.centralwidget)
        self.total_count.setObjectName(u"total_count")
        self.total_count.setGeometry(QRect(390, 10, 91, 41))
        self.total_count_2 = QTextEdit(self.centralwidget)
        self.total_count_2.setObjectName(u"total_count_2")
        self.total_count_2.setGeometry(QRect(510, 10, 104, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 986, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.start_pushButton.setText(QCoreApplication.translate("MainWindow", u"start", None))
        self.stop_pushButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.btncount.setText(QCoreApplication.translate("MainWindow", u"count", None))
        self.total_count.setText(QCoreApplication.translate("MainWindow", u"object_count", None))
    # retranslateUi

