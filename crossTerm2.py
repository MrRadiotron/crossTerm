#! /usr/bin/python

import sys
import os
import faulthandler

import platform
import glob
import serial
import threading
from PySide import QtCore, QtGui, QtUiTools

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
			serial_port.serial_port.write(lineText)

			ui.transmitEditCursor.movePosition(ui.transmitEditCursor.End)
			ui.transmitEditCursor.insertText(lineText)
			ui.transmitEditCursor.movePosition(ui.transmitEditCursor.End)
			ui.TRANSMIT_EDIT.setTextCursor(ui.transmitEditCursor)

class KeyPressEater(QtCore.QObject):
	def eventFilter(self, obj, event):
		global serial_port
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

				if serial_port.connected == True:
					serial_port.serial_port.write(ch)

		return QtCore.QObject.eventFilter(self, obj, event)

def baudToggled():
	global serial_port
	buttons = ui.BAUD_RATE.findChildren(QtGui.QRadioButton)
	for button in buttons:
		if button.isChecked():
			print "Baud Rate: " + button.text()
			serial_port.serial_settings.baud = int(button.text())

def dataBitsToggled():
	global serial_port
	buttons = ui.DATA_BITS.findChildren(QtGui.QRadioButton)
	for button in buttons:
		if button.isChecked():
			print "Data Bits: " + button.text()
			if button.text() == '5':
				serial_port.serial_settings.byteSize = serial.FIVEBITS
			elif button.text() == '6':
				serial_port.serial_settings.byteSize = serial.SIXBITS
			elif button.text() == '7':
				serial_port.serial_settings.byteSize = serial.SEVENBITS
			elif button.text() == '8':
				serial_port.serial_settings.byteSize = serial.EIGHTBITS

def parityToggled():
	global serial_port
	buttons = ui.PARITY.findChildren(QtGui.QRadioButton)
	for button in buttons:
		if button.isChecked():
			print "Parity: " + button.text()
			if button.text() == 'none':
				serial_port.serial_settings.parity = serial.PARITY_NONE
			if button.text() == 'even':
				serial_port.serial_settings.parity = serial.PARITY_EVEN
			if button.text() == 'odd':
				serial_port.serial_settings.parity = serial.PARITY_ODD
			if button.text() == 'mark':
				serial_port.serial_settings.parity = serial.PARITY_MARK
			if button.text() == 'space':
				serial_port.serial_settings.parity = serial.PARITY_SPACE

def stopBitsToggled():
	global serial_port
	buttons = ui.STOP_BITS.findChildren(QtGui.QRadioButton)
	for button in buttons:
		if button.isChecked():
			print "Stop Bits: " + button.text()
			if button.text() == '1':
				serial_port.serial_settings.stopBits = serial.STOPBITS_ONE
			if button.text() == '1.5':
				serial_port.serial_settings.stopBits = serial.STOPBITS_ONE_POINT_FIVE
			if button.text() == '2':
				serial_port.serial_settings.stopBits = serial.STOPBITS_TWO

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
			serial_port.serial_settings.parity = serial.PARITY_NONE
			if button.text() == 'LF':
			serial_port.serial_settings.parity = serial.PARITY_EVEN
			if button.text() == 'CRLF':
			serial_port.serial_settings.parity = serial.PARITY_ODD"""

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

def cleanUp():
	global serial_port
	if serial_port.connected:
		serial_port.disconnect_port()
	if fRunner.fd != None:
		fRunner.fd.close()
	QtCore.QCoreApplication.instance().quit()

class cross_term_serial_port:
	def __init__(self, ui):
		self.ui = ui
		self.connected = False
		self.serial_settings = serial_Settings_Class()

	def connect_port(self):
		print "opening serial port: " + self.serial_settings.port
		try:
			self.serial_port = serial.Serial(self.serial_settings.port, self.serial_settings.baud, self.serial_settings.byteSize, self.serial_settings.parity, self.serial_settings.stopBits, self.serial_settings.time, self.serial_settings.xonxoff, self.serial_settings.rtscts, self.serial_settings.writeTimeout, self.serial_settings.dsrdtr, self.serial_settings.interCharTimeout)
			self.connected = True
		except serial.SerialException, e:
			self.connected = False
			print "serial exceptiont" + e

		if self.connected:
			self.serial_thread = threading.Thread(target=self.recieve_port, args=([ui]))
			self.serial_thread.start()

	def disconnect_port(self):
		self.connected = False
		self.serial_thread.join()
		self.serial_port.close()

	def recieve_port(self, ui):
		while self.connected:
			try:
				print "serial thread here:"
				text = self.serial_port.read(1)
				if text != '':
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

		print "Serial Disconnected"

	def serial_port_connected(self):
		if self.connected == True:
			self.disconnect_port()
			if self.connected == False:
				fRunner.timer.stop()
				self.ui.CONNECT_BUTTON.setText("Connect")
				self.ui.COM_PORT.setDisabled(False)
				self.ui.BAUD_RATE.setDisabled(False)
				self.ui.DATA_BITS.setDisabled(False)
				self.ui.PARITY.setDisabled(False)
				self.ui.STOP_BITS.setDisabled(False)
				self.ui.HANDSHAKING.setDisabled(True)
				self.ui.FILE_CONTROL_BUTTON.setDisabled(True)
				self.ui.LINE_BY_LINE_CHECK_BOX.setDisabled(False)
				self.ui.BYTE_DELAY_SPIN_BOX.setDisabled(False)
				#ui.TRANSMIT_BAR.setDisabled(False)
				#ui.RECEIVE_BAR.setDisabled(False)

		else:
			self.serial_settings.port = ui.COM_PORT_SELECTOR.currentText()
			self.connect_port()
			if self.connected:
				self.ui.CONNECT_BUTTON.setText("Disconnect")
				self.ui.COM_PORT.setDisabled(True)
				self.ui.BAUD_RATE.setDisabled(True)
				self.ui.DATA_BITS.setDisabled(True)
				self.ui.PARITY.setDisabled(True)
				self.ui.STOP_BITS.setDisabled(True)
				self.ui.HANDSHAKING.setDisabled(True)
				self.ui.FILE_CONTROL_BUTTON.setDisabled(False)
				self.ui.LINE_BY_LINE_CHECK_BOX.setDisabled(False)
				self.ui.BYTE_DELAY_SPIN_BOX.setDisabled(False)
				#ui.TRANSMIT_BAR.setDisabled(True)
				#ui.RECEIVE_BAR.setDisabled(True)

class serial_Settings_Class():
	baud = None
	byteSize = None
	parity = None
	stopBits = None
	time = None
	port = None
	xonxoff=False
	rtscts=False
	writeTimeout=None
	dsrdtr=False
	interCharTimeout=None

def loadUiWidget(uifilename, parent=None):
	loader = QtUiTools.QUiLoader()
	uifile = QtCore.QFile(uifilename)
	uifile.open(QtCore.QFile.ReadOnly)
	ui = loader.load(uifile, parent)
	uifile.close()
	return ui


class my_plain_edit(QtGui.QPlainTextEdit):
	def __init__(self, serial_port):
		self.serial_port = serial_port
		super(my_plain_edit, self).__init__()

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
		for c in ch:
			if self.serial_port.connected == True:
				self.serial_Port.write(ch)


def main():
	app = QtGui.QApplication(sys.argv)
	global ui

	ui = loadUiWidget("crossTerm.ui")

	global serial_port
	serial_port = cross_term_serial_port(ui)

	ui.TRANSMIT_EDIT.setParent(None)
	ui.TRANSMIT_EDIT = my_plain_edit(serial_port)

	ui.splitter.addWidget(ui.TRANSMIT_EDIT)

	global fRunner
	fRunner = fileRunner()

	keyFilter = KeyPressEater(ui.TRANSMIT_EDIT)
	ui.transmitEditCursor = QtGui.QTextCursor(ui.TRANSMIT_EDIT.document())
	ui.receiveEditCursor = QtGui.QTextCursor(ui.RECEIVE_EDIT.document())

	ui.QUIT_BUTTON.clicked.connect(cleanUp)
	ui.CONNECT_BUTTON.clicked.connect(serial_port.serial_port_connected)
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



