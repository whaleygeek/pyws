# MotorDrive.py  (c) 2013 @whaleygeek
#
# An abstract base class for a motor driver.
# A motor driver has a pair of motors that work together.
# They allow movement and rotation.

#TODO need some motor specific counters
#index from 10 + n
#0 now leftdir
#1 now rightdir
#2 this left fwd time
#3 this left rev time
#4 this right fwd time
#5 this right rev time
#6 tot left fwd time
#7 tot left rev time
#8 tot right fwd time
#9 tot right rev time


class MotorDrive():
  FORWARD = 1
  OFF     = 0
  REVERSE = -1
  
  def moveby(self, distance):
    left, right = self.motorMoveConfig(distance)
    self.setLeft(left)
    self.setRight(right)
    self.moveStep(distance)
    self.setLeft(self.OFF)
    self.setRight(self.OFF)
    
  def rotateby(self, degrees):
    left, right = self.motorRotateConfig(degrees)
    self.setLeft(left)
    self.setRight(right)
    self.rotateStep(degrees)
    self.setLeft(self.OFF)
    self.setRight(self.OFF)
    
  def motorMoveConfig(self, distance):
    # return directions for left and right motors
    if (distance > 0):
      return self.FORWARD, self.FORWARD # forward
    elif (distance == 0):
      return self.OFF, self.OFF # no movement
    else:
      return self.REVERSE, self.REVERSE # backwards
      
  def motorRotateConfig(self, degrees):
    # return directions for left and right motors
    if (degrees > 0):
      return self.FORWARD, self.REVERSE # turn right
    elif (degrees == 0):
      return self.OFF, self.OFF # no turn
    else:
      return self.REVERSE, self.FORWARD # turn left    
    
    
  def setLeft(self, dirn):
    # override this in subclass
    # it must configure the left motor to dirn
    # it wont start the motor until steps() is called
    pass
    
  def setRight(self, dirn):
    # override this in subclass
    # it must configure the right motor to dirn
    # it won't start the motor until steps() is called
    pass
    
  def moveStep(self, num):
    # override this in subclass
    # for stepper motors, 1 step is really one step in the L/R configuration
    # for DC motors, it translates to an amount of time with the L/R configuration
    pass
    
  def rotateStep(self, degrees):
    # override this in subclass
    # for stepper motors, 1 degree is probably a fixed number of steps
    # for DC motors, it translates to an amount of time with the L/R configuration
    pass
    
    
# END
