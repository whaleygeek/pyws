# This is mainly to test that the packaging has worked for robot correctly

import robot

r = robot.MotorRobot(robot.DCMotorDrive(a1=11, a2=12, b1=13, b2=14))
r.test()
