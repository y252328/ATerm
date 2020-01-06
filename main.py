import yaml
import sys
import os
import time
import string
import serial, serial.tools.list_ports, serial.serialutil

from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QFileDialog, QLineEdit
from PySide2.QtCore import Slot, Qt, QPoint, Signal, QEvent, QTimer
from layout import Ui_MainWindow, icon

default_setting = """---
priority: []
baud: {}
custom_baud: []
"""

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ser = None
        self.load_setting()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_from_ser)
        self.setWindowIcon(QIcon(r':icon.ico'))

        scrollBar = self.ui.outputTextBrowser.verticalScrollBar()
        scrollBar.setStyleSheet("background-color: rgb(240, 240, 240);\n""color: rgb(12, 12, 12);")

        buads = [9600, 115200] + self.setting['custom_baud']
        buads = [str(b) for b in sorted(list(set(buads)))]
        self.ui.baudComboBox.addItems(buads)
        self.ui.baudComboBox.setLineEdit(QLineEdit())

        self.on_refreshBtn_clicked()
        self.ui.outputTextBrowser.installEventFilter(self)

    def closeEvent(self, event):
        self.on_connectBtn_clicked(force_off=True)
        self.save_setting()
        event.accept()

    
    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and source is self.ui.outputTextBrowser:
            key = event.key()
            if self.ser != None and (key == Qt.Key_Enter or key == Qt.Key_Return):
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
        if self.serial_in_waiting() > 0:
            text = self.serial_read(self.serial_in_waiting()).decode('ascii')
            self.append_term(text)

    def append_term(self, text):
        text = self.ui.outputTextBrowser.toPlainText() + text
        self.ui.outputTextBrowser.setText(text)
        if self.ui.autoScrollCheckBox.isChecked():
            scrollBar = self.ui.outputTextBrowser.verticalScrollBar()
            scrollBar.setValue(scrollBar.maximum())

    def serial_in_waiting(self):
        if self.ser != None:
            try:
                return self.ser.in_waiting
            except serial.serialutil.SerialException:
                self.on_connectBtn_clicked(True)
        return 0

    def serial_out_waiting(self):
        if self.ser != None:
            try:
                return self.ser.out_waiting
            except serial.serialutil.SerialException:
                self.on_connectBtn_clicked(True)
        return 0

    def serial_read(self, n):
        if self.ser != None:
            try:
                return self.ser.read(n)
            except serial.serialutil.SerialException:
                self.on_connectBtn_clicked(True)
        return bytes()

    def serial_write(self, data, timeout=None):
        if self.ser != None:
            try:
                if timeout != None: 
                    self.ser.write_timeout = timeout
                n = self.ser.write(data)
                if timeout != None: 
                    self.ser.write_timeout = None
                return n
            except serial.serialutil.SerialException:
                self.on_connectBtn_clicked(force_off=True)
        return 0

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
            self.ser = serial.Serial(dev, baud_rate)
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
            if self.ser != None:
                self.ser.close()
            try: self.ui.inputLineEdit.returnPressed.disconnect()
            except: pass
            self.ui.sendBtn.setEnabled(False)
            self.ui.sendFileBtn.setEnabled(False)
            self.ui.portComboBox.setEnabled(True)
            self.ui.baudComboBox.setEnabled(True)
            self.ui.refreshBtn.setEnabled(True)
            self.ser = None
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
            with open(fileName, 'rb') as f:
                self.serial_write(f.read(), 0)
            while self.serial_out_waiting() > 0:
                print(self.serial_out_waiting())
                time.sleep(0.2)

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
        self.serial_write(text.encode('ascii'))
        self.ui.inputLineEdit.setText('')

    @Slot()
    def on_clearOutputBtn_clicked(self):
        self.ui.outputTextBrowser.setText('')
            

def main():
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()