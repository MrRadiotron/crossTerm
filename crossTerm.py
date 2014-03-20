#! /usr/bin/python

import sys, os
from PySide import QtCore, QtGui, QtUiTools
import serial
import platform, glob



def closeEvent(self, event):
    event.ignore()
    cleanUp()

def cleanUp():
    global connected
    if connected:
        serialPort.close()
    if fRunner.fd != None:
        fRunner.fd.close()
    QtCore.QCoreApplication.instance().quit()
    

def baudToggled():
    global serialPort
    buttons = ui.BAUD_RATE.findChildren(QtGui.QRadioButton)
    for button in buttons:
        if button.isChecked():
            print "Baud Rate: " + button.text()
            serialSettings.baud = int(button.text())

def dataBitsToggled():
    global serialPort
    buttons = ui.DATA_BITS.findChildren(QtGui.QRadioButton)
    for button in buttons:
        if button.isChecked():
            print "Data Bits: " + button.text()
            if button.text() == '5':
                serialSettings.byteSize = serial.FIVEBITS
            elif button.text() == '6':
                serialSettings.byteSize = serial.SIXBITS
            elif button.text() == '7':
                serialSettings.byteSize = serial.SEVENBITS
            elif button.text() == '8':
                serialSettings.byteSize = serial.EIGHTBITS

def parityToggled():
    global serialPort
    buttons = ui.PARITY.findChildren(QtGui.QRadioButton)
    for button in buttons:
        if button.isChecked():
            print "Parity: " + button.text()
            if button.text() == 'none':
                serialSettings.parity = serial.PARITY_NONE
            if button.text() == 'even':
                serialSettings.parity = serial.PARITY_EVEN
            if button.text() == 'odd':
                serialSettings.parity = serial.PARITY_ODD
            if button.text() == 'mark':
                serialSettings.parity = serial.PARITY_MARK
            if button.text() == 'space':
                serialSettings.parity = serial.PARITY_SPACE

def stopBitsToggled():
    global serialPort
    buttons = ui.STOP_BITS.findChildren(QtGui.QRadioButton)
    for button in buttons:
        if button.isChecked():
            print "Stop Bits: " + button.text()
            if button.text() == '1':
                serialSettings.stopBits = serial.STOPBITS_ONE
            if button.text() == '1.5':
                serialSettings.stopBits = serial.STOPBITS_ONE_POINT_FIVE
            if button.text() == '2':
                serialSettings.stopBits = serial.STOPBITS_TWO

def handShakingToggled():
    buttons = ui.HANDSHAKING.findChildren(QtGui.QRadioButton)
    for button in buttons:
        if button.isChecked():
            print "Handshaking: " + button.text()

def connectRadioButtons(groupBox, function):
    buttons = groupBox.findChildren(QtGui.QRadioButton)
    for button in buttons:
        button.clicked.connect(function)

class KeyPressEater(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            ch = event.text().encode('latin-1')
            if len(ch):
                #send serial here
                print "Key Press: " , ch
                print "Key Length:" , len(ch)
                if ch == chr(13):
                    print "send: carrige return"
                    serialPort.write(chr(10))
                if connected == True:
                    serialPort.write(ch)

        return QtCore.QObject.eventFilter(self, obj, event)

def serialPortConnected():
    global serialPort
    global connected
    if connected == True:
        serialPort.close()
        fRunner.timer.stop()
        connected = False
        ui.CONNECT_BUTTON.setText("Connect")
        ui.COM_PORT.setDisabled(False)
        ui.BAUD_RATE.setDisabled(False)
        ui.DATA_BITS.setDisabled(False)
        ui.PARITY.setDisabled(False)
        ui.STOP_BITS.setDisabled(False)
        ui.HANDSHAKING.setDisabled(True)
        ui.FILE_CONTROL_BUTTON.setDisabled(True)
        ui.LINE_BY_LINE_CHECK_BOX.setDisabled(False)
        ui.BYTE_DELAY_SPIN_BOX.setDisabled(False)

    else:
        serialSettings.port = ui.COM_PORT_SELECTOR.currentText()
        print "opening serial port: ", serialSettings.port
        serialPort = serial.Serial(serialSettings.port, serialSettings.baud, serialSettings.byteSize, serialSettings.parity, serialSettings.stopBits, serialSettings.time, xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False, interCharTimeout=None)
        connected = True
        ui.CONNECT_BUTTON.setText("Disconnect")
        ui.COM_PORT.setDisabled(True)
        ui.BAUD_RATE.setDisabled(True)
        ui.DATA_BITS.setDisabled(True)
        ui.PARITY.setDisabled(True)
        ui.STOP_BITS.setDisabled(True)
        ui.HANDSHAKING.setDisabled(True)
        ui.FILE_CONTROL_BUTTON.setDisabled(False)
        ui.LINE_BY_LINE_CHECK_BOX.setDisabled(False)
        ui.BYTE_DELAY_SPIN_BOX.setDisabled(False)

class serialSettingsClass():
    baud = None
    byteSize = None
    parity = None
    stopBits = None
    time = 0
    port = None

def list_serial_ports():
    system_name = platform.system()
    if system_name == "Windows":
        # Scan for available ports.
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append(i)
                s.close()
            except serial.SerialException:
                pass
        return available
    elif system_name == "Darwin":
        # Mac
        return glob.glob('/dev/tty*') + glob.glob('/dev/cu*')
    else:
        # Assume Linux or something else
        return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')

def scan():
    system_name = platform.system()
    ports = list_serial_ports()
    print ports
    for x in range(0, ui.COM_PORT_SELECTOR.count()):
        ui.COM_PORT_SELECTOR.removeItem(0)
    for i in ports:
        if system_name == "Windows":
            ui.COM_PORT_SELECTOR.addItem("COM"+ str(i+1))
        else:
            ui.COM_PORT_SELECTOR.addItem(i)

def receivePort():
    global connected
    global serialPort
    #print "timer"
    if connected:
        text = serialPort.read()
        if text != '':
            if text == chr(10):
                print "receved: new line:"
            if text == chr(13):
                print "receved: carrige retrun"
            ui.receiveEditCursor.movePosition(ui.receiveEditCursor.End)
            ui.receiveEditCursor.insertText(text)
            ui.receiveEditCursor.movePosition(ui.receiveEditCursor.End)
            ui.RECEIVE_EDIT.setTextCursor(ui.receiveEditCursor)
            #ui.RECEIVE_EDIT.appendPlainText(serialPort.read())

def fileDialog():
    system_name = platform.system()
    if system_name == "Windows":
        pathName = os.getenv("UserProfile")
        print pathName
        #pathName = "%UserProfile%"
    else:
        pathName = pathName = os.getenv('$HOME')
    (fName,none) = QtGui.QFileDialog.getOpenFileName(ui, 'Open File', pathName)
    ui.FILE_EDIT.setText(fName)

class fileRunner:
    def __init__(self):
        self.fd = None
        self.state = 'idle'
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextChar)

    def fileController(self):
        if self.state == 'idle':
            fName = ui.FILE_EDIT.text()
            ui.FILE_EDIT.setDisabled(True)
            ui.CHOOSE_FILE.setDisabled(True)
            ui.BYTE_DELAY_SPIN_BOX.setDisabled(True)
            self.fd = open(fName, 'rU')
            if ui.LINE_BY_LINE_CHECK_BOX.checkState():
                self.state = 'nextLine'
                ui.FILE_CONTROL_BUTTON.setText('Next Line')
                ui.LINE_BY_LINE_CHECK_BOX.setDisabled(True)
            else:
                self.state = 'run'
                ui.FILE_CONTROL_BUTTON.setText('Pause')
                ui.LINE_BY_LINE_CHECK_BOX.setDisabled(True)
                self.timer.start(ui.BYTE_DELAY_SPIN_BOX.value())

        elif self.state == 'nextLine':
            self.nextLine()
        elif self.state == 'run':
            ui.BYTE_DELAY_SPIN_BOX.setDisabled(False)
            self.state = 'pause'
            self.timer.stop()
            ui.FILE_CONTROL_BUTTON.setText('Run')
        elif self.state == 'pause':
            self.state = 'run'
            ui.BYTE_DELAY_SPIN_BOX.setDisabled(True)
            self.timer.start(ui.BYTE_DELAY_SPIN_BOX.value())
            ui.FILE_CONTROL_BUTTON.setText('Pause')

    def nextChar(self):
        ch = self.fd.read(1)
        if ch == '':
            self.fd.close()
            self.state = 'idle'
            ui.FILE_CONTROL_BUTTON.setText('Start')
            ui.FILE_EDIT.setDisabled(False)
            ui.CHOOSE_FILE.setDisabled(False)
            ui.BYTE_DELAY_SPIN_BOX.setDisabled(False)
            ui.LINE_BY_LINE_CHECK_BOX.setDisabled(False)
            self.timer.stop()
        else:
            serialPort.write(ch)
            ui.transmitEditCursor.movePosition(ui.transmitEditCursor.End)
            ui.transmitEditCursor.insertText(ch)
            ui.transmitEditCursor.movePosition(ui.transmitEditCursor.End)
            ui.TRANSMIT_EDIT.setTextCursor(ui.transmitEditCursor)

    def nextLine(self):
        lineText = self.fd.readline()
        if lineText == '':
            self.fd.close()
            self.state = 'idle'
            ui.FILE_CONTROL_BUTTON.setText('Start')
            ui.FILE_EDIT.setDisabled(False)
            ui.CHOOSE_FILE.setDisabled(False)
            ui.BYTE_DELAY_SPIN_BOX.setDisabled(True)
            ui.LINE_BY_LINE_CHECK_BOX.setDisabled(False)
        else:
            serialPort.write(lineText)
            ui.transmitEditCursor.movePosition(ui.transmitEditCursor.End)
            ui.transmitEditCursor.insertText(lineText)
            ui.transmitEditCursor.movePosition(ui.transmitEditCursor.End)
            ui.TRANSMIT_EDIT.setTextCursor(ui.transmitEditCursor)


def lineByLineChange():
    if ui.LINE_BY_LINE_CHECK_BOX.checkState():
        ui.BYTE_DELAY_SPIN_BOX.setValue(0)
        ui.BYTE_DELAY_SPIN_BOX.setDisabled(True)
    else:
        ui.BYTE_DELAY_SPIN_BOX.setValue(10)
        ui.BYTE_DELAY_SPIN_BOX.setDisabled(False)

def loadUiWidget(uifilename, parent=None):
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui

def main():
    app = QtGui.QApplication(sys.argv)
    global ui
    ui = loadUiWidget("crossTerm.ui")
    global fRunner
    fRunner = fileRunner()

    global serialPort

    global connected
    connected = False

    global serialSettings
    serialSettings = serialSettingsClass()

    keyFilter = KeyPressEater(ui)
    ui.transmitEditCursor = QtGui.QTextCursor(ui.TRANSMIT_EDIT.document())
    ui.receiveEditCursor = QtGui.QTextCursor(ui.RECEIVE_EDIT.document())

    ui.QUIT_BUTTON.clicked.connect(cleanUp)
    ui.CONNECT_BUTTON.clicked.connect(serialPortConnected)
    ui.RESCAN_BUTTON.clicked.connect(scan)
    ui.CHOOSE_FILE.clicked.connect(fileDialog)
    ui.FILE_CONTROL_BUTTON.clicked.connect(fRunner.fileController)
    ui.LINE_BY_LINE_CHECK_BOX.stateChanged.connect(lineByLineChange)
    scan()
    #ui.portSelectCombo.activated[str].connect()

    connectRadioButtons(ui.BAUD_RATE, baudToggled)
    connectRadioButtons(ui.DATA_BITS, dataBitsToggled)
    connectRadioButtons(ui.PARITY, parityToggled)
    connectRadioButtons(ui.STOP_BITS, stopBitsToggled)
    connectRadioButtons(ui.HANDSHAKING, handShakingToggled)
    
    ui.BAUD_9600.setChecked(True)
    baudToggled()
    ui.DATA_BITS_8.setChecked(True)
    dataBitsToggled()
    ui.PARITY_NONE.setChecked(True)
    parityToggled()
    ui.STOP_BITS_1.setChecked(True)
    stopBitsToggled()
    ui.HANDSHAKING_NONE.setChecked(True)
    handShakingToggled()

    ui.TRANSMIT_EDIT.installEventFilter(keyFilter)
    ui.HANDSHAKING.setDisabled(True)
    ui.STOP_BITS_1_5.setDisabled(True)
    ui.BAUD_CUSTOM.setDisabled(True)
    ui.FILE_CONTROL_BUTTON.setDisabled(True)

    timer = QtCore.QTimer()
    timer.timeout.connect(receivePort)
    timer.start(1)

    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
