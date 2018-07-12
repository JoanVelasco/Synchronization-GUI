import tkinter as tk

def connect():
	print("connected")

def disconnect():
	print("disconnected")


root = tk.Tk()
root.title("Synchronization GUI")
frame = tk.Frame(root).pack()

#Add things to GUI some more
w = tk.Label(root, text="Synchronization Data").pack()
exitBut = tk.Button(frame, text = "Exit", command = quit).pack(side = tk.RIGHT)
connectBut = tk.Button(frame, text = "Connect", command = connect).pack(side = tk.LEFT)
DisconnectBut = tk.Button(frame, text = "Disconnect", command = disconnect).pack(side = tk.LEFT)

root.mainloop()