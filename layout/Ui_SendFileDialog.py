# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_SendFileDialog.ui',
# licensing of 'Ui_SendFileDialog.ui' applies.
#
# Created: Fri Jan 10 00:35:52 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SendFileDialog(object):
    def setupUi(self, SendFileDialog):
        SendFileDialog.setObjectName("SendFileDialog")
        SendFileDialog.resize(271, 123)
        self.verticalLayout = QtWidgets.QVBoxLayout(SendFileDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(SendFileDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.filenameLabel = QtWidgets.QLabel(SendFileDialog)
        self.filenameLabel.setText("")
        self.filenameLabel.setObjectName("filenameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.filenameLabel)
        self.label_2 = QtWidgets.QLabel(SendFileDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.pathLabel = QtWidgets.QLabel(SendFileDialog)
        self.pathLabel.setText("")
        self.pathLabel.setObjectName("pathLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pathLabel)
        self.label_3 = QtWidgets.QLabel(SendFileDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.sizeLabel = QtWidgets.QLabel(SendFileDialog)
        self.sizeLabel.setText("")
        self.sizeLabel.setObjectName("sizeLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sizeLabel)
        self.verticalLayout.addLayout(self.formLayout)
        self.progressBar = QtWidgets.QProgressBar(SendFileDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.buttonBox = QtWidgets.QDialogButtonBox(SendFileDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SendFileDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SendFileDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SendFileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SendFileDialog)

    def retranslateUi(self, SendFileDialog):
        SendFileDialog.setWindowTitle(QtWidgets.QApplication.translate("SendFileDialog", "Send File", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("SendFileDialog", "Filename:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("SendFileDialog", "Path:", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("SendFileDialog", "Size:", None, -1))

