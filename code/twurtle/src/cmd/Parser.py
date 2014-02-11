# parser.py  (c) 2013 @whaleygeek
#
# Parse a command string and dispatch to a robot for drawing

def iscommand(ch):
  return (ch >= 'A' and ch <= 'Z')
  
def isparam(ch):
  return (ch >= '0' and ch <= '9')
  
class Parser():
  CMD_HOME    = 'H'
  CMD_FORWARD = 'F' # optional param
  CMD_BACK    = 'B' # optional param
  CMD_NORTH   = 'N'
  CMD_EAST    = 'E'
  CMD_SOUTH   = 'S'
  CMD_WEST    = 'W'
  CMD_PENDOWN = 'D'
  CMD_PENUP   = 'U'
  CMD_RIGHT   = 'R' # optional param
  CMD_LEFT    = 'L' # optional param
  CMD_COUNTER = 'C' # optional param
  
  def __init__(self, robot):
    self.robot = robot
    self.result = None
    
  def parse(self, cmdstr):
    self.result = None
    state       = 0
    cmd         = None
    param       = None
    
    for ch in cmdstr:
      #print "ch:" + ch
      if (iscommand(ch)):
        if (cmd != None):
          self.run(cmd, param)
        cmd = ch
        param = None

      elif (isparam(ch)):
        if param == None:
          param = ch
        else:
          param += ch

    if (cmd != None):
      self.run(cmd, param) 

    return self.result      
 
    
  def getResult(self):
    return self.result
    
  def run(self, cmd, param):
    #if (param != None):
    #  print "run " + cmd + " " + param
    #else:
    #  print "run " + cmd
    if (param != None):
      param = int(param)
    
    if (cmd == self.CMD_HOME):
      self.home()
    elif (cmd == self.CMD_FORWARD):
      self.forward(param)
    elif (cmd == self.CMD_BACK):
      self.back(param)
    elif (cmd == self.CMD_NORTH):
      self.north()
    elif (cmd == self.CMD_EAST):
      self.east()
    elif (cmd == self.CMD_SOUTH):
      self.south()
    elif (cmd == self.CMD_WEST):
      self.west()
    elif (cmd == self.CMD_PENDOWN):
      self.pendown()
    elif (cmd == self.CMD_PENUP):
      self.penup()
    elif (cmd == self.CMD_RIGHT):
      self.right(param)
    elif (cmd == self.CMD_LEFT):
      self.left(param)
    elif (cmd == self.CMD_COUNTER):
      self.counter(param)
    
  def home(self):
    self.robot.home()

  def forward(self, distance=None):
    if (distance == None):
      distance = 10
    self.robot.forward(distance)

  def back(self, distance=None):
    if (distance == None):
      distance = 10
    self.robot.back(distance)

  def north(self):
    self.robot.north()

  def east(self):
    self.robot.east()
    
  def south(self):
    self.robot.south()
    
  def west(self):
    self.robot.west()
    
  def pendown(self):
    self.robot.pendown()
    
  def penup(self):
    self.robot.penup()
    
  def right(self, degrees=None):
    if (degrees == None):
      degrees = 90
    self.robot.right(degrees)
    
  def left(self, degrees=None):
    if (degrees == None):
      degrees = 90
    self.robot.left(degrees)
    
  def counter(self, number=None):
    if (number == None):
      number =0
    c = self.robot.counter(number)
    if (c == None):
      c = 0
    #print "counter:" + str(number) + "=" + str(c)
    if (self.result == None):
      self.result = str(c)
    else:
      self.result = self.result + "," + str(c)
    #print "result now:" + self.result
    return c
    
  
# END



