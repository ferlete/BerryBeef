# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Config_UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(301, 158)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(90, 90, 181, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_sincronizar = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_sincronizar.setObjectName("btn_sincronizar")
        self.horizontalLayout.addWidget(self.btn_sincronizar)
        self.btn_fechar = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_fechar.setObjectName("btn_fechar")
        self.horizontalLayout.addWidget(self.btn_fechar)
        self.txt_ip = QtWidgets.QLineEdit(Dialog)
        self.txt_ip.setGeometry(QtCore.QRect(10, 40, 171, 28))
        self.txt_ip.setObjectName("txt_ip")
        self.txt_port = QtWidgets.QLineEdit(Dialog)
        self.txt_port.setGeometry(QtCore.QRect(200, 40, 71, 28))
        self.txt_port.setObjectName("txt_port")
        self.lb_ip = QtWidgets.QLabel(Dialog)
        self.lb_ip.setGeometry(QtCore.QRect(10, 20, 81, 20))
        self.lb_ip.setObjectName("lb_ip")
        self.lbl_port = QtWidgets.QLabel(Dialog)
        self.lbl_port.setGeometry(QtCore.QRect(200, 20, 81, 20))
        self.lbl_port.setObjectName("lbl_port")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(0, 130, 291, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setMaximum(5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sincronizar Modelos"))
        self.btn_sincronizar.setText(_translate("Dialog", "Sincronizar"))
        self.btn_fechar.setText(_translate("Dialog", "Fechar"))
        self.txt_ip.setText(_translate("Dialog", "192.168.25.5"))
        self.txt_port.setText(_translate("Dialog", "8080"))
        self.lb_ip.setText(_translate("Dialog", "IP Servidor"))
        self.lbl_port.setText(_translate("Dialog", "Porta"))
