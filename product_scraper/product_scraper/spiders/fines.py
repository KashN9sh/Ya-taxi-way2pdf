# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/el-muncho/PycharmProjects/Ya-taxi-way2pdf/product_scraper/product_scraper/spiders/fines.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 20, 311, 321))
        self.listWidget.setObjectName("listWidget")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(350, 20, 431, 321))
        self.listWidget_2.setObjectName("listWidget_2")
        self.BtnGetFines = QtWidgets.QPushButton(self.centralwidget)
        self.BtnGetFines.setGeometry(QtCore.QRect(100, 350, 151, 32))
        self.BtnGetFines.setObjectName("BtnGetFines")
        self.BtgEbatShtrule1 = QtWidgets.QPushButton(self.centralwidget)
        self.BtgEbatShtrule1.setGeometry(QtCore.QRect(510, 350, 161, 32))
        self.BtgEbatShtrule1.setObjectName("BtgEbatShtrule1")
        self.listWidget1 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget1.setGeometry(QtCore.QRect(20, 391, 761, 181))
        self.listWidget1.setObjectName("listWidget1")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.BtnGetFines.setText(_translate("MainWindow", "Получить штрафы"))
        self.BtgEbatShtrule1.setText(_translate("MainWindow", "Списать штрафы"))
