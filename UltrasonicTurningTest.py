import time
import brickpi3
import grovepi

from TurnDegrees import Angle

BP = brickpi3.BrickPi3()

leftUltra = 4 # left sensor
middleUltra = 8 # middle sensor
rightUltra = 7 # right sensor

distDesired = 20

def turnLeft():
    Angle(91, 1, 1)
    #while(grovepi.ultrasonicRead(ultrasonic_sensor_port3) < 25 and grovepi.ultrasonicRead(ultrasonic_sensor_port2) < 25):
        #BP.set_motor_power(BP.PORT_A, -30) # originally 30
        #BP.set_motor_power(BP.PORT_D, 30)

def turnRight(): # if there's a wall in front, will need to implement check left or right to determine to turn left or right after encountering an obstacle
    Angle(91, 2, 1)
    #while(grovepi.ultrasonicRead(ultrasonic_sensor_port1) < 25 and grovepi.ultrasonicRead(ultrasonic_sensor_port2) < 25):
        #BP.set_motor_power(BP.PORT_A, 30) # originally 30
        #BP.set_motor_power(BP.PORT_D, -30)
        
def backUp():
    while(grovepi.ultrasonicRead(leftUltra) < 30 and grovepi.ultrasonicRead(rightUltra) < 30):
        BP.set_motor_power(BP.PORT_A + BP.PORT_D, 30)
    BP.set_motor_power(BP.PORT_A + BP.PORT_D, 30)
    time.sleep(1)

    if(grovepi.ultrasonicRead(rightUltra) > 20):
        turnRight()
    elif(grovepi.ultrasonicRead(leftUltra) > 20):
        turnLeft()
    
# def checkMap(): # in the instance the robot backs up, must check the map to maneuver to an unnavigated place, need mapping function implemented in order to use




# Main logic    
try:
    while True:
        print("hello")
        if(grovepi.ultrasonicRead(middleUltra) < 20):
            if (grovepi.ultrasonicRead(leftUltra) < 25 and grovepi.ultrasonicRead(rightUltra) < 25):
                backUp()
            elif (grovepi.ultrasonicRead(leftUltra) > 20):
               turnLeft()
            elif (grovepi.ultrasonicRead(rightUltra) > 20):
               turnRight()
        if(grovepi.ultrasonicRead(leftUltra) < 6):
            if(grovepi.ultrasonicRead(leftUltra) < 3):
                Angle(8, 1, -1)
            else:
                Angle(12, 2, 1)
        if(grovepi.ultrasonicRead(rightUltra) < 6):
            if(grovepi.ultrasonicRead(rightUltra) < 3):
                Angle(8, 2, -1)
            else:
                Angle(12, 1, 1)
        else:
            BP.set_motor_power(BP.PORT_A + BP.PORT_D, -30)

        print("This is left ultra: ", grovepi.ultrasonicRead(leftUltra))
        print("This is middle ultra: ", grovepi.ultrasonicRead(middleUltra))
        print("This is right ultra: ", grovepi.ultrasonicRead(rightUltra))


            
        time.sleep(0.00001) # hold each loop/iteration for .000001 seconds

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    print("You pressed ctrl+C...")
    BP.reset_all()
    
# use reset_all() to return all motors and sensors to resting states
