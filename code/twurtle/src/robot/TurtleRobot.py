# TurtleRobot.py  (c) 2013 @whaleygeek

from Robot import Robot
import turtle
import time

class TurtleRobot(Robot):

  def __init__(self, canvas, width=100, height=100):
    #TODO explicitly create a screen
    #TODO explicitly create a turtle object on that screen
    #rather than using the default turtle.Turtle, so that we can have
    #independent turtles on independent screens
    self.t = turtle.RawTurtle(canvas)
    #as this is a RawTurtle, we have no screen?
    #so cant set colormode(255)

  def fast(self):
    self.t.speed("fastest")
    self.t.getscreen().delay(0)
    
  def normal(self):
    self.t.speed("normal")
    self.t.getscreen().delay(10)
    
  def realPencolor(self, color):
    self.t.pencolor(color)
    
  def realMoveby(self, distance):
    #self.trace("realMoveby:" + str(distance))
    # Try to catch the occasional distance error here
    try:
      f = float(distance)
    except ValueError:
      print "#######can't convert to float:" + str(distance)
      return
      
    self.t.forward(distance)
    
  #def realMoveto(self, x, y):
  #  print("###real moveto " + str(x) + " " + str(y))
  #  self.t.setx(x)
  #  self.t.sety(y)

  def realRotateby(self, degrees):
    self.trace("realRotateby:" + str(degrees))
    if (degrees > 0):
      self.t.left(degrees)
    else:
      self.t.right(-degrees)
      
  def realClear(self):
    # note this moves the turtle home too, but that is fine
    # as the only reason for calling this is a home command.
    self.t.reset()
    
  def realPenup(self):
    self.t.penup()
    
  def realPendown(self):
    self.t.pendown()
  
if __name__ == "__main__":
  r = TurtleRobot()
  r.test()  
  print "sleep 4"
  time.sleep(4)
  

# END

