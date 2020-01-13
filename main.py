import yaml
import sys
import os
import time
import string
import serial.tools.list_ports, serial.serialutil

from PySide2.QtGui import QPixmap, QImage, QIcon, QTextCursor, QFont
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QFileDialog, QLineEdit
from PySide2.QtCore import Slot, Qt, QPoint, Signal, QEvent, QTimer
from layout import Ui_MainWindow, icon
from send_file import SendFileDialog
from edit import LinePlainTextEdit

import serial_port
default_setting = """---
priority: []
baud: {}
custom_baud: []
"""

__version__ = '1.4.0'

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ====================
        # == output browser ==
        # ====================
        linePlainTextEdit = LinePlainTextEdit(self)
        outputTextBrowser = self.ui.outputTextBrowser
        self.ui.verticalLayout.replaceWidget(outputTextBrowser, linePlainTextEdit)
        self.ui.outputTextBrowser = linePlainTextEdit
        self.ui.outputTextBrowser.setReadOnly(True)
        outputTextBrowser.deleteLater()

        scrollBar = self.ui.outputTextBrowser.verticalScrollBar()
        scrollBar.setStyleSheet("background-color: rgb(240, 240, 240);\n""color: rgb(12, 12, 12);")
        self.ui.outputTextBrowser.setStyleSheet("background-color: rgb(30, 30, 30);\n""color: rgb(236, 236, 236);")
        self.ui.outputTextBrowser.installEventFilter(self)
        font = QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        self.ui.outputTextBrowser.setFont(font)
        # =============================

        self.ser = serial_port.QPySerial()
        self.ser.errorOccurred.connect(self.on_serial_errorOccurred)
        self.load_setting()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_from_ser)
        self.setWindowIcon(QIcon(r':icon.ico'))
        self.setWindowTitle('ATerm '+__version__)


        buads = [9600, 115200] + self.setting['custom_baud']
        buads = [str(b) for b in sorted(list(set(buads)))]
        self.ui.baudComboBox.addItems(buads)
        self.ui.baudComboBox.setLineEdit(QLineEdit())

        self.on_refreshBtn_clicked()

    def closeEvent(self, event):
        self.on_connectBtn_clicked(force_off=True)
        self.save_setting()
        event.accept()

    
    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and source is self.ui.outputTextBrowser:
            key = event.key()
            if self.ser.is_open() and (key == Qt.Key_Enter or key == Qt.Key_Return):
                self.on_sendBtn_clicked()
            else:
                if event.key() == Qt.Key_Backspace:
                    txt = self.ui.inputLineEdit.text()[:-1]
                elif event.text() in string.printable:
                    txt = self.ui.inputLineEdit.text() + event.text()
                else:
                    txt = self.ui.inputLineEdit.text()
                self.ui.inputLineEdit.setText(txt)
            # print('key press:', (event.key(), event.text()))
        return super(AppWindow, self).eventFilter(source, event)

    def load_setting(self):
        self.setting = yaml.load(default_setting, Loader=yaml.SafeLoader)
        if os.path.isfile('setting.yaml'):
            with open('setting.yaml', 'r') as f:
                setting = yaml.load(f, Loader=yaml.SafeLoader)
            self.setting.update(setting)
    
    def save_setting(self):
        with open('setting.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(self.setting, f, encoding='utf-8')

    def read_from_ser(self):
        if self.ser.in_waiting() > 0:
            text = self.ser.read(self.ser.in_waiting()).decode('ascii')
            self.append_term(text)

    def append_term(self, text):
        scrollBar = self.ui.outputTextBrowser.verticalScrollBar()
        slider_pos = scrollBar.value()
        self.ui.outputTextBrowser.moveCursor(QTextCursor.End)
        self.ui.outputTextBrowser.insertPlainText(text)
        if self.ui.autoScrollCheckBox.isChecked():
            scrollBar.setValue(scrollBar.maximum())
        else:
            scrollBar.setValue(slider_pos)

    @Slot(int)
    def on_autoScrollCheckBox_stateChanged(self, state):
        if (state == Qt.Checked):
            scrollBar = self.ui.outputTextBrowser.verticalScrollBar()
            scrollBar.setValue(scrollBar.maximum())

    @Slot()
    def on_refreshBtn_clicked(self):
        self.on_connectBtn_clicked(force_off=True)
        ports = serial.tools.list_ports.comports()
        ports = ['{} - {}'.format(device.device, device.description) for device in ports]
        self.ui.portComboBox.clear()
        self.ui.portComboBox.addItems(ports)
        for target in self.setting['priority']:
            for i, port in enumerate(ports):
                if target.lower() in port.lower():
                    self.ui.portComboBox.setCurrentIndex(i)
                    return

        # self.ui.portComboBox.view().setMinimumWidth(100)
    
    @Slot(int)
    def on_portComboBox_currentIndexChanged(self, index):
        port_name = self.ui.portComboBox.itemText(index)
        for k, v in self.setting['baud'].items():
            if k.lower() in port_name.lower():
                self.ui.baudComboBox.setEditText(str(v))
                self.ui.baudComboBox.setCurrentIndex(0)

    @Slot()
    def on_connectBtn_clicked(self, force_off=False):
        if self.ui.connectBtn.text() == 'Connect' and not force_off:
            dev = self.ui.portComboBox.currentText().split('-')[0].strip()
            baud_rate = int(self.ui.baudComboBox.currentText())
            if dev == '': return
            self.ser.open(dev, baud_rate)
            self.ui.connectBtn.setText('Disconnect')
            self.timer.start(200)
            self.ui.inputLineEdit.returnPressed.connect(self.on_sendBtn_clicked)
            self.ui.sendBtn.setEnabled(True)
            self.ui.sendFileBtn.setEnabled(True)
            self.ui.portComboBox.setEnabled(False)
            self.ui.baudComboBox.setEnabled(False)
            self.ui.refreshBtn.setEnabled(False)
        else:
            self.timer.stop()
            if not self.ser.is_open():
                self.ser.close()
            try: self.ui.inputLineEdit.returnPressed.disconnect()
            except: pass
            self.ui.sendBtn.setEnabled(False)
            self.ui.sendFileBtn.setEnabled(False)
            self.ui.portComboBox.setEnabled(True)
            self.ui.baudComboBox.setEnabled(True)
            self.ui.refreshBtn.setEnabled(True)
            self.ui.connectBtn.setText('Connect')

    @Slot()
    def on_sendFileBtn_clicked(self):
        path = os.getcwd()
        if 'path' in self.setting and os.path.exists(path):
            if os.path.isfile(path):
                path = os.path.dirname(self.setting['path'])
            else:
                path = self.setting['path']
        fileName = QFileDialog.getOpenFileName(parent=self, caption="Choose file", dir=path)[0]
        if os.path.isfile(fileName):
            self.setting['path'] = os.path.dirname(fileName)
            dialog = SendFileDialog(fileName, self.ser, self)
            dialog.exec_()
            # with open(fileName, 'rb') as f:
            #     self.ser.write(f.read(), 0)
            # while self.ser.out_waiting() > 0:
            #     print(self.ser.out_waiting())
            #     time.sleep(0.2)

    @Slot()
    def on_sendBtn_clicked(self):
        eol = ''
        if self.ui.EOLComboBox.currentText() == 'LF':
            eol = '\n'
        elif self.ui.EOLComboBox.currentText() == 'CR;LF':
            eol = '\r\n'
        elif self.ui.EOLComboBox.currentText() == 'CR':
            eol = '\r'
        text = self.ui.inputLineEdit.text()
        text = text + eol
        self.ser.write(text.encode('ascii'))
        self.ui.inputLineEdit.setText('')

    @Slot(int)
    def on_serial_errorOccurred(self, error):
        if serial_port.CLOSED != error:
            self.on_connectBtn_clicked(True)

    @Slot()
    def on_clearOutputBtn_clicked(self):
        self.ui.outputTextBrowser.clear()
            

def main():
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()