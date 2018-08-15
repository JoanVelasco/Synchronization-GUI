from __future__ import division
import struct
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
from tkinter import *
from tkinter import font
import serial
import threading
import time


OUT_STATE = 0
SCAN_STATE = 1
DATA_STATE = 2
CONNECTING_STATE = 3
style.use("ggplot")

handleMutex = threading.Semaphore(0)
FileList = ('S1data.txt', 'S2data.txt', 'S3data.txt', 'S4data.txt')

conn = None
readThread = None
state = OUT_STATE
sensortagList = []
macList = []

LineSeparator = "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
Information = "This file contains acceleration values of x,y and z axis!"
DateTimeNow = "Measurements taken by Joan Velasco on: " + time.strftime("%c") #%c = prints appropiate date and time representation
headerFile = LineSeparator + "\n" + Information  + "\n"+ DateTimeNow + "\n" + LineSeparator + "\n" + "Accel-x [G], Accel-y [G], Accel-z [G]" + "\n"

# w+ means --> open a file for writing and create it if it does not exist
for filename in FileList:
	with open(filename, 'w+') as file:
		file.write(headerFile)
		file.close()

figure = Figure(figsize=(5,6), dpi=70)
graphic1 = figure.add_subplot(311)
graphic2 = figure.add_subplot(312)
graphic3 = figure.add_subplot(313)
graphic1.set_ylabel('Acc X (G)')
graphic2.set_ylabel('Acc Y (G)')
graphic3.set_ylabel('Acc Z (G)')
graphic3.set_xlabel('Time (s)')


class sensorTag(object):
	def __init__(self, name, mac):
		self.name = name
		self.mac = mac
		self.handle = None
		self.xAcc = []
		self.yAcc = []
		self.zAcc = []
		self.time = []

class connection(object):
	def __init__(self, connected = False, port = 'COM12', baud = 115200, serPort = None):
		self.connected = connected
		self.port = port #define the port
		self.baud = baud #define bit rate
		self.serPort = serPort

def updateGraphs():
	graphic1.clear()
	graphic2.clear()
	graphic3.clear()
	for sensor in sensortagList:
		graphic1.plot(sensor.time, sensor.xAcc, '.-', label = sensor.name)
		graphic2.plot(sensor.time, sensor.yAcc, '.-', label = sensor.name)
		graphic3.plot(sensor.time, sensor.zAcc, '.-', label = sensor.name)
		graphic1.legend(loc = 'upper left', ncol = 4)
	canvas.draw()

def connect():
	global conn
	global readThread
	conn = connection()
	conn.connected = True
	conn.serPort = serial.Serial(conn.port, conn.baud, timeout = None, bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, xonxoff = False, rtscts = False, dsrdtr = False)
	InitLaunchpad()
	readThread = threading.Thread(target = readPort)
	readThread.daemon = True
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

def disconnectStk():
	#Disable sensors
	for sensor in sensortagList:
		conn.serPort.write(b'\x01\x92\xFD\x05' + sensor.handle + b'\x47\x00\x00')
		time.sleep(0.2)
		conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x3f\x00\x47\x00')
		time.sleep(0.2)
		conn.serPort.write(b'\x01\x8A\xFD\x04' + sensor.handle + b'\x3f\x00')
		time.sleep(0.2)
		conn.serPort.write(b'\x01\x92\xFD\x05' + sensor.handle + b'\x2f\x00\x00')
		time.sleep(0.2)
		conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x3f\x00\x40\x00')
		time.sleep(0.2)
		conn.serPort.write(b'\x01\x92\xFD\x05' + sensor.handle + b'\x37\x00\x00')
		time.sleep(0.2)
		conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x3f\x00\x00\x00')
		time.sleep(0.2)
	#Disconnect sensor tags
	for sensor in sensortagList:
		conn.serPort.write(b'\x01\x0A\xFE\x03' + sensor.handle + b'\x13')
		time.sleep(0.2)
	state = OUT_STATE

def clearTextArea():
	print("Text are cleared")
	TextArea.delete('1.0', END)

def scan():
	conn.serPort.write(b'\x01\x04\xFE\x03\x03\x01\x00')
	print("Scanning")

def startConnectStkThread():
	StkConn = threading.Thread(target = connectStk)
	StkConn.start()

def connectStk():
	global state
	if state == OUT_STATE and len(sensortagList):
		print("Connecting to Sensor Tag")
		state = CONNECTING_STATE
		for sensor in sensortagList:
			#connect to sensor tag
			conn.serPort.write(b'\x01\x09\xFE\x09\x00\x00\x00' + sensor.mac)
			handleMutex.acquire()

			#Activate notifications and configure sensors
			conn.serPort.write(b'\x01\x92\xFD\x05' + sensor.handle + b'\x53\x00\x02')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x8A\xFD\x04' + sensor.handle + b'\x51\x00')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x05' + sensor.handle + b'\x51\x00\x00')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x05' + sensor.handle + b'\x53\x00\x01')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x3d\x00\x01\x00')
			time.sleep(0.5)
			#conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x44\x00\x01\x00')
			#time.sleep(0.5)

		#Enable sensors
		for sensor in sensortagList:
			conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x3f\x00\x3f\x02')
			time.sleep(0.5)

		state = DATA_STATE
			


	else :
		print("Error: No Sensortags found, or already connected")


def InitLaunchpad():
	conn.serPort.write(b'\x01\x03\x0C\x00')
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(conn.serPort.in_waiting))
	conn.serPort.write(b'\x01\x00\xfe\x26\x08\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00')
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(9))
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(47))
	conn.serPort.write(b'\x01\x31\xFE\x01\x15')
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(11))
	conn.serPort.write(b'\x01\x31\xFE\x01\x16')
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(11))
	conn.serPort.write(b'\x01\x31\xFE\x01\x1A')
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(11))
	conn.serPort.write(b'\x01\x31\xFE\x01\x19')
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(11))

#Thread functions
def handleData(data):
	print("handling data")
	TextArea.insert(END, ''.join(" " + format(x, '02x') for x in data) + "\n")
	TextArea.see(END)


def readPort():
	global conn
	global state
	global macList
	global sensortagList
	while conn.connected:
		while conn.serPort.in_waiting > 0:
			header = conn.serPort.read(3)
			data = conn.serPort.read(header[2])
			if state != DATA_STATE:
				handleData(header + data)
			if(state == OUT_STATE):
				#Default
				if (data[0] == 0x7F and data[1] == 0x06): #Data[0] is actually the 4th byte of the transmission, the first 3 are in "header"
					TextArea.insert(END,("Scanning process started\n"))
					macList = []
					sensortagList = []
					state = SCAN_STATE

			elif(state == SCAN_STATE):
				#Messages from the scan
				if (data[0] == 0x01 and data[1] == 0x06):
					TextArea.insert(END,("Scanning process finished\n"))
					state = OUT_STATE
				elif 0x54 in data:
					#Find mac and create sensortag object
					i = data.find(0x54)
					mac = data[i-5:i+1]
					if mac not in macList:
						macList.append(mac)
						sensor = sensorTag(name = "SensorTag"+str(len(sensortagList)), mac = mac)
						sensortagList.append(sensor)
					handleData(mac)

			elif state == CONNECTING_STATE:
				if 0x54 in data:
					i = data.find(0x54)
					print(i)
					mac = data[i-5:i+1]
					print(mac)
					index = macList.index(mac)
					print(index)
					sensortagList[index].handle = data[i+1:i+3]
					print(sensortagList[index].handle)
					handleMutex.release()
					
				
			elif(state == DATA_STATE):
				#Messages from the sensortags
				if (data[0] == 0x1B and data[1] == 0x05 and data[5] == 0x14 and data[6] == 0x3C):
					accRaw = struct.unpack('<hhh', data[14:20])
					acc = [x / 4096.0 for x in accRaw]
					sensortagList[int(data[3])].xAcc.append(acc[0])
					sensortagList[int(data[3])].yAcc.append(acc[1])
					sensortagList[int(data[3])].zAcc.append(acc[2])

					time = struct.unpack('<HH', data[22:])
					timeStructured = time[1] + (time[0] / 65536)
					sensortagList[int(data[3])].time.append(timeStructured)

					TextArea.insert(END, '%.3f' % (timeStructured) + " --> " + sensortagList[int(data[3])].name + ":  " + "X: %.5f, Y: %.5f, Z: %.5f" % (acc[0], acc[1], acc[2]) + "\n")
					TextArea.see(END)

					with open(FileList[int(data[3])], 'a') as file:	#'a' is to add data to the file.
						file.write('%.3f' % (timeStructured) + " --> " + sensortagList[int(data[3])].name + ":  " + "X: %.5f, Y: %.5f, Z: %.5f" % (acc[0], acc[1], acc[2]) + "\n")
						file.close()

					if len(sensortagList[int(data[3])].xAcc) > 50:
						#Pop first element of all the arrays[handle]
						sensortagList[int(data[3])].xAcc.pop(0)
						sensortagList[int(data[3])].yAcc.pop(0)
						sensortagList[int(data[3])].zAcc.pop(0)
						sensortagList[int(data[3])].time.pop(0)

					updateGraphs()

	conn.serPort.__del__()



root = Tk()
root.title("Synchronization GUI")

#Frame tree to devide the space
windowFrame = Frame(root)
windowFrame.pack(fill = BOTH, expand = 1, padx = 40, pady = 20)

titleFrame = Frame(windowFrame)
titleFrame.pack(fill = X, pady = 5)



mainFrame = Frame(windowFrame)
mainFrame.pack(fill = BOTH, expand = 1, pady = 5)

optButFrame = Frame(mainFrame)
optButFrame.pack(fill = Y, side = RIGHT)


dataFrame = Frame(mainFrame)
dataFrame.pack(fill = BOTH, expand = 1, side = LEFT)

graphicsFrame = Frame(dataFrame)
graphicsFrame.grid(row=0, column=0, sticky="nsew")

textFrame = Frame(dataFrame)
textFrame.grid(row=0, column=1, sticky="nsew")

dataFrame.grid_columnconfigure(0, weight=1, uniform="group1")
dataFrame.grid_columnconfigure(1, weight=1, uniform="group1")
dataFrame.grid_rowconfigure(0, weight=1)



buttonsFrame = Frame(windowFrame)
buttonsFrame.pack(fill = X, pady = 5)

#Add things to GUI some more
#Title and buttons
title = Label(titleFrame, text="Synchronization Data", font = "Segoe 16 bold").pack(side = LEFT)
exitBut = Button(buttonsFrame, text = "Exit", command = root.destroy).pack(side = RIGHT, ipadx = 20)
connectBut = Button(buttonsFrame, text = "Connect", command = connect).pack(side = LEFT, ipadx = 20)
disconnectBut = Button(buttonsFrame, text = "Disconnect", command = disconnect).pack(side = LEFT, ipadx = 20, padx = 30)
subtitle = Label(optButFrame, text="Sensortag Buttons:", font = "Segoe 10 bold").pack(side = TOP)
scanBut = Button(optButFrame, text = "Scan", command = scan).pack(ipadx = 20, pady = 30)
connectStkBut = Button(optButFrame, text = "Connect", command = startConnectStkThread).pack(ipadx = 20)
disconnectStkBut = Button(optButFrame, text = "Disonnect", command = disconnectStk).pack(ipadx = 20, pady = 10)
clearBut = Button(optButFrame, text = "Clear", command = clearTextArea).pack(side = BOTTOM, ipadx = 20)


#Text area and scrollbar
Scroll = Scrollbar(textFrame)
TextArea = Text(textFrame, height = 4) #heigth not releveant, for in pack it is said to occupy all the space, however if its not set the buttons below experience some problems
Scroll.pack(side=RIGHT, fill=Y)
TextArea.pack(side=LEFT, fill=BOTH, expand = 1)
Scroll.config(command=TextArea.yview)
TextArea.config(yscrollcommand=Scroll.set)


#Live graphics
canvas = FigureCanvasTkAgg(figure, graphicsFrame)
canvas.draw()
canvas.get_tk_widget().pack(side=TOP, fill= BOTH, expand = 1)



root.geometry("900x600+20+25")
root.mainloop()