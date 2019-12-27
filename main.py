
import sys
import os
import time
import serial
import serial.tools.list_ports
import serial.serialutil

from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QSizePolicy, QMenu, QMessageBox, QFileDialog
from PySide2.QtCore import Slot, Qt, QPoint, Signal, QEvent, QTimer
from layout import Ui_MainWindow  


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ser = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_from_ser)
        self.on_refreshBtn_clicked()
        scrollBar = self.ui.outputTextBrowser.verticalScrollBar()
        scrollBar.setStyleSheet("background-color: rgb(240, 240, 240);\n"
"color: rgb(12, 12, 12);")

    def closeEvent(self, event):
        if self.ser != None:
            self.ser.close()
        self.timer.stop()
        event.accept()

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

    def serial_write(self, data):
        if self.ser != None:
            try:
                return self.ser.write(data)
            except serial.serialutil.SerialException:
                self.on_connectBtn_clicked(True)
        return 0

    @Slot()
    def on_refreshBtn_clicked(self):
        ports = serial.tools.list_ports.comports()
        port = ['{} - {}'.format(device.device, device.description) for device in ports]
        self.ui.portComboBox.clear()
        self.ui.portComboBox.addItems(port)
        # self.ui.portComboBox.view().setMinimumWidth(100)

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
        else:
            self.timer.stop()
            if self.ser != None:
                self.ser.close()
            self.ui.inputLineEdit.returnPressed.disconnect()
            self.ui.sendBtn.setEnabled(False)
            self.ui.sendFileBtn.setEnabled(False)
            self.ser == None
            self.ui.connectBtn.setText('Connect')

    @Slot()
    def on_sendFileBtn_clicked(self):
        fileName = QFileDialog.getOpenFileName(parent=self, caption="Choose file", dir=os.getcwd())
        print(fileName[0])
        with open(fileName[0], 'rb') as f:
            self.serial_write(f.read())
        while self.serial_out_waiting() > 0:
            print('wait')
            time.sleep(0.1)

    @Slot()
    def on_sendBtn_clicked(self):
        eol = '\n'
        if self.ui.EOLComboBox.currentText() == 'CR;LF':
            eol = '\r\n'
        elif self.ui.EOLComboBox.currentText() == 'CR':
            eol = '\r'
        text = self.ui.inputLineEdit.text() + eol
        self.serial_write(text.encode('ascii'))
        self.ui.inputLineEdit.setText('')
        self.append_term(text)

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