# GPIO.py  (c) 2013 @whaleygeek
#
# A Raspberry Pi GPIO simulator/scaffolding for use on the PC

IN  = False
OUT = True

BCM = 1
BOARD = 2

sim = False

def setmode(mode):
  pass
  
def cleanup():
  pass
  
def setup(pin, dirn):
  pass
  
def output(pin, value):
  # just display the value on any write
  print "out:" + str(pin) + "=" + str(value)
  
def input(pin):
  global sim
  # return a simulated toggling value on any read.
  # ignores the pin for the moment as we only have 1 pin
  result = sim
  sim = not sim
  return result
  
# END
