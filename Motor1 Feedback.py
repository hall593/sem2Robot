# Program provides feedback control based on motor encoder readings
# Developed for in class activity
# ENGR 162, Spring 2018

from MPU9250 import MPU9250
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
mpu9250 = MPU9250()

# initialization
# Tuning parameters
KPA = 3.0 # proportional control gain - motor A
KIA = 0.06 # integral control gain - motor A
KDA = 0.04 # derivative control gain - motor A

KPB = 3.0 # proportional control gain - motor B
KIB = 0.06 # integral control gain - motor B
KDB = 0.04 # derivative control gain - motor B

dT = 0.02 # time step

target_posA = 0
target_posB = 0

current_posA = 0
current_posB = 0

PA = 0
IA = 0
DA = 0
e_prevA = 0

PB = 0
IB = 0
DB = 0
e_prevB = 0

# --------------------------------
# Hardware initialization
# --------------------------------
BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A) )
BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_B) )
#BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH), not using button
BP.set_motor_limits(BP.PORT_A, power=50, dps=200)
BP.set_motor_limits(BP.PORT_B, power=50, dps=200)
# --------------------------------
# ---------------------------------------------------------
# Control loop -- run infinitely until a keyboard interrupt
# ---------------------------------------------------------
try:
    while True:

        gyro_data = mpu9250.readGyro()
        x_position = gyro_data['x']
        y_position = gyro_data['y']
        
        # sig = BP.get_sensor(BP.PORT_1) - not using button
        
        # get current position
        current_posA -= x_position * dT
        current_posB -= y_position * dT
        
        #print("current position: " + str(current_pos) )
        eA = target_posA - current_posA # error
        eB = target_posB - current_posB # error
        print("error A is" + str(eA) + "\n")
        print("error B is" + str(eB) + "\n")

        # set up P,I,D, terms for control inputs: A = motor 1, B = motor 2
        PA = KPA * eA
        IA += KIA * eA * dT/2
        DA = KDA * (eA - e_prevA)/ dT

        PB = KPB * eB
        IB += KIB * eB * dT/2
        DB = KDB * (eB - e_prevB)/ dT


        #print("D" + str(D))
        if True:
            # control input for motor
            power_inA = PA + IA + DA
            power_inB = PB + IB + DB
            
            BP.set_motor_power(BP.PORT_A, power_inA) # power to position motor A
            BP.set_motor_power(BP.PORT_B, power_inB) # power to position motor B
            # save error for this step; needed for D
            e_prevA = eA
            e_prevB = eB
        else:
            BP.set_motor_power(BP.PORT_A, BP.MOTOR_FLOAT) 
        time.sleep(dT)

# ---------------------------------------------------------------------
# If a problem occurse with the while or an interrupt from the keyboard
# ---------------------------------------------------------------------
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()
    BP.set_motor_power(BP.PORT_B, 3) # sets resting resistance of bottom motor to prevent the tray from falling
    BP.set_motor_power(BP.PORT_A, 1) # sets resting resistance of top motor
