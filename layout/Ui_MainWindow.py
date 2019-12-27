# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_MainWindow.ui',
# licensing of 'Ui_MainWindow.ui' applies.
#
# Created: Fri Dec 27 23:26:55 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.portComboBox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portComboBox.sizePolicy().hasHeightForWidth())
        self.portComboBox.setSizePolicy(sizePolicy)
        self.portComboBox.setMinimumSize(QtCore.QSize(0, 0))
        self.portComboBox.setObjectName("portComboBox")
        self.horizontalLayout.addWidget(self.portComboBox)
        self.refreshBtn = QtWidgets.QPushButton(self.centralwidget)
        self.refreshBtn.setObjectName("refreshBtn")
        self.horizontalLayout.addWidget(self.refreshBtn)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.baudComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.baudComboBox.setObjectName("baudComboBox")
        self.baudComboBox.addItem("")
        self.baudComboBox.addItem("")
        self.horizontalLayout.addWidget(self.baudComboBox)
        self.connectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.connectBtn.setObjectName("connectBtn")
        self.horizontalLayout.addWidget(self.connectBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.autoScrollCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.autoScrollCheckBox.setChecked(True)
        self.autoScrollCheckBox.setObjectName("autoScrollCheckBox")
        self.horizontalLayout.addWidget(self.autoScrollCheckBox)
        self.sendFileBtn = QtWidgets.QPushButton(self.centralwidget)
        self.sendFileBtn.setEnabled(False)
        self.sendFileBtn.setObjectName("sendFileBtn")
        self.horizontalLayout.addWidget(self.sendFileBtn)
        self.clearOutputBtn = QtWidgets.QPushButton(self.centralwidget)
        self.clearOutputBtn.setObjectName("clearOutputBtn")
        self.horizontalLayout.addWidget(self.clearOutputBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.outputTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        self.outputTextBrowser.setFont(font)
        self.outputTextBrowser.setStyleSheet("background-color: rgb(30, 30, 30);\n"
"color: rgb(236, 236, 236);")
        self.outputTextBrowser.setObjectName("outputTextBrowser")
        self.verticalLayout.addWidget(self.outputTextBrowser)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.inputLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.inputLineEdit.setObjectName("inputLineEdit")
        self.horizontalLayout_2.addWidget(self.inputLineEdit)
        self.sendBtn = QtWidgets.QPushButton(self.centralwidget)
        self.sendBtn.setEnabled(False)
        self.sendBtn.setObjectName("sendBtn")
        self.horizontalLayout_2.addWidget(self.sendBtn)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.EOLComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.EOLComboBox.setObjectName("EOLComboBox")
        self.EOLComboBox.addItem("")
        self.EOLComboBox.addItem("")
        self.EOLComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.EOLComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Port:", None, -1))
        self.refreshBtn.setText(QtWidgets.QApplication.translate("MainWindow", "Refresh", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Baud rate:", None, -1))
        self.baudComboBox.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "9600", None, -1))
        self.baudComboBox.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "115200", None, -1))
        self.connectBtn.setText(QtWidgets.QApplication.translate("MainWindow", "Connect", None, -1))
        self.autoScrollCheckBox.setText(QtWidgets.QApplication.translate("MainWindow", "Auto scroll", None, -1))
        self.sendFileBtn.setText(QtWidgets.QApplication.translate("MainWindow", "Send file", None, -1))
        self.clearOutputBtn.setText(QtWidgets.QApplication.translate("MainWindow", "Clear output", None, -1))
        self.sendBtn.setText(QtWidgets.QApplication.translate("MainWindow", "Send", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "EOL:", None, -1))
        self.EOLComboBox.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "LF", None, -1))
        self.EOLComboBox.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "CR;LF", None, -1))
        self.EOLComboBox.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "CR", None, -1))

