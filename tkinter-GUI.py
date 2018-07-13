from tkinter import *
from tkinter import font

def connect():
	print("connected")
	TextArea.insert(END, "Connected\n")

def disconnect():
	print("disconnected")
	TextArea.insert(END, "Disconnected\n")

def clearTextArea():
	print("Text are cleared")
	TextArea.delete('1.0', END)




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
clearBut = Button(optButFrame, text = "Clear", command = clearTextArea).pack(side = RIGHT, ipadx = 20)


#Text area and scrollbar
Scroll = Scrollbar(mainFrame)
TextArea = Text(mainFrame, height = 4) #heigth not releveant, for in pack it is said to occupy all the space, however if its not set the buttons below experience some problems
Scroll.pack(side=RIGHT, fill=Y)
TextArea.pack(side=LEFT, fill=BOTH)
Scroll.config(command=TextArea.yview)
TextArea.config(yscrollcommand=Scroll.set)


root.geometry("800x500+20+25")
root.mainloop()