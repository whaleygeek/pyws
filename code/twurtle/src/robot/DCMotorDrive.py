# DCMotorDrive.py  (c) 2013 @whaleygeek
#
# A concrete class that implements a motor drive using two DC motors
# distance and rotation is entirely done by timing

from MotorDrive import MotorDrive
import RPi.GPIO as GPIO
import time

class DCMotorDrive(MotorDrive):  
  # 10 steps per second
  MOVE_STEP_TIME   = 0.1
  # 10 degrees per second
  ROTATE_STEP_TIME = 0.1
  
  def __init__(self, a1, a2, b1, b2):
    self.motora = [a1, a2]
    self.motorb = [b1, b2]
  
  def gpio(self, pin, state):
    GPIO.output(pin, state)
    
  def drive(self, motor, dirn):
    if (dirn == self.OFF):
      self.gpio(motor[0], False)
      self.gpio(motor[1], False)
      
    elif (dirn == self.FORWARD):
      self.gpio(motor[0], True)
      self.gpio(motor[1], False)

    elif (dirn == self.REVERSE):
      self.gpio(motor[0], False)
      self.gpio(motor[1], True)

  def wait(self, secs):
    print "wait secs:" + str(secs)
    #time.sleep(secs)

        
  def setLeft(self, dirn):
    self.drive(self.motora, dirn)
    
  def setRight(self, dirn):
    self.drive(self.motorb, dirn)

  def moveStep(self, num):
    t = num * self.MOVE_STEP_TIME
    self.wait(t)
    
  def rotateStep(self, degrees):
    t = degrees * self.ROTATE_STEP_TIME
    self.wait(t)
    
    
# END
