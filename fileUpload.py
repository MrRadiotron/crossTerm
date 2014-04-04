#! /usr/bin/python

import sys, os
from PySide import QtGui, QtCore
import serial, signal
import platform, glob

def serialPortConnected():
    global serialPort
    global connected
    serialSettings.port = ui.portSelectCombo.currentText()
    print "opening serial port: ", serialSettings.port
    serialPort = serial.Serial(serialSettings.port, serialSettings.baud, serialSettings.byteSize, serialSettings.parity, serialSettings.stopBits, serialSettings.time, xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False, interCharTimeout=None)
    connected = True
    ui.connectButton.setText("Disconnect")
    ui.comSelectGroupBox.setDisabled(True)
    ui.baudSelectGroupBox.setDisabled(True)
    ui.dataBitsGroupBox.setDisabled(True)
    ui.parityGroupBox.setDisabled(True)
    ui.stopBitsGroupBox.setDisabled(True)
    ui.handshakingGroupBox.setDisabled(True)
    ui.fileControl.setDisabled(False)
    ui.lineByLine.setDisabled(False)
    ui.byteDelaySpinBox.setDisabled(False)

def fileDialog():
    global fileName
    system_name = platform.system()
    if system_name == "Windows":
        pathName = os.getenv("UserProfile")
        print pathName
        #pathName = "%UserProfile%"
    else:
        pathName = '$HOME'
    (fileName,none) = QtGui.QFileDialog.getOpenFileName(None, 'Open File', None)#pathName)

class serialSettingsClass():
    baud = None
    byteSize = None
    parity = None
    stopBits = None
    time = 0
    port = None

class fileRunner:
    def __init__(self):
        self.fd = None
        self.state = 'idle'
        self.fd = open(fileName, 'rU')

    def nextChar(self):
        global serialPort
        ch = self.fd.read(1)
        serialPort.write(ch)


    def nextLine(self):
        global serialPort
        lineText = self.fd.readline()
        if lineText == '':
            serialPort.close()
            sys.exit(0)
        sys.stdout.write('\n' + lineText + '\n')
        serialPort.write(lineText)   

def main():
    app = QtGui.QApplication(sys.argv)
    global fileName
    global serialPort
    global serialSettings
    fileDialog()
    serialSettings = serialSettingsClass()
    serialSettings.port = "COM25"
    serialSettings.baud = '19200'
    serialSettings.byteSize = serial.EIGHTBITS
    serialSettings.parity = serial.PARITY_NONE
    serialSettings.stopBits = serial.STOPBITS_ONE
    serialSettings.time = None
    print "opening serial port: ", serialSettings.port
    serialPort = serial.Serial(serialSettings.port, serialSettings.baud, serialSettings.byteSize, serialSettings.parity, serialSettings.stopBits, serialSettings.time, xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False, interCharTimeout=None)
    global fRunner
    fRunner = fileRunner()
    #fRunner.nextLine()
    while 1:
        #time.sleep(.010)
        text = serialPort.read(1)
        if text != '':
            sys.stdout.write(text)
            if text == chr(5):
                fRunner.nextLine()




if __name__ == '__main__':
    main()
