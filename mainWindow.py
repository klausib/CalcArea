# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created: Fri Mar 14 09:25:50 2014
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmMainWindow(object):
    def setupUi(self, frmMainWindow):
        frmMainWindow.setObjectName(_fromUtf8("frmMainWindow"))
        frmMainWindow.resize(177, 138)
        frmMainWindow.setMinimumSize(QtCore.QSize(177, 138))
        frmMainWindow.setMaximumSize(QtCore.QSize(177, 16777215))
        self.frame_2 = QtGui.QFrame(frmMainWindow)
        self.frame_2.setGeometry(QtCore.QRect(10, 10, 151, 111))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_2.setLineWidth(0)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.layoutWidget = QtGui.QWidget(self.frame_2)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 131, 96))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblLayer = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblLayer.setFont(font)
        self.lblLayer.setObjectName(_fromUtf8("lblLayer"))
        self.verticalLayout.addWidget(self.lblLayer)
        self.lblQuadratmeter = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblQuadratmeter.setFont(font)
        self.lblQuadratmeter.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.lblQuadratmeter.setFrameShape(QtGui.QFrame.WinPanel)
        self.lblQuadratmeter.setFrameShadow(QtGui.QFrame.Raised)
        self.lblQuadratmeter.setText(_fromUtf8(""))
        self.lblQuadratmeter.setMargin(0)
        self.lblQuadratmeter.setObjectName(_fromUtf8("lblQuadratmeter"))
        self.verticalLayout.addWidget(self.lblQuadratmeter)
        self.lblHektar = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblHektar.setFont(font)
        self.lblHektar.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.lblHektar.setFrameShape(QtGui.QFrame.WinPanel)
        self.lblHektar.setFrameShadow(QtGui.QFrame.Raised)
        self.lblHektar.setText(_fromUtf8(""))
        self.lblHektar.setObjectName(_fromUtf8("lblHektar"))
        self.verticalLayout.addWidget(self.lblHektar)
        self.lblQuadratkilometer = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblQuadratkilometer.setFont(font)
        self.lblQuadratkilometer.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.lblQuadratkilometer.setFrameShape(QtGui.QFrame.WinPanel)
        self.lblQuadratkilometer.setFrameShadow(QtGui.QFrame.Raised)
        self.lblQuadratkilometer.setText(_fromUtf8(""))
        self.lblQuadratkilometer.setObjectName(_fromUtf8("lblQuadratkilometer"))
        self.verticalLayout.addWidget(self.lblQuadratkilometer)

        self.retranslateUi(frmMainWindow)
        QtCore.QMetaObject.connectSlotsByName(frmMainWindow)

    def retranslateUi(self, frmMainWindow):
        frmMainWindow.setWindowTitle(QtGui.QApplication.translate("frmMainWindow", "Calc Area", None, QtGui.QApplication.UnicodeUTF8))
        self.lblLayer.setText(QtGui.QApplication.translate("frmMainWindow", "Layer:", None, QtGui.QApplication.UnicodeUTF8))

