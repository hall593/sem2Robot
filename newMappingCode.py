from MPU9250 import MPU9250
import sys
import time # import time library for sleep and timer function
import brickpi3 # import the BrickPi3 drivers
import numpy # hopefully numpy is here

BP = brickpi3.BrickPi3()

timeStart = time.time()
dT = 3 # 3 seconds to next box?
timeRunning = 0


#mazeMap = numpy.zeros(shape = (7,7))

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

def moveLeft():
    X += 1
    
def moveRight():
    X -= 1
    
def moveForward():
    Y += 1
    
def move Backwards():
    Y -= 1
    
def checkTurns(orientation): # return value of x, y to the left and right of robot
    if(orientation == 1): # positioned forward relative to starting pt
        if(mazeMap[Y][X + 1] == 1): # left of the robot has been navigated?? DEPENDS ON ORIENTATION, this is on oriented forward, make a variable that tracks orientation values 1 - 4
            return 1 # not sure about this yet
        else if(mazeMap[Y][X - 1] == 1): # right of robot
            return 2
    if(orientation == 2): # positioned turned horizontal relative to start
        if(mazeMap[Y + 1][X] == 1): # right has been navigated if robot is positioned to the left
            return 1
        else if(mazeMap[Y - 1][X] == 1): # spot between robot and x-axis
            return 2
        
try:
    while True:
        while(time.time() - timeStart < 3):
          
        
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")
    BP.reset_all()
