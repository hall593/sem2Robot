from MPU9250 import MPU9250
import sys
import time # import time library for sleep and timer function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3()
mpu9250 = MPU9250()

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
desiredAngle = int(input("Please enter the desired angle to turn: "))

# after trial and error, enter the number of degrees the robot itself turns per one second
# divide the desiredAngle by this number to get num seconds to run
timeRun = desiredAngle / 36 # 36 is the number of degrees per sec

mazeMap[startingPtY][startingPtX] = 5

try:
    while True:
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
            print("starting ptY: ", startingPtY)
            if(currentY - lastYPos < 0):
                if(startingPtY != 0):
                    startingPtY -= 1
                
            elif(currentY - lastYPos > 0):
                
                startingPtY += 1

            mazeMap[startingPtY][startingPtX] = 1

            #print("Accel Y: ", y_accel, " Velocity Y: ", yVelocity, " currentY: ", currentY, "last Y pos: ", lastYPos)

            lastYPos = currentY

            print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")
            
        if (abs(currentX - lastXPos) >= ptDistance):
            print("starting ptX: ", startingPtX)
            
            if(currentX - lastXPos < 0):
                if(startingPtX != 0):
                    startingPtX -= 1 
                
            elif(currentX - lastXPos > 0):
                
                startingPtX += 1

            mazeMap[startingPtY][startingPtX] = 1
            lastXPos = currentX

            #print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")

        #if((startingPtY > 6 or startingPtY < 0) or (startingPtX > 6 or startingPtX < 0)):
            #print("Outside Matrix bounds, terminate")
            #print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")

        
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    print(mazeMap[0], "\n", mazeMap[1], "\n", mazeMap[2], "\n", mazeMap[3], "\n", mazeMap[4], "\n", mazeMap[5], "\n", mazeMap[6], "\n")
    BP.reset_all()
        
        
