from tkinter import *
from tkinter import font
import serial
import threading
import time

OUT_STATE = 0
SCAN_STATE = 1
DATA_STATE = 2
CONNECTING_STATE = 3

handleMutex = threading.Semaphore(0)

conn = None
readThread = None
state = OUT_STATE
sensortagList = []
macList = []
emptyByte = b''

class sensorTag(object):
	def __init__(self, name, mac):
		self.name = name
		self.mac = mac
		self.handle = None

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
	#StkConn.join()
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
			conn.serPort.write(b'\x01\x8A\xFD\x04' + sensor.handle + b'\x11\x00')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x8A\xFD\x04' + sensor.handle + b'\x1E\x00')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x1F\x00\x01\x00')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x05' + sensor.handle + b'\x53\x00\x02')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x8A\xFD\x04' + sensor.handle + b'\x51\x00')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x05' + sensor.handle + b'\x51\x00\x00')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x05' + sensor.handle + b'\x53\x00\x01')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x2d\x00\x01\x00')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x35\x00\x01\x00')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x45\x00\x01\x00')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x3d\x00\x01\x00')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x4d\x00\x01\x00')
			time.sleep(0.5)
		#Enable sensors
		for sensor in sensortagList:
			#conn.serPort.write(b'\x01\x92\xFD\x05' + sensor.handle + b'\x47\x00\x01')
			#time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x3f\x00\x38\x02')
			time.sleep(0.5)
			conn.serPort.write(b'\x01\x8A\xFD\x04' + sensor.handle + b'\x3f\x00')
			time.sleep(0.5)
			#conn.serPort.write(b'\x01\x92\xFD\x05' + sensor.handle + b'\x2f\x00\x01')
			#time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x3f\x00\x3f\x02')
			time.sleep(0.5)
			#conn.serPort.write(b'\x01\x92\xFD\x05' + sensor.handle + b'\x37\x00\x01')
			#time.sleep(0.5)
			conn.serPort.write(b'\x01\x92\xFD\x06' + sensor.handle + b'\x3f\x00\x7f\x02')
			time.sleep(0.5)
		state = DATA_STATE
			


	else :
		print("Error: No Sensortags found, or already connected")


def InitLaunchpad():
	conn.serPort.write(b'\x01\x03\x0C\x00')
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(conn.serPort.in_waiting), emptyByte)
	#time.sleep(0.2)
	conn.serPort.write(b'\x01\x00\xfe\x26\x08\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00')
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(9), emptyByte)
	while conn.serPort.in_waiting <= 0: pass
	#time.sleep(0.2)
	handleData(conn.serPort.read(47), emptyByte)
	#time.sleep(0.2)
	conn.serPort.write(b'\x01\x31\xFE\x01\x15')
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(11), emptyByte)
	#time.sleep(0.2)
	conn.serPort.write(b'\x01\x31\xFE\x01\x16')
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(11), emptyByte)
	#time.sleep(0.2)
	conn.serPort.write(b'\x01\x31\xFE\x01\x1A')
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(11), emptyByte)
	#time.sleep(0.2)
	conn.serPort.write(b'\x01\x31\xFE\x01\x19')
	while conn.serPort.in_waiting <= 0: pass
	handleData(conn.serPort.read(11), emptyByte)
	#time.sleep(0.2)

#Thread functions
def handleData(header, data):
	print("handling data")
	#TextArea.insert(END, data.decode()+"\n") # "utf-8" parameter of decode
	TextArea.insert(END,(''.join(" " + format(x, '02x') for x in header) + ''.join(" " + format(x, '02x') for x in data) + "\n"))


def readPort():
	global conn
	global state
	global macList
	global sensortagList
	while conn.connected:
		while conn.serPort.in_waiting > 0:
			header = conn.serPort.read(3)
			data = conn.serPort.read(header[2])
			print(type(data))
			handleData(header, data)
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
					#Find mac and name
					#TextArea.insert(END, data.decode()+"\n")
					i = data.find(0x54)
					mac = data[i-5:i+1]
					if mac not in macList:
						macList.append(mac)
						sensor = sensorTag(name = "SensorTag"+str(len(sensortagList)), mac = mac)
						sensortagList.append(sensor)

					handleData(mac, emptyByte)

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
				pass
			else:
				#Default2?? do I need it??
				pass
	conn.serPort.__del__() #conn.serPort.close()




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
connectStkBut = Button(optButFrame, text = "Connect", command = startConnectStkThread).pack(ipadx = 20)
disconnectStkBut = Button(optButFrame, text = "Disonnect", command = disconnectStk).pack(ipadx = 20)
clearBut = Button(optButFrame, text = "Clear", command = clearTextArea).pack(side = BOTTOM, ipadx = 20)


#Text area and scrollbar
Scroll = Scrollbar(mainFrame)
TextArea = Text(mainFrame, height = 4) #heigth not releveant, for in pack it is said to occupy all the space, however if its not set the buttons below experience some problems
Scroll.pack(side=RIGHT, fill=Y)
TextArea.pack(side=LEFT, fill=BOTH, expand = 1)
Scroll.config(command=TextArea.yview)
TextArea.config(yscrollcommand=Scroll.set)


root.geometry("800x500+20+25")
root.mainloop()