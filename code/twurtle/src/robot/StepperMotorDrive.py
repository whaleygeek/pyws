# StepperMotorDrive.py  (c) 2013 @whaleygeek
#
# A placeholder for a stepper motor driver

# This is not written yet.

from MotorDrive import MotorDrive
#TODO GPIO

class StepperMotorDrive(MotorDrive): 
  #TODO init for GPIO pins, 4 pins per stepper, 2 steppers = 8 IO?
  #def __init__(self, a1, a2, a3, a4, b1, b2, b3, b4):
  
  #TODO
  #def gpio(self, pin, state):
  
  def setLeft(self, dirn):
    # self.leftdirn = dirn
    pass
    
  def setRight(self, dirn):
    # self.rightdirn = dirn
    pass
    
  def moveStep(self, num):
    # generate "num" steps on left and right
    # using the micro stepping pattern, with leftdirn and rightdirn
    pass
    
  def rotateStep(self, degrees):
    # calculate how many microsteps required per degree
    # then multiply up by degrees
    
    # generate "num" steps on left and right
    # using the micro stepping pattern, with leftdirn and rightdirn
    pass
    
  #def microstep(self, motor, steps):
  #a microstepping shift register pattern
  #there will need to be delays between each step
  
  #def step(self, motor, steps):
  #a normalstepping shift register pattern
  #there will need to be delays between each step
  
# END
