import time
import mcpi.minecraft as minecraft

try:
  from Tkinter import * # python2
except ImportError:
  from tkinter import * # python3

mc = minecraft.Minecraft.create("192.168.0.4")

win = Tk()

def doHello():
  mc.postToChat("HELLO")
  
b=Button(text="HELLO", command=doHello)
b.pack()

win.mainloop()
  
