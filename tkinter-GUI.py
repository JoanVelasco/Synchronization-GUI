from tkinter import *
from tkinter import font

def connect():
	print("connected")

def disconnect():
	print("disconnected")


root = Tk()
root.title("Synchronization GUI")

windowFrame = Frame(root)
windowFrame.pack(fill = BOTH, expand = 1, padx = 40, pady = 20)

titleFrame = Frame(windowFrame, bg = "green")
titleFrame.pack(fill = X, pady = 5)

mainFrame = Frame(windowFrame, bg = "red")
mainFrame.pack(fill = BOTH, expand = 1, pady = 5)

buttonsFrame = Frame(windowFrame, bg = "green")
buttonsFrame.pack(fill = X, pady = 5)

#Add things to GUI some more
w = Label(titleFrame, text="Synchronization Data", font = "Segoe 16 bold").pack(side = LEFT)
exitBut = Button(buttonsFrame, text = "Exit", command = root.destroy).pack(side = RIGHT, ipadx = 20)
connectBut = Button(buttonsFrame, text = "Connect", command = connect).pack(side = LEFT, ipadx = 20)
DisconnectBut = Button(buttonsFrame, text = "Disconnect", command = disconnect).pack(side = LEFT, ipadx = 20, padx = 30)



root.geometry("800x500+20+25")
root.mainloop()