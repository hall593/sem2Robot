import time
import brickpi3

BP = brickpi3.BrickPi3()

def Angle(angle, side, direction):

# after trial and error, enter the number of degrees the robot itself turns per one second
# divide the desiredAngle by this number to get num seconds to run
    timeRun = angle / 46 # 36 is the number of degrees per sec

    if(side == 1): #  turn left
        BP.set_motor_dps(BP.PORT_D, 120) # left wheel motor, positive turns counterclockwise
        BP.set_motor_dps(BP.PORT_A, -120) # right wheel motor
        time.sleep(timeRun / 2) # runs for one second before turning off
        BP.set_motor_dps(BP.PORT_A + BP.PORT_D, direction * -120)
        time.sleep(1)
        BP.set_motor_dps(BP.PORT_D, 120) # left wheel motor, positive turns counterclockwise
        BP.set_motor_dps(BP.PORT_A, -120)
        time.sleep(timeRun/2)
        BP.set_motor_dps(BP.PORT_A + BP.PORT_D, direction * -120)
        time.sleep(2)
        
    elif(side == 2):
        BP.set_motor_dps(BP.PORT_D, -120) # left wheel motor, positive turns counterclockwise
        BP.set_motor_dps(BP.PORT_A, 120) # right wheel motor
        time.sleep(timeRun / 2)
        BP.set_motor_dps(BP.PORT_A + BP.PORT_D, direction * -120)
        time.sleep(1)
        BP.set_motor_dps(BP.PORT_D, -120) # left wheel motor, positive turns counterclockwise
        BP.set_motor_dps(BP.PORT_A, 120)
        time.sleep(timeRun / 2)
        BP.set_motor_dps(BP.PORT_A + BP.PORT_D, direction * -120)
        time.sleep(2)
        
