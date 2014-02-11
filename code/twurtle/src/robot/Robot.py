# Robot.py  (c) 2013 @whaleygeek
#
# Implemenents the mathematical model for a Robot.
# Provides a binding to the python turtle (via subclassing)
# Provides a binding to real raspberry pi robot motors (via subclassing)

import turtle
import time
import VectorMath

def realColor(c):
  r, g, b = c
  r = float(r/255)
  g = float(g/255)
  b = float(b/255)
  return (r, g, b)

class Robot():
  DEFAULT_ROTATE     = 30
  DEFAULT_DISTANCE   = 1
  HOME_X             = 0
  HOME_Y             = 0
  EAST               = 0
  NORTH              = 90
  WEST               = 180 
  SOUTH              = 270
  HOME_FACING        = EAST
  

    
  BLACK              = realColor((0, 0, 0))
  BROWN              = realColor((165, 42, 42))
  RED                = realColor((255, 0, 0))
  ORANGE             = realColor((255, 128, 64))
  YELLOW             = realColor((255, 255, 0))
  GREEN              = realColor((0, 255, 0))
  BLUE               = realColor((0, 0, 255))
  VIOLET             = realColor((128, 0, 128))
  GREY               = realColor((128, 128, 128))
  WHITE              = realColor((255, 255, 255))
  # intentionally miss white as it is bg color
  colors = (BLACK, BROWN, RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET, GREY)
  
  posx               = HOME_X
  posy               = HOME_Y
  facing             = HOME_FACING
  penstate           = True
  pencol             = BLACK
  awake              = False
  drawing            = False
  counters           = [0,0,0,0,0,0,0,0,0,0]
  COUNT_NOW_POSX     = 0
  COUNT_NOW_POSY     = 1
  COUNT_NOW_FACING   = 2
  COUNT_THIS_DIST    = 3
  COUNT_THIS_RROT    = 4
  COUNT_THIS_LROT    = 5
  COUNT_TOT_DRAWINGS = 6
  COUNT_TOT_DIST     = 7
  COUNT_TOT_RROT     = 8
  COUNT_TOT_LROT     = 9
  names = ["posx","posy","facing","dist","rrot","lrot","Tdrg","Tdist","Trrot","Tlrot"]
    
  def __init__(self):
    pass
    
  def realMoveby(self, distance):
    # subclasses override this if they want a vector movement
    pass
    
  def realMoveto(self, x, y):
    # subclasses override this if they want a cartesian movement
    pass
    
  def realRotateby(self, degrees):
    # subclasses override this to change the present rotation
    pass    
    
  def realClear(self):
    # subclasses override to clear any output device
    pass
    
  def realPenup(self):
    # subclasses override to lift a physical pen
    pass
    
  def realPendown(self):
    # subclasses override to drop a physical pen
    pass
    
  def realPencolor(self, color):
    # subclasses override to change pen
    pass
    
  def fast(self):
    # set to fastest drawing speed
    pass
    
  def normal(self):
    # set to normal drawing speed
    pass

  def counterName(self, number):
    return self.names[number]
     
  def pencolor(self, color):
    self.pencol = color
    self.realPencolor(color)
    
  def moveto(self, x, y):
    #print("moveto:" + str(x) + "," + str(y))
    
    self.realMoveto(x, y)
    self.counters[self.COUNT_NOW_POSX] = self.posx
    self.counters[self.COUNT_NOW_POSY] = self.posy
    self.posx = x
    self.posy = y
    
  def rotateto(self, facing):
    degrees = (self.facing - facing) % 360
    self.rotateby(degrees)
    
  def moveby(self, distance):
    self.trace("moveby:" + str(distance))
    
    self.realMoveby(distance)
    newx, newy = VectorMath.xymove(self.posx, self.posy, self.facing, distance) 
    self.moveto(newx, newy)
    self.inc(self.COUNT_THIS_DIST, abs(distance))
    
  def rotateby(self, degrees):
    self.trace("rotateby:" + str(degrees))
    
    self.realRotateby(degrees)

    if (degrees < 0):
      self.inc(self.COUNT_THIS_LROT, -degrees)
    else:
      self.inc(self.COUNT_THIS_RROT, degrees)
    self.facing = (self.facing + degrees) % 360 # +ve=ccw, -ve=cw
    self.counters[self.COUNT_NOW_FACING] = self.facing
    
  def trace(self, msg):
    pass #print msg
    
  def wakeup(self):
    self.trace("wakeup")
    awake = True
    
  def sleep(self):
    self.trace("sleep")
    awake = False
    
  def start(self):
    self.trace("start")
    self.clearThisCounters()
    drawing = True
    
  def finish(self):
    self.trace("finish")
    drawing = False
    self.rollUpTotalCounters()
    self.inc(self.COUNT_TOT_DRAWINGS)
    
  def clear(self):
    # intended to reset the whole screen for turtle robots
    self.realClear()
    #self.home()
    
  def home(self):
    self.trace("home")
    self.penup()
    # Move to the home location
    degrees, distance = VectorMath.bestmove(self.facing, self.posx, self.posy, self.HOME_X, self.HOME_Y)
    # this should make us face the home (unless backwards optimiser enabled)
    self.rotateby(degrees)
    self.moveby(distance)
    # Rotate to the default facing direction when at home
    degrees = VectorMath.bestrotate(self.facing, self.HOME_FACING)
    self.rotateby(degrees)
    self.pendown()
    # Force back to home to prevent compound rounding errors
    self.posx = self.HOME_X
    self.posy = self.HOME_Y
    
  def forward(self, distance=DEFAULT_DISTANCE):
    self.trace("forward:" + str(distance))
    self.moveby(distance)
    
  def back(self, distance=DEFAULT_DISTANCE):
    self.trace("back:" + str(distance))
    self.moveby(-distance)
    
  def north(self):
    self.trace("north")
    rot = VectorMath.bestrotate(self.facing, self.NORTH)
    self.rotateby(rot)
    
  def east(self):
    self.trace("east")
    rot = VectorMath.bestrotate(self.facing, self.EAST)
    self.rotateby(rot)
    
  def south(self):
    self.trace("south")
    rot = VectorMath.bestrotate(self.facing, self.SOUTH)
    self.rotateby(rot)
    
  def west(self):
    self.trace("west")
    rot = VectorMath.bestrotate(self.facing, self.WEST)
    self.rotateby(rot)
    
  def right(self, degrees=DEFAULT_ROTATE):
    self.trace("right:" + str(degrees))
    self.rotateby(-degrees)
    
  def left(self, degrees=DEFAULT_ROTATE):
    self.trace("left:" + str(degrees))
    self.rotateby(degrees)
    
  def pendown(self):
    self.trace("pendown")
    self.realPendown()
    self.penstate = True
    
  def penup(self):
    self.trace("penup")
    self.realPenup()
    self.penstate = False    
    
  def inc(self, counter, amount=1):
    self.counters[counter] = self.counters[counter] + amount
    
  def clearThisCounters(self):
    self.counters[self.COUNT_THIS_DIST] = 0
    self.counters[self.COUNT_THIS_RROT] = 0
    self.counters[self.COUNT_THIS_LROT] = 0    
    
  def rollUpTotalCounters(self):
    self.inc(self.COUNT_TOT_DIST, self.counters[self.COUNT_THIS_DIST])
    self.inc(self.COUNT_TOT_LROT, self.counters[self.COUNT_THIS_LROT])
    self.inc(self.COUNT_TOT_RROT, self.counters[self.COUNT_THIS_RROT])
       
  def counter(self, number=0):
    #self.trace("counter:" + str(number))
    return self.counters[number]
    
  def test(self):
    self.wakeup()
    self.start()

    for i in range(4):
      self.forward(100)
      self.right(90)

    self.finish()
    for c in range(0,10):
      print self.counterName(c) + "=" + str(self.counter(c))
    self.sleep()
    
  
if __name__ == "__main__":
  r = Robot()
  r.test()

# END

