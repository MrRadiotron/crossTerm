#import faulthandler
import sys
import serial
import threading
from PySide import QtCore, QtGui, QtUiTools
    
class serial_port_class(object):
    def __init__(self):
        self.connected = False

    def __del__(self):
        self.disconnect_port()

    def connect_port(self):
        try:
            self.serial_port = serial.Serial("/dev/tty.usbserial-A601R86K", 9600, timeout = None)
            self.connected = True
        except serial.SerialException, e:
            self.connected = False
        if self.connected:
            self.serial_thread = threading.Thread(target=self.recieve_port, args=(self))
            self.serial_thread.start()

    def disconnect_port(self):
        self.connected = False
        self.serial_thread.join()
        self.serial_port.close()
    
    def recieve_port(self):

        while self.connected:
            try:
                text = self.serial_port.read(1)
                if text != '':
                    print "text"
            except serial.SerialException, e:
                connected = False


class KeyPressEater(object):
    def connect_port(self):
        self.serial_thread = threading.Thread(target=self.eventFilter)
        self.serial_thread.start()

    def eventFilter(self):
        global serial_port
        while serial_port.connected == True:
            ch = raw_input()
            if serial_port.connected == True:
                serial_port.serial_port.write(ch)
            return QtCore.QObject.eventFilter(self, obj, event)
    
def main():
    global serial_port

    #faulthandler.enable()
    
    serial_port = serial_port_class()
    serial_port.connect_port()
    heyeater = KeyPressEater()

    if serial_port.connected== True:
        heyeater.connect_port()
        heyeater.serial_thread.join()


if __name__ == '__main__':
    main()

