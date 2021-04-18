from MPU9250 import MPU9250
import time
import math
import brickpi3

mpu9250 = MPU9250()

BP = brickpi3.BrickPi3()

try:
    while True:
        mag = mpu9250.readMagnet()
        total_mag=math.sqrt(mag['x']*mag['x']+mag['y']*mag['y']+mag['z']*mag['z'])
        print("Total magnitude = ", total_mag)
        print("x value = ", str(mag['x']))
        print("y value = ", str(mag['y']))
        print("z value = ", str(mag['z']))
        time.sleep(1)

except KeyboardInterrupt:
    BP.reset_all()


# starting values
# magnet in front (x pointing towards magnet) = -34.8
# magnet in the side ( y pointing left and right) = 56.46
# z is upwards = 5 - 6.5

# magnet in front (default) = x = -25, y = 51 z = 0 - -2
# changing field to y (right side) = x = -24, y = 55, z = 67
# magnet over the IMU = 
