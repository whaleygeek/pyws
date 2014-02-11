# App.py (c) 2013 @whaleygeek
#
# The main interactive application.
# waits for a command at a command prompt.
# Accepts drawing commands or simple management commands.


import Tkinter
import thread
import random
import time
import sys
import robot
#import twitter
import cmd
from RFC822 import RFC822Reader
from RFC822 import RFC822Writer
from Proxy import GenericDynamicProxy


# CONFIGURATION

USER_WIDTH = 200
USER_HEIGHT = 200

ALL_WIDTH = 400
ALL_HEIGHT = 400


# based on code from:
# http://stackoverflow.com/questions/14514524/how-to-combine-tkinter-windows
# http://effbot.org/tkinterbook/grid.htm

win = Tkinter.Tk()
win.withdraw()

# this draws two frames in a single window

userframe = Tkinter.Frame(bg='black')
Tkinter.Label(userframe, text=u'Your Turtle', bg='grey', fg='white').pack(fill='x')
usercanvas = Tkinter.Canvas(userframe, width=USER_WIDTH, height=USER_HEIGHT)
usercanvas.pack()
#userframe.pack(fill='both', expand=True)
userframe.grid(row=0, column=0, sticky=Tkinter.N)

allframe = Tkinter.Frame(bg='black')
Tkinter.Label(allframe, text=u'Grandpa Turtle', bg='grey', fg='white').pack(fill='x')
allcanvas= Tkinter.Canvas(allframe, width=ALL_WIDTH, height=ALL_HEIGHT)
allcanvas.pack()
#allframe.pack(fill='both', expand=True)
allframe.grid(row=0, column=1)

win.deiconify()

userbot = robot.TurtleRobot(usercanvas)
allbot  = robot.TurtleRobot(allcanvas)
bothbot = GenericDynamicProxy([userbot, allbot])
bothcmd = cmd.Parser(bothbot)


#disabled - fails on raspberry pi if not in main thread
#print "starting thread"    
#thread.start_new_thread(tkloop, ())    
#print "thread started"

def tkloop():
  global win
  w = win
  while True:
    # same as w.mainloop()
    # but this gives us a chance to monitor it later if needed
    #print "update"
    try:
      w.update()
    except:
      print "exception in update - ignored"
      time.sleep(1)
    #time.sleep(0.25)

def storeDone(item):
  # store a done item to the done.txt file at the end
  dw = RFC822Writer("done.txt")
  dw.start()
  dw.write(item)
  dw.finished()
  
def recoverDone():
  # recover all commands from done and interpret quickly
  # later we will add a number, but not enough time now
  # if you want less, just hand edit the file
  
  userbot.fast()
  allbot.fast()
  
  dr = RFC822Reader("done.txt")
  dr.start()
  while True:
    item = dr.read()
    if (item == None):
      break
    screen_name = item["screen_name"]
    command     = item["command"]
    print screen_name
    interpret(command)
      
  dr.finished()
  userbot.normal()
  allbot.normal()
  
  
def tweet(number):
  # Read a numbered tweet from commands.txt
  # returns None if not found

  number = int(number)
  print "tweet:" + str(number)
  
  tr = RFC822Reader("commands.txt")
  if (not tr.exists()):
    print "no file"
    return None
    
  tr.start()
  if (number != 1):
    result = tr.skip(number-1)
    if (result == None):
      print "no tweets"
      tr.finished()
      return None
      
  print "reading"
  item = tr.read()  
    
  tr.finished()
  return item
  
  
def interpret(cmdstr):
  global bothcmd, userbot, allbot
  global ALL_WIDTH, ALL_HEIGHT, USER_WIDTH, USER_HEIGHT
  
  userbot.home()
  userbot.clear()  

  c = random.choice(robot.Robot.colors)
  
  facing = random.randint(0, 360)
  distance = random.randint(0, (ALL_WIDTH-USER_WIDTH)/2)
  
  allbot.home()  
  allbot.pencolor(c)
  allbot.rotateto(facing)
  allbot.forward(distance)
  
  result = bothcmd.parse(cmdstr)
  if (result != None):
    print result
  
  
  
# MAIN TOP LOOP ----------------------------------------------------------------
   
while True:
  cmdstr = raw_input("command? ")
  cmdstr = cmdstr.strip().upper()
  if (len(cmdstr) != 0):
    parts = cmdstr.split(" ", 1)
    try:
      params = parts[1]
      cmdstr = parts[0]
    except IndexError:
      params = None
  
    if (cmdstr == "QUIT"):
      break
    
    elif (cmdstr == "RECOVER"):
      recoverDone()
    
    elif (cmdstr == "TWEET"):
      item = tweet(params)
      if (item == None):
        print "no such tweet"
      else:
        cmdstr = item["command"]
        interpret(cmdstr)
        storeDone(item)
    
    else: # a command string entered from the console
      interpret(cmdstr)
      item = {"screen_name":"console", "name":"console", "command":cmdstr}
      storeDone(item)
    

