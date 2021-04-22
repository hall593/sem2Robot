from MPU9250 import MPU9250
import sys
import time # import time library for sleep and timer function
import brickpi3 # import the BrickPi3 drivers
import numpy # hopefully numpy is here
import grovepi
import math

from TurnDegrees import Angle
from MPU9250 import MPU9250

BP = brickpi3.BrickPi3()
imu = MPU9250()

timeStart = time.time()
boxTime = 3 # 3 seconds to next box?
timeRunning = 0

orientation = 1 # starting at forward position

leftUltra = 4 # left sensor
middleUltra = 8 # middle sensor
rightUltra = 7 # right sensor

sensor1 = 14 # left IR sensor
sensor2 = 15 # right IR sensor

totalmag = 0

#mazeMap = numpy.zeros(shape = (7,7)) # if numpy is on the pi, we'll use this insteas

mazeMap = [[ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0]]
X = 3 # starting x point
Y = 0 # starting y point

lastIX = 0;
lastIY = 0; 

mazeMap[Y][X] = 5

def turnLeft(orientation):
    Angle(91, 1, 1) 
    orientation += 1
    if(orientation == 5): # resets orientation to forward
       orientation = 1 
    
    lastIX = X
    lastIY = Y
    
    timeStart = time.time()

def turnRight(orientation): 
    Angle(91, 2, 1)
    orientation -= 1
    if(orientation == 0): # resets to right position
       orientation = 4
    
    lastIX = X
    lastIY = Y
    
    timeStart = time.time()
    
def checkMagnet():
    mag = imu.readMagnet()
    total_mag=math.sqrt(mag['x']*mag['x']+mag['y']*mag['y']+mag['z']*mag['z'])
    
def backUp(instance, orientation): # need to implement instance of changing map indicator, although could be a separate function
    X = lastIX
    Y = lastIY
    
    if(instance == 1):
        while(grovepi.ultrasonicRead(leftUltra) < 30 and grovepi.ultrasonicRead(rightUltra) < 30):
            BP.set_motor_power(BP.PORT_A + BP.PORT_D, 30)
        BP.set_motor_power(BP.PORT_A + BP.PORT_D, 30)
        time.sleep(1)
        
   if(instance == 2): # in the instance that a magnet is sensed
        while((grovepi.analogRead(sensor1) > 40 or grovepi.analogRead(sensor2) > 40) or (grovepi.ultrasonicRead(leftUltra) < 30 and grovepi.ultrasonicRead(rightUltra) < 30)):
            BP.set_motor_power(BP.PORT_A + BP.PORT_D, 30)
   if(instance == 3):
        while(totalmag > 100 or (grovepi.ultrasonicRead(leftUltra) < 30 and grovepi.ultrasonicRead(rightUltra) < 30)):
            BP.set_motor_power(BP.PORT_A + BP.PORT_D, 30)
            checkMagnet()    
            
   if(checkTurns(orientation) == 1):
      turnLeft(orientation)
   if(checkTurns(orientation) == 2):
      turnRight(orientation)
            
   elif(grovepi.ultrasonicRead(rightUltra) > 20):
      turnRight(orientation)
   elif(grovepi.ultrasonicRead(leftUltra) > 20):
      turnLeft(orientation)

def markMap(occurrence): # changes number based on occurrence key (IR, magnet, nothing)
    if(occurrence == 4): # case of IR detection
        mazeMap[Y][X] = 4
    elif (occurrence == 3): # case of strong magnetic reading
        mazeMap[Y][X] = 3
    else: # normal readings
        mazeMap[Y][X] = 1
    timeStart = time.time()

def move(orientation):
    if(oriententation == 1): # oriented facing front
        Y += 1
    elif(orientation == 2): # oriented front facing left (relative to starting position)
        X += 1
    elif(orientation == 3): # oriented front facing towards start
        Y -= 1
    elif(orientation == 4): # oriented front facing right (relative to starting position)
        X -= 1

def checkTurns(orientation): # return value of x, y to the left and right of robot
    if(orientation == 1): # positioned forward relative to starting pt
        if(mazeMap[Y][X + 1] == 1): # left of the robot has been navigated?? DEPENDS ON ORIENTATION, this is on oriented forward, make a variable that tracks orientation values 1 - 4
            return 2 # turn right
        elif(mazeMap[Y][X - 1] == 1): # right of robot
            return 1 # turn left
        
    if(orientation == 2): # positioned turned left horizontal relative to start
        if(mazeMap[Y + 1][X] == 1): # right has been navigated if robot is positioned to the left
            return 1 # turn left
        elif(mazeMap[Y - 1][X] == 1): # spot between robot and x-axis
            return 2 # turn right
          
    if(orientation == 3): # positioned backward relative to starting pt
        if(mazeMap[Y][X + 1] == 1): # left of the robot has been navigated?? DEPENDS ON ORIENTATION, this is on oriented forward, make a variable that tracks orientation values 1 - 4
            return 2 # turn left
        elif(mazeMap[Y][X - 1] == 1): # right of robot
            return 1 # turn right
     
    if(orientation == 4): # positioned turned right horizontal relative to start
        if(mazeMap[Y + 1][X] == 1): # right has been navigated if robot is positioned to the left
            return 2 # turn right
        elif(mazeMap[Y - 1][X] == 1): # spot between robot and x-axis
            return 1 # turn left
  # to use this, use conditionals to determine whether to move left or right based on after using Back Up or turning

try:
    while True:
        checkMagnet()
        if(grovepi.ultrasonicRead(middleUltra) < 20):
            if (grovepi.ultrasonicRead(leftUltra) < 25 and grovepi.ultrasonicRead(rightUltra) < 25):
                backUp(1, orientation)
            elif (grovepi.ultrasonicRead(leftUltra) > 20):
               turnLeft(orientation)
            elif (grovepi.ultrasonicRead(rightUltra) > 20):
               turnRight(orientation)
        elif(grovepi.ultrasonicRead(leftUltra) < 6):
            if(grovepi.ultrasonicRead(leftUltra) < 3):
                Angle(8, 1, -1)
            else:
                Angle(12, 2, 1)
        elif(grovepi.ultrasonicRead(rightUltra) < 6):
            if(grovepi.ultrasonicRead(rightUltra) < 3):
                Angle(8, 2, -1)
            else:
                Angle(12, 1, 1)
        elif((grovepi.analogRead(sensor1) > 40 or grovepi.analogRead(sensor2) > 40)):
            move(orientation)
            markMap(4) # marks heat at space above on map
            backUp(2, orientation)
        elif(totalmag > 100):
            move(orientation)
            markMap(3) # marks magnet source above on map
            backUp(3, orientation)
            
        else:
            BP.set_motor_power(BP.PORT_A + BP.PORT_D, -30)


        if(timeStart + boxTime <= time.time()):
            move(orientation)
            markMap(1)
            print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")
        
        time.sleep(0.001) # hold each loop/iteration for .001 seconds
        
except IOError as error:
    print(error)
except TypeError as error:
    print(error)       
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")
    BP.reset_all()
