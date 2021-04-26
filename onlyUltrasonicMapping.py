import sys
import time # import time library for sleep and timer function
import brickpi3 # import the BrickPi3 drivers
import numpy # hopefully numpy is here
import grovepi
import math

from TurnDegrees import Angle
from MPU9250 import MPU9250

BP = brickpi3.BrickPi3()

timeStart = time.time()

boxTime = 2 # 3 seconds to next box?
timeRunning = 0
totalmag = 0

leftUltra = 4 # left sensor
middleUltra = 8 # middle sensor
rightUltra = 7 # right sensor

mazeMap = numpy.zeros(shape = (15,15)) # if numpy is on the pi, we'll use this instead
coordinates = [0, 0]
orientation = [0]

def turnLeft(orientation):
    Angle(91, 1, 1) 
    orientation[0] += 1
    if(orientation[0] == 5): # resets orientation to forward
       orientation[0] = 1

def turnRight(orientation): 
    Angle(91, 2, 1)
    orientation[0] -= 1
    if(orientation[0] == 0): # resets to right position
       orientation[0] = 4
    
def backUp(orientation): # need to implement instance of changing map indicator, although could be a separate function    
    while(grovepi.ultrasonicRead(leftUltra) < 30 and grovepi.ultrasonicRead(rightUltra) < 30):
        BP.set_motor_power(BP.PORT_A + BP.PORT_B, 30)
    BP.set_motor_power(BP.PORT_A + BP.PORT_B, 30)
    time.sleep(1)
       
    if(checkTurns(orientation[0], coordinates[0], coordinates[1]) == 1):
      turnLeft(orientation)
    if(checkTurns(orientation[0], coordinates[0], coordinates[1]) == 2):
      turnRight(orientation)
            
    elif(grovepi.ultrasonicRead(rightUltra) > 20):
      turnRight(orientation)
    elif(grovepi.ultrasonicRead(leftUltra) > 20):
      turnLeft(orientation)


def markMap(X, Y): # changes number based on occurrence key (IR, magnet, nothing)
    mazeMap[Y][X] = 1

def move(orientation, coordinates):
    if(orientation == 1): # oriented facing front
        coordinates[1] += 1
    elif(orientation == 2): # oriented front facing left (relative to starting position)
        coordinates[0] += 1
    elif(orientation == 3): # oriented front facing towards start
        coordinates[1] -= 1
    elif(orientation == 4): # oriented front facing right (relative to starting position)
        coordinates[0] -= 1

def checkTurns(orientation, X, Y): # return value of x, y to the left and right of robot
    print("orientation = ", orientation, " x is ", X, " y is ", Y)
    if(orientation == 1): # positioned forward relative to starting pt
        if(mazeMap[Y][X + 1] == 1): # left of the robot has been navigated?? DEPENDS ON ORIENTATION, this is on oriented forward, make a variable that tracks orientation values 1 - 4
            return 2 # turn right
        elif(mazeMap[Y][X - 1] == 1): # right of robot
            return 1 # turn left
        
        else:
            if(grovepi.ultrasonicRead(leftUltra) > 20):
                return 1
            else:
                return 2
            
       
    if(orientation == 2): # positioned turned left horizontal relative to start
        if(mazeMap[Y + 1][X] == 1 and grovepi.ultrasonicRead(rightUltra) > 30): # right has been navigated if robot is positioned to the left
            return 1 # turn left
        elif(mazeMap[Y - 1][X] == 1 and grovepi.ultrasonicRead(leftUltra) > 30): # spot between robot and x-axis
            return 2 # turn right
        else:
            if(grovepi.ultrasonicRead(leftUltra) > 20):
                return 1
            else:
                return 2
            
          
    if(orientation == 3): # positioned backward relative to starting pt
        if(mazeMap[Y][X + 1] == 1): # left of the robot has been navigated?? DEPENDS ON ORIENTATION, this is on oriented forward, make a variable that tracks orientation values 1 - 4
            return 2 # turn left
        elif(mazeMap[Y][X - 1] == 1): # right of robot
            return 1 # turn right
        else:
            if(grovepi.ultrasonicRead(leftUltra) > 20):
                return 1
            else:
                return 2
            
     
    if(orientation == 4): # positioned turned right horizontal relative to start
        if(mazeMap[Y + 1][X] == 1): # right has been navigated if robot is positioned to the left
            return 2 # turn right
        elif(mazeMap[Y - 1][X] == 1): # spot between robot and x-axis
            return 1 # turn left
        else:
            if(grovepi.ultrasonicRead(leftUltra) > 20):
                return 1
            else:
                return 2
            
  # to use this, use conditionals to determine whether to move left or right based on after using Back Up or turning

try:
    totalmag = 0
    timeStart = time.time()
    timeRunning = 0
    
    coordinates[0] = 7 # starting x point
    coordinates[1] = 0 # starting y point
    orientation[0] = 1 # starting in foward position

    lastIX = coordinates[0];
    lastIY = coordinates[1]; 

    mazeMap[coordinates[1]][coordinates[0]] = 5
    
    while True:
        if(grovepi.ultrasonicRead(middleUltra) < 20):
            if (grovepi.ultrasonicRead(leftUltra) < 25 and grovepi.ultrasonicRead(rightUltra) < 25):
                backUp(orientation)
                coordinates[0] = lastIX
                coordinates[1] = lastIY
            elif (grovepi.ultrasonicRead(leftUltra) > 20):
                turnLeft(orientation)
                lastIX = coordinates[0]
                lastIY = coordinates[1]
    
            elif (grovepi.ultrasonicRead(rightUltra) > 20):
                turnRight(orientation) 
                lastIX = coordinates[0]
                lastIY = coordinates[1]
            
            timeStart = time.time()
            
        elif(grovepi.ultrasonicRead(leftUltra) < 6):
            print("short correct left")
            if(grovepi.ultrasonicRead(leftUltra) < 3):
                Angle(8, 1, -1)
            else:
                Angle(12, 2, 1)
                
        elif(grovepi.ultrasonicRead(rightUltra) < 6):
            print("short correct right")
            if(grovepi.ultrasonicRead(rightUltra) < 3):
                Angle(8, 2, -1)
            else:
                Angle(12, 1, 1)
            
        else:
            print("go go")
            BP.set_motor_power(BP.PORT_A + BP.PORT_B, -30)

        if(timeStart + boxTime <= time.time()):
            move(orientation[0], coordinates)
            markMap(coordinates[0], coordinates[1])
            
            print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")
            timeStart = time.time()
        
        time.sleep(0.0000001) # hold each loop/iteration for .001 seconds
        
except IOError as error:
    print(error)
    BP.reset_all()
except TypeError as error:
    print(error)
    BP.reset_all()
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.set_motor_dps(BP.PORT_C, -10) # drop off mechanism
    time.sleep(1)
    print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")
    BP.reset_all()
