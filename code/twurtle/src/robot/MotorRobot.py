# MotorRobot.py  (c) 2013 @whaleygeek

from Robot import Robot

class MotorRobot(Robot):
  def __init__(self, m):
    self.setMotorDrive(m)
    
  def setMotorDrive(self, m):
    # an association to a MotorDrive that drives two motors
    self.motorDrive = m
    
  def realMoveby(self, distance):
    self.trace("realMoveby:" + str(distance))
    self.motorDrive.moveby(distance)
    
  def realRotateby(self, degrees):
    self.trace("realRotateby:" + str(degrees))
    self.motorDrive.rotateby(degrees)

  
if __name__ == "__main__":
  #TODO r = MotorRobot(DCMotorDrive(a1=11, a2=12, b1=13, b2=14))
  r = MotorRobot()
  r.test()
  

# END

