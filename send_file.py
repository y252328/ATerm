import os
import time

from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QApplication, QMainWindow, QFileDialog, QSizePolicy, QMenu, QMessageBox
from PySide2.QtCore import Slot, Qt, QPoint, QThread, Signal
from layout import Ui_SendFileDialog

class SendFileThread(QThread):
    update_remain = Signal(int)
    def __init__(self, file_path, serial):
        super(SendFileThread, self).__init__()
        self.ser = serial
        self.file_path = file_path
        self.stop = False

    def run(self):
        with open(self.file_path, 'rb') as f:
            self.ser.write(f.read(), 0)
        while self.ser.out_waiting() > 0 and not self.stop:
            remain = self.ser.out_waiting()
            print(remain)
            self.update_remain.emit(remain)
            time.sleep(0.2)
        self.update_remain.emit(0)
        print('thread stop')

    def on_serial_errorOccurred(self):
        self.stop = True
        


class SendFileDialog(QDialog):
    def __init__(self, file_path, serial, parent=None):
        super(SendFileDialog, self).__init__(parent=parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.ser = serial
        self.ser.errorOccurred.connect(self.on_serial_errorOccurred)
        self.file_path = file_path
        self.ui = Ui_SendFileDialog()
        self.ui.setupUi(self)
        self.ui.filenameLabel.setText(os.path.basename(file_path))
        self.ui.pathLabel.setText(file_path)
        self.size = os.path.getsize(file_path)
        self.remain = self.size
        self.ui.sizeLabel.setText("{:.2f} / {:.2f} KB".format((self.size-self.remain)/1024, self.size/1024))
        self.thread = SendFileThread(self.file_path, self.ser)
        self.thread.update_remain.connect(self.update_remain)
        self.thread.start()

    def closeEvent(self, event):
        self.thread.on_serial_errorOccurred()
        event.accept()

    @Slot(int)
    def update_remain(self, remain):
        self.remain = remain
        self.ui.sizeLabel.setText("{:.2f} / {:.2f} KB".format((self.size-self.remain)/1024, self.size/1024))
        self.ui.progressBar.setValue(((self.size-self.remain)/self.size)*100)
        if remain == 0:
            self.close()
        
    @Slot(int)
    def on_serial_errorOccurred(self, error):
        self.thread.on_serial_errorOccurred()
        self.thread.wait()
        self.close()

    