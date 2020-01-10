from PySide2.QtCore import QObject , Signal
import serial

CLOSED = 2
NOT_OPEN = 1
UNKNOWN_ERROR = 9

class QPySerial(QObject):
    errorOccurred = Signal(int)

    def __init__(self,parent=None):
        super(QPySerial,self).__init__(parent)
        self.ser = None

    def open(self, port, baudrate):
        if self.ser != None:
            self.ser.close()
        self.ser = serial.Serial(port=port, baudrate=baudrate)
    
    def close(self):
        if self.ser != None:
            self.ser.close()
        self.ser = None
        self.errorOccurred.emit(CLOSED)

    def is_open(self):
        if self.ser != None:
            try:
                if self.ser.readable() and self.ser.writable():
                    return True
            except serial.serialutil.SerialException:
                pass
            self.errorOccurred.emit(UNKNOWN_ERROR)
            self.ser = None
        return False

    def in_waiting(self):
        if self.ser != None:
            try:
                return self.ser.in_waiting
            except serial.serialutil.SerialException:
                self.errorOccurred.emit(UNKNOWN_ERROR)
                self.ser = None
        return 0

    def out_waiting(self):
        if self.ser != None:
            try:
                return self.ser.out_waiting
            except serial.serialutil.SerialException:
                self.errorOccurred.emit(UNKNOWN_ERROR)
                self.ser = None
        return 0

    def read(self, n):
        if self.ser != None:
            try:
                return self.ser.read(n)
            except serial.serialutil.SerialException:
                self.errorOccurred.emit(UNKNOWN_ERROR)
                self.ser = None
        return bytes()

    def write(self, data, timeout=None):
        if self.ser != None:
            try:
                self.ser.write_timeout = None
                if timeout != None: 
                    self.ser.write_timeout = timeout
                n = self.ser.write(data)
                # if timeout != None: 
                #     self.ser.write_timeout = None
                return n
            except serial.serialutil.SerialException:
                self.errorOccurred.emit(UNKNOWN_ERROR)
                self.ser = None
        return 0
