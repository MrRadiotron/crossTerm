#! /usr/bin/python
import sys
import serial
import threading
from PySide import QtCore, QtGui, QtUiTools

class serial_port_class(object):
	def __init__(self, ui):
		print "create port"
		self.ui = ui
		self.connected = False

	def __del__(self):
		print "delete port"
		self.disconnect_port()

	def connect_port(self):
		print "connect_port"
		try:
			self.serial_port = serial.Serial("/dev/tty.usbmodem1451", 9600, timeout = None)
			self.connected = True
		except serial.SerialException, e:
			self.connected = False

		if self.connected:
			print "launch thread"
			self.serial_thread = threading.Thread(target=self.recieve_port, args=([self.ui]))
			self.serial_thread.start()

	def disconnect_port(self):
		print "disconnect_port"
		self.connected = False
		self.serial_thread.join()
		self.serial_port.close()

	def recieve_port(self, ui):
		print "thread_start"
		while self.connected:
			print"thread_loop"
			try:
				text = self.serial_port.read(1)
				if text != '':
					ui.plain_edit.appendPlainText(text)
			except serial.SerialException, e:
				connected = False
		print "thread_exit"



class KeyPressEater(QtCore.QObject):
	def eventFilter(self, obj, event):
		global serial_port
		if event.type() == QtCore.QEvent.KeyPress:	
			ch = event.text().encode('utf-8')
			print "got " + ch
			if serial_port.connected == True:
				print "send " + ch
				serial_port.serial_port.write(ch)

		return QtCore.QObject.eventFilter(self, obj, event)


def main():
	print "main"
	global serial_port
	app = QtGui.QApplication(sys.argv)
	ui = QtGui.QWidget()
	ui.plain_edit = QtGui.QPlainTextEdit(ui)
	keyFilter = KeyPressEater(ui)
	ui.plain_edit.installEventFilter(keyFilter)
	serial_port = serial_port_class(ui)
	serial_port.connect_port()
	ui.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
