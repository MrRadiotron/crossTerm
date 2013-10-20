#! /usr/local/bin/python

import sys
from PySide import QtGui, QtCore



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
        self.transmitEdit = QtGui.QPlainTextEdit()

        self.vboxSplitter = QtGui.QSplitter()
        self.vboxSplitter.setOrientation(QtCore.Qt.Vertical)
        self.vboxSplitter.addWidget(self.receiveEdit)
        self.vboxSplitter.addWidget(self.transmitEdit)

        self.mainVBox = QtGui.QVBoxLayout()
        self.mainVBox.addLayout(self.topHBox)
        self.mainVBox.addWidget(self.vboxSplitter)

        self.setLayout(self.mainVBox)

        self.setWindowTitle('crossTermTest1')
        self.show()

    def closeEvent(self, event):
        event.ignore()
        cleanUp()

def cleanUp():
    QtCore.QCoreApplication.instance().quit()

def baudToggled():
    buttons = ui.baudSelectGroupBox.findChildren(QtGui.QRadioButton)
    for button in buttons:
        if button.isChecked():
            print "Baud Rate: " + button.text()

def dataBitsToggled():
    buttons = ui.dataBitsGroupBox.findChildren(QtGui.QRadioButton)
    for button in buttons:
        if button.isChecked():
            print "Data Bits: " + button.text()

def parityToggled():
    buttons = ui.parityGroupBox.findChildren(QtGui.QRadioButton)
    for button in buttons:
        if button.isChecked():
            print "Parity: " + button.text()

def stopBitsToggled():
    buttons = ui.stopBitsGroupBox.findChildren(QtGui.QRadioButton)
    for button in buttons:
        if button.isChecked():
            print "Stop Bits: " + button.text()

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

        return QtCore.QObject.eventFilter(self, obj, event)


def main():
    app = QtGui.QApplication(sys.argv)
    global ui
    ui = uiClass()

    keyFilter = KeyPressEater(ui)

    ui.quitButton.clicked.connect(cleanUp)

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

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
