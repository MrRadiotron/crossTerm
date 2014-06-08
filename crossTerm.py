#! /usr/bin/python

import faulthandler
import sys, os
from PySide import QtCore, QtGui, QtUiTools
from PySide.QtCore import QThread
import serial
import platform, glob
import threading

def closeEvent(self, event):
    event.ignore()
    cleanUp()

def cleanUp():
    global connected
    global serial_thread
    if connected:
        connected = False
        while serial_thread.running:
            pass
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

def transmit_bar_toggled():
    global transmit_line_ending
    buttons = ui.TRANSMIT_BAR.findChildren(QtGui.QRadioButton)
    for button in buttons:
        if button.isChecked():
            print "Transmit line ending: " + button.text()
            transmit_line_ending = button.text()
            """if button.text() == 'CR':
                serialSettings.parity = serial.PARITY_NONE
            if button.text() == 'LF':
                serialSettings.parity = serial.PARITY_EVEN
            if button.text() == 'CRLF':
                serialSettings.parity = serial.PARITY_ODD"""
def receive_bar_toggled():
    global receive_line_ending
    buttons = ui.RECEIVE_BAR.findChildren(QtGui.QRadioButton)
    for button in buttons:
        if button.isChecked():
            print "receive line ending: " + button.text()
            receive_line_ending = button.text()

def connectRadioButtons(groupBox, function):
    buttons = groupBox.findChildren(QtGui.QRadioButton)
    for button in buttons:
        button.clicked.connect(function)

class KeyPressEater(QtCore.QObject):
    def eventFilter(self, obj, event):
        global connected
        if event.type() == QtCore.QEvent.ContextMenu:
            print "paste event"
        if event.type() == QtCore.QEvent.KeyPress:
            if (event.matches(QtGui.QKeySequence.Paste) or event.matches(QtGui.QKeySequence.Paste)):
                clipboard = QtGui.QApplication.clipboard()
                ch = clipboard.text().encode('utf-8')
                print ch
            else:
                ch = event.text().encode('utf-8')

            if len(ch):
                #send serial here
                print "Key Press: " , ch
                print "Key Length:" , len(ch)

                if ch == chr(13):
                    if transmit_line_ending == "LF":
                        print "send: LF"
                        ch = chr(10)
                    elif transmit_line_ending == "CRLF":
                        print "send: CRLF"
                        ch = "\r\n"
                        #ch = chr(13)
                        #ch.join(chr(10))
                    else:
                        print "send: CR"

                elif ch == chr(10):
                    if transmit_line_ending == "CR":
                        print "send: CR"
                        ch = chr(13)
                    elif transmit_line_ending == "CRLF":
                        print "send: CRLF"
                        ch = "\r\n"
                        #ch = chr(13)
                        #ch.join(chr(10))
                    else:
                        print "send: LF"

                if connected == True:
                    try:
                        serialPort.write(ch)
                    except serial.SerialException, e:
                        connected = False

        return QtCore.QObject.eventFilter(self, obj, event)

def serialPortConnected():
    global serialPort
    global connected
    global serial_thread
    if connected == True:
        connected = False
        fRunner.timer.stop()
        while serial_thread.running:
            pass
        serialPort.close()
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
        #ui.TRANSMIT_BAR.setDisabled(False)
        #ui.RECEIVE_BAR.setDisabled(False)

    else:
        serialSettings.port = ui.COM_PORT_SELECTOR.currentText()
        print "opening serial port: ", serialSettings.port
        serialPort = serial.Serial(serialSettings.port, serialSettings.baud, serialSettings.byteSize, serialSettings.parity, serialSettings.stopBits, serialSettings.time, xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False, interCharTimeout=None)
        connected = True
        serial_thread = receivePort()
        serial_thread.start()
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
        #ui.TRANSMIT_BAR.setDisabled(True)
        #ui.RECEIVE_BAR.setDisabled(True)

class serialSettingsClass():
    baud = None
    byteSize = None
    parity = None
    stopBits = None
    time = None
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

class receivePort(QThread):
    def __init__(self):
        self.running = False
        QThread.__init__(self)

    def run(self):
        global connected
        global serialPort
        global last_char
        self.running = True

        while connected:
            try:
                print "thread here"
                text = serialPort.read(1)
                #if text != '':
                if text == chr(10):
                    print "received: LF"
                    if receive_line_ending == "CR":
                        text = ''
                    elif receive_line_ending == "CRLF":
                        if last_char:
                            print "received: CRLF"
                            text = chr(10)
                        else:
                            text = ''
                    last_char = False
                elif text == chr(13):
                    print "received: CR"
                    last_char = True
                    if receive_line_ending == "LF":
                        text = ''
                    elif receive_line_ending == "CRLF":
                        text = ''
                else:
                    last_char = False

                ui.receiveEditCursor.movePosition(ui.receiveEditCursor.End)
                ui.receiveEditCursor.insertText(text)
                ui.receiveEditCursor.movePosition(ui.receiveEditCursor.End)
                ui.RECEIVE_EDIT.setTextCursor(ui.receiveEditCursor)
                #ui.RECEIVE_EDIT.appendPlainText(serialPort.read())
            except serial.SerialException, e:
                connected = False



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
            try:
                serialPort.write(lineText)
            except serial.SerialException, e:
                connected = False

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

def clear_plain_text(plain_text):
    plain_text.setPlainText("")

def clear_transmit():
    clear_plain_text(ui.TRANSMIT_EDIT)

def clear_receive():
    clear_plain_text(ui.RECEIVE_EDIT)

def loadUiWidget(uifilename, parent=None):
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui

class my_plain_edit(QtGui.QPlainTextEdit):
    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        print "custom context menu"
        x = menu.actions()
        for i in x:
            print "text: " + i.text().encode('utf-8')
            if(i.text().encode('utf-8').lower().find("paste")):
                i.triggered.connect(self.context_paste)

        menu.exec_(event.globalPos())

    def context_paste(self):
        print "context paint"
        clipboard = QtGui.QApplication.clipboard()
        ch = clipboard.text().encode('utf-8')
        print ch

        if connected == True:
            try:
                serialPort.write(ch)
            except serial.SerialException, e:
                connected = False


def main():
    app = QtGui.QApplication(sys.argv)
    global ui
    ui = loadUiWidget("crossTerm.ui")

    ui.TRANSMIT_EDIT.setParent(None)
    ui.TRANSMIT_EDIT = my_plain_edit()

    ui.splitter.addWidget(ui.TRANSMIT_EDIT)


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
    ui.TRANSMIT_CLEAR_BUTTON.clicked.connect(clear_transmit)
    ui.RECEIVE_CLEAR_BUTTON.clicked.connect(clear_receive)
    scan()
    #ui.portSelectCombo.activated[str].connect()

    connectRadioButtons(ui.BAUD_RATE, baudToggled)
    connectRadioButtons(ui.DATA_BITS, dataBitsToggled)
    connectRadioButtons(ui.PARITY, parityToggled)
    connectRadioButtons(ui.STOP_BITS, stopBitsToggled)
    connectRadioButtons(ui.HANDSHAKING, handShakingToggled)
    connectRadioButtons(ui.TRANSMIT_BAR, transmit_bar_toggled)
    connectRadioButtons(ui.RECEIVE_BAR, receive_bar_toggled)
    
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
    ui.TRANSMIT_LF.setChecked(True)
    transmit_bar_toggled()
    ui.RECEIVE_LF.setChecked(True)
    receive_bar_toggled()

    ui.TRANSMIT_EDIT.installEventFilter(keyFilter)
    ui.HANDSHAKING.setDisabled(True)
    ui.STOP_BITS_1_5.setDisabled(True)
    ui.BAUD_CUSTOM.setDisabled(True)
    ui.FILE_CONTROL_BUTTON.setDisabled(True)

    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    faulthandler.enable()
    main()
