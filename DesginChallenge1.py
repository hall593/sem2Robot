import brickpi3
import grovepi
import time

BP = brickpi3.BrickPi3()
ultrasonic_sensor_port = 3

BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.TOUCH) # Configure port

distDesired = 200 # hard for ultrasonic to measure over 300, so parameters set to 200 instead

print("Press touch sensor on port 1 to start")
   

value = 0
up = 0
timeOpen = 0
while not value:
    try: 
        value = BP.get_sensor(BP.PORT_3)
        print(grovepi.ultrasonicRead(ultrasonic_sensor_port))
        if value == 1 and up == 0:
            BP.set_motor_dps(BP.PORT_C + BP.PORT_B, -50)
            time.sleep(2)

            timeOpen = time.time()
            BP.set_motor_dps(BP.PORT_C + BP.PORT_B, 0)
            BP.set_motor_power(BP.PORT_C + BP.PORT_B,0)
            up += 1
            value = 0
        if (grovepi.ultrasonicRead(ultrasonic_sensor_port) > distDesired or time.time() >= timeOpen + 5) and up == 1:
            
            BP.set_motor_dps(BP.PORT_C + BP.PORT_B, 50)
            time.sleep(2)

            BP.set_motor_dps(BP.PORT_C + BP.PORT_B, 0)
            BP.set_motor_power(BP.PORT_C + BP.PORT_B,0)
            up -= 1
            value = 0
            
    except brickpi3.SensorError:
        value = 0
