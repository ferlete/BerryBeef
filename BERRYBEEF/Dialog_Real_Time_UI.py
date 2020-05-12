# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_Real_Time_UI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(468, 436)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(180, 380, 81, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lbl_result = QtWidgets.QLabel(Dialog)
        self.lbl_result.setGeometry(QtCore.QRect(20, 20, 441, 261))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lbl_result.setFont(font)
        self.lbl_result.setObjectName("lbl_result")
        self.lbl_apro = QtWidgets.QLabel(Dialog)
        self.lbl_apro.setGeometry(QtCore.QRect(10, 310, 441, 61))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.lbl_apro.setFont(font)
        self.lbl_apro.setObjectName("lbl_apro")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Predição em tempo real"))
        self.lbl_result.setText(_translate("Dialog", "TextLabel"))
        self.lbl_apro.setText(_translate("Dialog", "TextLabel"))
