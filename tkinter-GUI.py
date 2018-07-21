from tkinter import *
from tkinter import font
import serial
import threading
import time

conn = None
readThread = None

class connection(object):
	def __init__(self, connected = False, port = 'COM12', baud = 115200, serPort = None):
		self.connected = connected
		self.port = port #define the port
		self.baud = baud #define bit rate
		self.serPort = serPort

def connect():
	global conn
	global readThread
	conn = connection()
	conn.connected = True
	conn.serPort = serial.Serial(conn.port, conn.baud, timeout = 0)
	InitLaunchpad()
	readThread = threading.Thread(target = readPort)
	print("connected")
	TextArea.insert(END, "Connected\n")
	readThread.start()

def disconnect():
	global conn
	global readThread
	conn.connected = False
	readThread.join()
	conn = None
	print("disconnected")
	TextArea.insert(END, "Disconnected\n")

def clearTextArea():
	print("Text are cleared")
	TextArea.delete('1.0', END)

def scan():
	conn.serPort.write('\x01\x04\xFE\x03\x03\x01\x00'.encode())
	time.sleep(0.2)
	print("Scanning")

def connectStk():
	print("Connecting to Sensor Tag")


def InitLaunchpad():
	conn.serPort.write('\x01\x03\x0C\x00'.encode())
	time.sleep(0.2)
	conn.serPort.write('\x01\x00\xFE\x26\x08\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'.encode())
	time.sleep(0.2)
	conn.serPort.write('\x01\x31\xFE\x01\x15'.encode())
	time.sleep(0.2)
	conn.serPort.write('\x01\x31\xFE\x01\x16'.encode())
	time.sleep(0.2)
	conn.serPort.write('\x01\x31\xFE\x01\x1A'.encode())
	time.sleep(0.2)
	conn.serPort.write('\x01\x31\xFE\x01\x19'.encode())
	time.sleep(0.2)

#Thread functions
def handleData(data):
	print("handling data")
	TextArea.insert(END, data.decode("utf-8")+"\n")


def readPort():
	global conn
	while conn.connected:
		while conn.serPort.in_waiting > 0:
			data = conn.serPort.readline(1) #maybe add ".decode()" look up what is it for
			handleData(data)
	conn.serPort.close()




root = Tk()
root.title("Synchronization GUI")

#Frame tree to devide the space
windowFrame = Frame(root)
windowFrame.pack(fill = BOTH, expand = 1, padx = 40, pady = 20)

titleFrame = Frame(windowFrame, bg = "green")
titleFrame.pack(fill = X, pady = 5)

mainFrame = Frame(windowFrame, bg = "red")
mainFrame.pack(fill = BOTH, expand = 1, pady = 5)

optButFrame = Frame(mainFrame, bg = "blue")
optButFrame.pack(fill = Y, side = RIGHT, padx = 5)

buttonsFrame = Frame(windowFrame, bg = "green")
buttonsFrame.pack(fill = X, pady = 5)

#Add things to GUI some more
#Title and buttons
title = Label(titleFrame, text="Synchronization Data", font = "Segoe 16 bold").pack(side = LEFT)
exitBut = Button(buttonsFrame, text = "Exit", command = root.destroy).pack(side = RIGHT, ipadx = 20)
connectBut = Button(buttonsFrame, text = "Connect", command = connect).pack(side = LEFT, ipadx = 20)
disconnectBut = Button(buttonsFrame, text = "Disconnect", command = disconnect).pack(side = LEFT, ipadx = 20, padx = 30)
scanBut = Button(optButFrame, text = "Scan", command = scan).pack(ipadx = 20)
connectStkBut = Button(optButFrame, text = "Connect", command = connectStk).pack(ipadx = 20)
clearBut = Button(optButFrame, text = "Clear", command = clearTextArea).pack(side = BOTTOM, ipadx = 20)


#Text area and scrollbar
Scroll = Scrollbar(mainFrame)
TextArea = Text(mainFrame, height = 4) #heigth not releveant, for in pack it is said to occupy all the space, however if its not set the buttons below experience some problems
Scroll.pack(side=RIGHT, fill=Y)
TextArea.pack(side=LEFT, fill=BOTH)
Scroll.config(command=TextArea.yview)
TextArea.config(yscrollcommand=Scroll.set)


root.geometry("800x500+20+25")
root.mainloop()