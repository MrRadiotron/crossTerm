#! /usr/bin/python

import sys
from PySide import QtGui, QtCore
import serial
import platform, glob



class uiClass(QtGui.QWidget):

    def __init__(self):
        super(uiClass, self).__init__()

        self.initUI()

    def initUI(self):

        self.connectButton = QtGui.QPushButton("Connect")
        self.reScanButton = QtGui.QPushButton("ReScan")
        self.helpButton = QtGui.QPushButton("Help")
        self.aboutButton = QtGui.QPushButton("About")
        self.buttonVBOXSpacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.quitButton = QtGui.QPushButton("Quit")

        self.buttonFrame = QtGui.QFrame()
        self.buttonFrame.setMaximumSize(QtCore.QSize(16777215, 172))
        self.buttonFrame.setMinimumSize(QtCore.QSize(111, 16777215))
        self.buttonVBox = QtGui.QVBoxLayout(self.buttonFrame)
        self.buttonVBox.addWidget(self.connectButton)
        self.buttonVBox.addWidget(self.reScanButton)
        self.buttonVBox.addWidget(self.helpButton)
        self.buttonVBox.addWidget(self.aboutButton)
        self.buttonVBox.addItem(self.buttonVBOXSpacer)
        self.buttonVBox.addWidget(self.quitButton)        

        self.portSelectCombo = QtGui.QComboBox()
        self.comSelectSpacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        self.comSelectVBox = QtGui.QVBoxLayout()
        self.comSelectVBox.addWidget(self.portSelectCombo)
        self.comSelectVBox.addItem(self.comSelectSpacer)

        self.comSelectGroupBox = QtGui.QGroupBox()
        self.comSelectGroupBox.setMaximumSize(QtCore.QSize(16777215, 172))
        self.comSelectGroupBox.setMinimumSize(QtCore.QSize(150, 16777215))
        self.comSelectGroupBox.setLayout(self.comSelectVBox)
        self.comSelectGroupBox.setTitle('COM Port')

        self.baud600Radio = QtGui.QRadioButton('600')
        self.baud1200Radio = QtGui.QRadioButton('1200')
        self.baud2400Radio = QtGui.QRadioButton('2400')
        self.baud4800Radio = QtGui.QRadioButton('4800')
        self.baud9600Radio = QtGui.QRadioButton('9600')
        self.baud14400Radio = QtGui.QRadioButton('14400')
        self.baud19200Radio = QtGui.QRadioButton('19200')
        self.baud28800Radio = QtGui.QRadioButton('28800')
        self.baud38400Radio = QtGui.QRadioButton('38400')
        self.baud56000Radio = QtGui.QRadioButton('56000')
        self.baud57600Radio = QtGui.QRadioButton('57600')
        self.baud115200Radio = QtGui.QRadioButton('115200')
        self.baud128000Radio = QtGui.QRadioButton('128000')
        self.baud256000Radio = QtGui.QRadioButton('256000')
        self.baudCustomRadio = QtGui.QRadioButton('custom')

        self.baudGrid = QtGui.QGridLayout()
        self.baudGrid.addWidget(self.baud600Radio, 0, 0)
        self.baudGrid.addWidget(self.baud1200Radio, 1, 0)
        self.baudGrid.addWidget(self.baud2400Radio, 2, 0)
        self.baudGrid.addWidget(self.baud4800Radio, 3, 0)
        self.baudGrid.addWidget(self.baud9600Radio, 4, 0)
        self.baudGrid.addWidget(self.baud14400Radio, 0 ,1)
        self.baudGrid.addWidget(self.baud19200Radio, 1, 1)
        self.baudGrid.addWidget(self.baud28800Radio, 2, 1)
        self.baudGrid.addWidget(self.baud38400Radio, 3, 1)
        self.baudGrid.addWidget(self.baud56000Radio, 4, 1)
        self.baudGrid.addWidget(self.baud57600Radio, 0, 2)
        self.baudGrid.addWidget(self.baud115200Radio, 1 ,2)
        self.baudGrid.addWidget(self.baud128000Radio, 2, 2)
        self.baudGrid.addWidget(self.baud256000Radio, 3, 2)
        self.baudGrid.addWidget(self.baudCustomRadio, 4, 2)

        self.baudSelectGroupBox = QtGui.QGroupBox()
        self.baudSelectGroupBox.setLayout(self.baudGrid)
        self.baudSelectGroupBox.setTitle('Baud Rate')

        self.dataBits5 = QtGui.QRadioButton('5')
        self.dataBits6 = QtGui.QRadioButton('6')
        self.dataBits7 = QtGui.QRadioButton('7')
        self.dataBits8 = QtGui.QRadioButton('8')

        self.dataBitsVBox = QtGui.QVBoxLayout()
        self.dataBitsVBox.addWidget(self.dataBits5)
        self.dataBitsVBox.addWidget(self.dataBits6)
        self.dataBitsVBox.addWidget(self.dataBits7)
        self.dataBitsVBox.addWidget(self.dataBits8)

        self.dataBitsGroupBox = QtGui.QGroupBox('Data Bits')
        self.dataBitsGroupBox.setLayout(self.dataBitsVBox)

        self.parityNoneRadio = QtGui.QRadioButton('none')
        self.parityOddRadio = QtGui.QRadioButton('odd')
        self.parityEvenRadio = QtGui.QRadioButton('even')
        self.parityMarkRadio = QtGui.QRadioButton('mark')
        self.paritySpaceRadio = QtGui.QRadioButton('space')

        self.parityVBox = QtGui.QVBoxLayout()
        self.parityVBox.addWidget(self.parityNoneRadio)
        self.parityVBox.addWidget(self.parityOddRadio)
        self.parityVBox.addWidget(self.parityEvenRadio)
        self.parityVBox.addWidget(self.parityMarkRadio)
        self.parityVBox.addWidget(self.paritySpaceRadio)

        self.parityGroupBox = QtGui.QGroupBox('Parity')
        self.parityGroupBox.setLayout(self.parityVBox)

        self.stopBits1 = QtGui.QRadioButton('1')
        self.stopBits1_5 = QtGui.QRadioButton('1.5')
        self.stopBits2 = QtGui.QRadioButton('2')

        self.stopBitsVBox = QtGui.QVBoxLayout()
        self.stopBitsVBox.addWidget(self.stopBits1)
        self.stopBitsVBox.addWidget(self.stopBits1_5)
        self.stopBitsVBox.addWidget(self.stopBits2)

        self.stopBitsGroupBox = QtGui.QGroupBox('Stop Bits')
        self.stopBitsGroupBox.setLayout(self.stopBitsVBox)

        self.handshakingNone = QtGui.QRadioButton('none')
        self.handshakingRTSCTS = QtGui.QRadioButton('RTS/CTS')
        self.handshakingXONXOFF = QtGui.QRadioButton('XON/XOFF')
        self.handshakingRTSCTSXONXOFF = QtGui.QRadioButton('RTS/CTS+XON/XOFF')
        self.handshakingRTSOnTx = QtGui.QRadioButton('RTS on Tx')
        self.handshakingInvert = QtGui.QCheckBox('invert')

        self.handshakingHBox = QtGui.QHBoxLayout()
        self.handshakingHBox.addWidget(self.handshakingRTSOnTx)
        self.handshakingHBox.addWidget(self.handshakingInvert)

        self.handshakingVBox = QtGui.QVBoxLayout()
        self.handshakingVBox.addWidget(self.handshakingNone)
        self.handshakingVBox.addWidget(self.handshakingRTSCTS)
        self.handshakingVBox.addWidget(self.handshakingXONXOFF)
        self.handshakingVBox.addWidget(self.handshakingRTSCTSXONXOFF)
        self.handshakingVBox.addLayout(self.handshakingHBox)

        self.handshakingGroupBox = QtGui.QGroupBox('Handshaking')
        self.handshakingGroupBox.setLayout(self.handshakingVBox)

        self.HBoxSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        self.topHBox = QtGui.QHBoxLayout()
        self.topHBox.addWidget(self.buttonFrame)
        self.topHBox.addWidget(self.comSelectGroupBox)
        self.topHBox.addWidget(self.baudSelectGroupBox)
        self.topHBox.addWidget(self.dataBitsGroupBox)
        self.topHBox.addWidget(self.parityGroupBox)
        self.topHBox.addWidget(self.stopBitsGroupBox)
        self.topHBox.addWidget(self.handshakingGroupBox)
        self.topHBox.addItem(self.HBoxSpacer)

        self.receiveEdit = QtGui.QPlainTextEdit()
        self.receiveEdit.setReadOnly(True)
        self.receiveEditCursor = QtGui.QTextCursor(self.receiveEdit.document())
        self.transmitEdit = QtGui.QPlainTextEdit()
        self.transmitEditCursor = QtGui.QTextCursor(self.transmitEdit.document())

        self.vboxSplitter = QtGui.QSplitter()
        self.vboxSplitter.setOrientation(QtCore.Qt.Vertical)
        self.vboxSplitter.addWidget(self.receiveEdit)
        self.vboxSplitter.addWidget(self.transmitEdit)


        self.fileEdit = QtGui.QLineEdit()        
        self.chooseFile = QtGui.QPushButton()        
        self.sendFileLayoutSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.byteDelayLabel = QtGui.QLabel()        
        self.byteDelaySpinBox = QtGui.QSpinBox()        
        self.lineByLine = QtGui.QCheckBox()        
        self.fileControl = QtGui.QPushButton()    

        self.chooseFile.setText('Choose File')
        self.byteDelayLabel.setText('Byte Delay(ms):')
        self.lineByLine.setText('Line by Line')
        self.fileControl.setText('Start')   

        self.sendFileFrame = QtGui.QWidget()
        self.sendFileLayout = QtGui.QHBoxLayout(self.sendFileFrame)
        self.sendFileLayout.setSpacing(9)
        self.sendFileLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.sendFileLayout.setContentsMargins(0, 0, 0, 0)
        self.sendFileLayout.setContentsMargins(0, 0, 0, 0)

        self.sendFileLayout.addWidget(self.fileEdit)
        self.sendFileLayout.addWidget(self.chooseFile)
        self.sendFileLayout.addItem(self.sendFileLayoutSpacer)
        self.sendFileLayout.addWidget(self.byteDelayLabel)
        self.sendFileLayout.addWidget(self.byteDelaySpinBox)
        self.sendFileLayout.addWidget(self.lineByLine)
        self.sendFileLayout.addWidget(self.fileControl)

        self.mainVBox = QtGui.QVBoxLayout()
        self.mainVBox.addLayout(self.topHBox)
        self.mainVBox.addWidget(self.vboxSplitter)
        self.mainVBox.addWidget(self.sendFileFrame)

        self.setLayout(self.mainVBox)

        self.setWindowTitle('crossTerm')
        self.show()

    def closeEvent(self, event):
        event.ignore()
        cleanUp()

def cleanUp():
    global connected
    if connected:
        serialPort.close()
    fRunner.fd.close()
    QtCore.QCoreApplication.instance().quit()
    

def baudToggled():
    global serialPort
    buttons = ui.baudSelectGroupBox.findChildren(QtGui.QRadioButton)
    for button in buttons:
        if button.isChecked():
            print "Baud Rate: " + button.text()
            serialSettings.baud = int(button.text())

def dataBitsToggled():
    global serialPort
    buttons = ui.dataBitsGroupBox.findChildren(QtGui.QRadioButton)
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
    buttons = ui.parityGroupBox.findChildren(QtGui.QRadioButton)
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
    buttons = ui.stopBitsGroupBox.findChildren(QtGui.QRadioButton)
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
    buttons = ui.handshakingGroupBox.findChildren(QtGui.QRadioButton)
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
                if connected == True:
                    serialPort.write(ch)

        return QtCore.QObject.eventFilter(self, obj, event)

def serialPortConnected():
    global serialPort
    global connected
    if connected == True:
        serialPort.close()
        connected = False
        ui.connectButton.setText("Connect")
        ui.comSelectGroupBox.setDisabled(False)
        ui.baudSelectGroupBox.setDisabled(False)
        ui.dataBitsGroupBox.setDisabled(False)
        ui.parityGroupBox.setDisabled(False)
        ui.stopBitsGroupBox.setDisabled(False)
        ui.handshakingGroupBox.setDisabled(True)
        ui.fileControl.setDisabled(False)
        ui.lineByLine.setDisabled(False)
        ui.byteDelaySpinBox.setDisabled(False)

    else:
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
        ui.fileControl.setDisabled(True)
        ui.lineByLine.setDisabled(True)
        ui.byteDelaySpinBox.setDisabled(True)

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
    ports = list_serial_ports()
    print ports
    for x in range(0, ui.portSelectCombo.count()):
        ui.portSelectCombo.removeItem(0)
    for i in ports:
        ui.portSelectCombo.addItem(i)

def receivePort():
    global connected
    global serialPort
    #print "timer"
    if connected:
        ui.receiveEditCursor.movePosition(ui.receiveEditCursor.End)
        ui.receiveEditCursor.insertText(serialPort.read())
        ui.receiveEditCursor.movePosition(ui.receiveEditCursor.End)
        ui.receiveEdit.setTextCursor(ui.receiveEditCursor)
        #ui.receiveEdit.appendPlainText(serialPort.read())

def fileDialog():
    (fName,none) = QtGui.QFileDialog.getOpenFileName(ui, 'Open File', '/home')
    ui.fileEdit.setText(fName)

class fileRunner:
    def fileController(self):
        fName = ui.fileEdit.text()
        ui.fileEdit.setDisabled(True)
        ui.chooseFile.setDisabled(True)
        ui.byteDelaySpinBox.setDisabled(True)
        if ui.lineByLine.isChecked:
            ui.fileControl.setText('Next Line')
            ui.fileControl.clicked.connect(self.nextLine)
        self.fd = open(fName, 'rU')

    def nextLine(self):
        lineText = self.fd.readline()
        print lineText

        #serialPort.write(lineText)
        ui.transmitEditCursor.movePosition(ui.transmitEditCursor.End)
        ui.transmitEditCursor.insertText(lineText)
        ui.transmitEditCursor.movePosition(ui.transmitEditCursor.End)
        ui.transmitEdit.setTextCursor(ui.transmitEditCursor)


def lineByLineChange():
    if ui.lineByLine.checkState():
        ui.byteDelaySpinBox.setValue(0)
        ui.byteDelaySpinBox.setDisabled(True)
    else:
        ui.byteDelaySpinBox.setValue(0)
        ui.byteDelaySpinBox.setDisabled(False)


def main():
    app = QtGui.QApplication(sys.argv)
    global ui
    ui = uiClass()
    global fRunner
    fRunner = fileRunner()

    global serialPort

    global connected
    connected = False

    global serialSettings
    serialSettings = serialSettingsClass()

    keyFilter = KeyPressEater(ui)

    ui.quitButton.clicked.connect(cleanUp)
    ui.connectButton.clicked.connect(serialPortConnected)
    ui.reScanButton.clicked.connect(scan)
    ui.chooseFile.clicked.connect(fileDialog)
    ui.fileControl.clicked.connect(fRunner.fileController)
    ui.lineByLine.stateChanged.connect(lineByLineChange)
    scan()
    #ui.portSelectCombo.activated[str].connect()

    connectRadioButtons(ui.baudSelectGroupBox, baudToggled)
    connectRadioButtons(ui.dataBitsGroupBox, dataBitsToggled)
    connectRadioButtons(ui.parityGroupBox, parityToggled)
    connectRadioButtons(ui.stopBitsGroupBox, stopBitsToggled)
    connectRadioButtons(ui.handshakingGroupBox, handShakingToggled)
    
    ui.baud9600Radio.setChecked(True)
    baudToggled()
    ui.dataBits8.setChecked(True)
    dataBitsToggled()
    ui.parityNoneRadio.setChecked(True)
    parityToggled()
    ui.stopBits1.setChecked(True)
    stopBitsToggled()
    ui.handshakingNone.setChecked(True)
    handShakingToggled()

    ui.transmitEdit.installEventFilter(keyFilter)
    ui.handshakingGroupBox.setDisabled(True)
    ui.stopBits1_5.setDisabled(True)
    ui.baudCustomRadio.setDisabled(True)

    timer = QtCore.QTimer()
    timer.timeout.connect(receivePort)
    timer.start(1)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
