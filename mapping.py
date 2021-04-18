from MPU9250 import MPU9250
import sys
import time # import time library for sleep and timer function
import brickpi3 # import the BrickPi3 drivers
import grovepi

BP = brickpi3.BrickPi3()
mpu9250 = MPU9250()

ultrasonic_sensor_port1 = 4 # right sensor
ultrasonic_sensor_port2 = 8 # middle sensor
ultrasonic_sensor_port3 = 7 # left sensor

timeRunning = 0
timeStart = time.time()

deltaT = 0.01
yVelocity = 0
xVelocity = 0

lastXPos = 0
lastYPos = 0
currentX = 0
currentY = 0

mazeMap = [[ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0]]
startingPtX = int(input("Please enter the X coordinate of the starting point: "))
startingPtY = int(input("Please enter the Y coordinate of the starting point: "))
ptDistance = int(input("Please enter the distance between pts (in cm): "));

# after trial and error, enter the number of degrees the robot itself turns per one second
# divide the desiredAngle by this number to get num seconds to run

mazeMap[startingPtY][startingPtX] = 5

def moveY(current, lastPos):
    if(current - lastPos < 0):
        return -1
    elif(current - lastPos > 0):
        return 1

def moveX(current, lastPos):
    if(currrent - lastPos < 0):
        return -1
    elif(current - lastPos > 0):
        return 1

def checkMap():
    accel_data = mpu9250.readAccel()
    x_accel = accel_data['x']
    y_accel = accel_data['y']

    yVelocity = y_accel * deltaT + yVelocity # Euler's method to calculate velocity
    xVelocity = x_accel * deltaT + xVelocity

    if(y_accel == 0):
        yVelocity = 0
    if(x_accel == 0):
        xVelocity = 0

    currentY = yVelocity * deltaT + currentY # Euler's method to calculate position of robot
    currentX = xVelocity * deltaT + currentX


    if (abs(currentY - lastYPos) >= ptDistance):
        startingPtY += moveY(currentY, lastYPos)
        if(startingPtY < 7 and startingPtY > -1):
            mazeMap[startingPtY][startingPtX] = 1
        lastYPos = currentY
        print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")

            
    if (abs(currentX - lastXPos) >= ptDistance):
        startingPtX += moveX(currentX, lastXPos)
        if(startingPtX < 7 and startingPtX > -1):
            mazeMap[startingPtY][startingPtX] = 1
        lastXPos = currentX
        print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")


    if((startingPtY > 6 or startingPtY < 0) or (startingPtX > 6 or startingPtX < 0)):
        print("Outside Matrix bounds, terminate")
        BP.reset_all()

def turnLeft():
    timeStart = time.time()
    while(timeStart + 3 >= time.time()):
        BP.set_motor_power(BP.PORT_A,-30)
        BP.set_motor_power(BP.PORT_D,30)

def turnRight(): # if there's a wall in front, will need to implement check left or right to determine to turn left or right after encountering an obstacle
    timeStart = time.time()
    while(timeStart + 3 >= time.time()):
        BP.set_motor_power(BP.PORT_A,-30)
        BP.set_motor_power(BP.PORT_D,30)

def backUp(): 
    timeStart = time.time()
    while(grovepi.ultrasonicRead(ultrasonic_sensor_port1) < 15 and (grovepi.ultrasonicRead(ultrasonic_sensor_port3) < 15)):
        BP.set_motor_power(BP.PORT_A + BP.PORT_D, 30)

try:
    while True:
        if(grovepi.ultrasonicRead(ultrasonic_sensor_port2) < 21):
           if(grovepi.ultrasonicRead(ultrasonic_sensor_port1) < 15 and (grovepi.ultrasonicRead(ultrasonic_sensor_port3) < 15)):
               backUp()
           elif (grovepi.ultrasonicRead(ultrasonic_sensor_port3) < 15):
               turnRight()
           elif (grovepi.ultrasonicRead(ultrasonic_sensor_port1) < 15):
               turnLeft()
           break
        else:
            BP.set_motor_power(BP.PORT_A + BP.PORT_D, -30)
            
        checKMap()
        
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")
    BP.reset_all()
        
        

