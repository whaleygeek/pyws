# VectorMath.py (c) 2013 @whaleygeek
#
# Simple mathematical transforms for vectors
# useful for working with both polar and cartesian coordinate systems
#
# see: http://www.mathsisfun.com/algebra/trig-four-quadrants.html

import math

def trace(msg):
  pass # print(msg)

def xymove(oldx, oldy, angle, distance):
  # solve the right angled triangle to move from x,y
  # move by vector theta="angle", hypotenuse="distance"
  # 0 is east, degrees increase counter clockwise
  # +y is up, -y is down
  # +x is right, -x is left
  
  # if the relationship is non triangluar, we do it rectangular
  # this stops horrible rounding errors that add up gradually
  
  if (angle == 0):
    return oldx+distance, oldy
  if (angle == 90):
    return oldx, oldy+distance
  if (angle == 180):
    return oldx-distance, oldy
  if (angle == 270):
    return oldx, oldy-distance
  
  #TODO review this for all quadrants
  #TODO review this for sign change in y that we just made
  theta = math.radians(angle)
  newx = oldx + (distance * math.cos(theta))
  newy = oldy + (distance * math.sin(theta))
  return newx, newy
  
 
def bestrotate(oldDegrees, newDegrees): 
  trace("quickest from" + str(oldDegrees) + " to " + str(newDegrees))
  # work out quickest way to rotate from old to new
  # be careful of quadrant changes esp wraps from 270 to 360(0)
  # to make sure we go the right way. 
  # +ve is anticlockwise
  # -ve is clockwise
  
  trace("old:" + str(oldDegrees) + " new:" + str(newDegrees))
  d = (newDegrees - oldDegrees) 
  if (d < -180):
    d = 360 + d
  elif (d > 180):
    d = 360 - d
  trace("quickest:" + str(d))
  return d  
  
  
def quadrant(x1, y1, x2, y2):
  # work out which quadrant a line (x1,y1) to (x2,y2) is in
  # where x1,y1 is present position
  # x2, y2 is new position
  # +x is right, -x is left
  # +y is up, -y is down
  # Q1 is top right
  # Q2 is top left
  # Q3 is bottom left
  # Q4 is bottom right
  # None means it is not in a quadrant, but on the edge,
  # e.g. x1=y1 or x2=y2 and thus theta will be invalid
  # as the relationship is square, not triangular
  
  xd = x2-x1
  yd = y2-y1
  
  if (xd == 0 or yd == 0):
    return None # relationship is square, not triangular
    
  if (yd > 0):
    if (xd > 0):
      return 1 # top right quadrant (0<= d < 90)
    else:
      return 2 # top left quadrant (90 <= d < 180)
  else: # yd < 0
    if (xd < 0):
      return 3 # bottom left quadrant (180 <= d < 270)
    else:
      return 4 # bottom right quadrant (270 <= d < 360)
  
      
def bestmove(facing, oldx, oldy, newx, newy):
  trace("bestmove:" + str(facing) + " " + str(oldx) + " " + str(oldy) + " " + str(newx) + " " + str(newy))
  degrees, distance = bestmove2(facing, oldx, oldy, newx, newy)
  
  degrees, distance = optimisemove(facing, 0, degrees, distance)
  
  trace("degrees:" + str(degrees) + " distance:" + str(distance))
  return degrees, distance
  
def oppositedegrees(degrees):
  return (degrees + 180) % 360
  
def optimisemove(oldfacing, newfacing, degrees, distance):
  # work out if (degrees,distance) is the best move,
  # or whether it is better to walk backwards
  # i.e. minimise the total time spent rotating
  # this is useful if rotation is inaccurate and should be minimised
  #
  # There is a mathematically simpler way to do this,
  # but we do it this way so we can later weight right rotates and left rotate
  # and backwards movement differently, 
  # as the accuracy of each might be non symmetrical
  
  targetdegrees = (oldfacing + degrees) % 360
  
  # work out cost of forward movement
  firstrotfwd = degrees
  lastrotfwd  = bestrotate(targetdegrees, newfacing)
  totalrotfwd = abs(firstrotfwd) + abs(lastrotfwd)

  # work out cost of reverse movement
  firstrotrev = oppositedegrees(firstrotfwd)
  lastrotrev  = oppositedegrees(lastrotfwd)
  totalrotrev = abs(firstrotrev) + abs(lastrotrev)
  
  # choose the minimal cost
  if (totalrotrev < totalrotfwd):
    return firstrotrev, -distance
  else:
    return degrees, distance
    
  
def bestmove2(facing, oldx, oldy, newx, newy):
  # work out whether a square move (along an axis)
  # or a triangular move (within a quadrant)
  # is the best move, 
  # and turn into a degrees, distance for that move
  
  q = quadrant(oldx, oldy, newx, newy)
  if (q == None): # Not a triangular relationship
    degrees, distance = squaremove(facing, oldx, oldy, newx, newy)
  else:
    degrees, distance = triangularmove(facing, oldx, oldy, newx, newy)
    
  #TODO perform backwards optimisation, if rotation is less, we can
  #rotate a little bit and then walk backwards to the newpos
  return degrees, distance
    
    
def squaremove(facing, oldx, oldy, newx, newy):
  # optimise move based on a rectangular relationship  
  dx = newx - oldx
  dy = newy - oldy
  
  if (dy == 0): # y matches
    if (dx == 0): 
      # already there
      return 0, 0 # do nothing
      
    elif (newx < oldx): 
      # move left along x axis
      degrees = bestrotate(facing, 180)
      distance = abs(dx)
      trace("optimised abs left")
      return degrees, distance
      
    else: # newx > oldx
      # move right along x axis
      degrees = bestrotate(facing, 0)
      distance = abs(dx)
      trace("optimised abs right")
      return degrees, distance

  if (dx == 0): # x matches
    if (newy > oldy):
      # move up along y axis
      degrees = bestrotate(facing, 90)
      distance = abs(dy)
      trace("optimised abs down")
      return degrees, distance
      
    else: # newy < oldy
      # move down along y axis
      degrees = bestrotate(facing, 270)
      distance = abs(dy)
      trace("optimised abs up")
      return degrees, distance
    
    
def triangularmove(facing, oldx, oldy, newx, newy):
  # use trigonometry to work out the best rotate and move
  
  A = newx - oldx
  O = newy - oldy 
  trace("A=" + str(A))
  trace("O=" + str(O))
  
  # theta is the angle in radians from 0 degrees (east) ccw to hypotenuse
  # this is not strictly theta, as theta is from the adjacent to the hypotenuse
  # T=O/A
  #use atan2(O,A) so quadrant is known, as signs of both parts are known
  theta = math.atan2(O,A)
  theta_degrees = math.degrees(theta)
  trace("trig: need to face:" + str(theta_degrees))
    
  # hypotenuse is the distance to travel along H
  # S=O/H => H=O/S
  H = O / math.sin(theta)
    
  # given our present facing direction, and theta (from 0 to H)
  # work out the rotation needed to face the newx, newy
  # best rotate to 0 from facing is always -facing
  rotate_degrees = -facing + math.degrees(theta)
  distance       = abs(H)

  trace("trigonometry used")
  return rotate_degrees, distance
  
  
def xybetween(x1, x2, y1, y2):
  # use pythagora's theorem to work out distane beween two points
  A = x2 - x1
  O = y2 - y1
  H = math.sqrt((A*A) + (O*O))
  # result will always be positive as the squares are positive
  return H 


# END

