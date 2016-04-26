# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file Ui_Anglecalc.ui
# Created with: PyQt4 UI code generator 4.4.4
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Anglecalc(object):
    def setupUi(self, Anglecalc):
        Anglecalc.setObjectName("Anglecalc")
        Anglecalc.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Anglecalc)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Anglecalc)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Anglecalc.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Anglecalc.reject)
        QtCore.QMetaObject.connectSlotsByName(Anglecalc)

    def retranslateUi(self, Anglecalc):
        Anglecalc.setWindowTitle(QtGui.QApplication.translate("Anglecalc", "Anglecalc", None, QtGui.QApplication.UnicodeUTF8))
