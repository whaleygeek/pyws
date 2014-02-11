# This is mainly to test that the packaging has worked for robot correctly

import robot
import cmd
import time
import sys

def interactive():
  while True:
    cmdstr = raw_input("command string? ")
    if (cmdstr == "Q"):
      break
    p.parse(cmdstr)
    
    
    
r = robot.TurtleRobot()
p = cmd.Parser(r)

if (len(sys.argv) >= 2):
  p.parse(sys.argv[1])
  time.sleep(2)
else:
  interactive()

