# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ventanaCalendarioDevolucion.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/calendario/img/calendar-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.calendarioDevolucion = QtWidgets.QCalendarWidget(Dialog)
        self.calendarioDevolucion.setGeometry(QtCore.QRect(0, 0, 401, 291))
        self.calendarioDevolucion.setStyleSheet("background-color:rgb(135, 154, 209)")
        self.calendarioDevolucion.setObjectName("calendarioDevolucion")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "CALENDARIO FECHA DEVOLUCIÓN"))
import recursos_rc