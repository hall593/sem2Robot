from MPU9250 import MPU9250
import sys
import time # import time library for sleep and timer function
import brickpi3 # import the BrickPi3 drivers
import numpy # hopefully numpy is here

BP = brickpi3.BrickPi3()

timeStart = time.time()
boxTime = 3 # 3 seconds to next box?
timeRunning = 0


#mazeMap = numpy.zeros(shape = (7,7)) # if numpy is on the pi, we'll use this insteas

mazeMap = [[ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0]]
X = 3 # starting x point
Y = 0 # starting y point

mazeMap[Y][X] = 5

def markMap(occurrence): # changes number based on occurrence key (IR, magnet, nothing)
    if(occurrence == 4): # case of IR detection
        mazeMap[Y][X] = 4
    else if (occurrence == 3): # case of strong magnetic reading
        mazeMap[Y][X] = 3
    else: # normal readings
        mazeMap[Y][X] = 1
    timeStart = time.time()

def move(orientation):
    if(oriententation == 1): # oriented facing front
        Y += 1
    else if(orientation == 2): # oriented front facing left (relative to starting position)
        X += 1
    else if(orientation == 3): # oriented front facing right (relative to starting position)
        X -= 1
    else if(orientation == 4): # oriented front facing towards start
        Y -= 1

def checkTurns(orientation): # return value of x, y to the left and right of robot
    if(orientation == 1 or orientation == 4): # positioned forward relative to starting pt
        if(mazeMap[Y][X + 1] == 1): # left of the robot has been navigated?? DEPENDS ON ORIENTATION, this is on oriented forward, make a variable that tracks orientation values 1 - 4
            return 1 # not sure about this yet, but returning number can be used to determine whether the robot turns left or right, maybe left is obstructed, have it turn right if 1 is returned
        else if(mazeMap[Y][X - 1] == 1): # right of robot
            return 2
        else: # pretty sure we won't need this
            return 0
        
    if(orientation == 2 or orientation == 3): # positioned turned horizontal relative to start
        if(mazeMap[Y + 1][X] == 1): # right has been navigated if robot is positioned to the left
            return 1
        else if(mazeMap[Y - 1][X] == 1): # spot between robot and x-axis
            return 2
        else:
            return 0
        
  # to use this, use conditionals to determine whether to move left or right based on after using Back Up or turning
          
        
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")
    BP.reset_all()
