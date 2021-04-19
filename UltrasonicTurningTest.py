import time
import brickpi3
import grovepi

from TurnDegrees import Angle
from MPU9250 import MPU9250

BP = brickpi3.BrickPi3()
imu = MPU9250()

leftUltra = 4 # left sensor
middleUltra = 8 # middle sensor
rightUltra = 7 # right sensor

sensor1 = 14 # left IR sensor
sensor2 = 15 # right IR sensor

distDesired = 20
totalmag = 0

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
        
def backUp(instance): # need to implement instance of changing map indicator, although could be a separate function
    if(instance == 1):
        while(grovepi.ultrasonicRead(leftUltra) < 30 and grovepi.ultrasonicRead(rightUltra) < 30):
            BP.set_motor_power(BP.PORT_A + BP.PORT_D, 30)
        BP.set_motor_power(BP.PORT_A + BP.PORT_D, 30)
        time.sleep(1)
    
        if(grovepi.ultrasonicRead(rightUltra) > 20):
            turnRight()
        elif(grovepi.ultrasonicRead(leftUltra) > 20):
            turnLeft()
   if(instance == 2): # in the instance that a magnet is sensed
        while((grovepi.analogRead(sensor1) > 40 or grovepi.analogRead(sensor2) > 40) and (grovepi.ultrasonicRead(leftUltra) < 30 and grovepi.ultrasonicRead(rightUltra) < 30)):
            BP.set_motor_power(BP.PORT_A + BP.PORT_D, 30)
   if(instance == 3):
        while(totalmag > 100 and (grovepi.ultrasonicRead(leftUltra) < 30 and grovepi.ultrasonicRead(rightUltra) < 30)):
            BP.set_motor_power(BP.PORT_A + BP.PORT_D, 30)
            checkMagnet()
       
def checkMagnet():
    mag = imu.readMagnet()
    total_mag=math.sqrt(mag['x']*mag['x']+mag['y']*mag['y']+mag['z']*mag['z'])
# def checkMap(): # in the instance the robot backs up, must check the map to maneuver to an unnavigated place, need mapping function implemented in order to use




# Main logic    
try:
    while True:
        checkMagnet()
        
        if(grovepi.ultrasonicRead(middleUltra) < 20):
            if (grovepi.ultrasonicRead(leftUltra) < 25 and grovepi.ultrasonicRead(rightUltra) < 25):
                backUp(1)
            elif (grovepi.ultrasonicRead(leftUltra) > 20):
               turnLeft()
            elif (grovepi.ultrasonicRead(rightUltra) > 20):
               turnRight()
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
        if((grovepi.analogRead(sensor1) > 40 or grovepi.analogRead(sensor2) > 40)):
            backUp(2)
        if(totalmag > 100):
            backUp(3)
            
        else:
            BP.set_motor_power(BP.PORT_A + BP.PORT_D, -30)

        print("This is left ultra: ", grovepi.ultrasonicRead(leftUltra))
        print("This is middle ultra: ", grovepi.ultrasonicRead(middleUltra))
        print("This is right ultra: ", grovepi.ultrasonicRead(rightUltra))


            
        time.sleep(0.001) # hold each loop/iteration for .001 seconds

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    print("You pressed ctrl+C...")
    BP.reset_all()
    
# use reset_all() to return all motors and sensors to resting states
