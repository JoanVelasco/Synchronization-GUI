from tkinter import *

def connect():
	print("connected")

def disconnect():
	print("disconnected")


root = Tk()
root.title("Synchronization GUI")
frame = Frame(root, bg = "red")
frame.pack( fill = BOTH, expand = 1)
frame2 = Frame(root, bg = "green")
frame2.pack( fill = BOTH, expand = 1)

#Add things to GUI some more
w = Label(frame, text="Synchronization Data")
w.pack(side = TOP)

exitBut = Button(frame2, text = "Exit", command = root.destroy)
exitBut.pack(side = RIGHT)

connectBut = Button(frame2, text = "Connect", command = connect)
connectBut.pack(side = LEFT)

DisconnectBut = Button(frame2, text = "Disconnect", command = disconnect)
DisconnectBut.pack(side = LEFT)



root.geometry("800x500+20+25")
root.mainloop()