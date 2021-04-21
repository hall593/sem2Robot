from MPU9250 import MPU9250
import time
import math
import brickpi3 # import the BrickPi3 drivers

mpu9250 = MPU9250()

BP = brickpi3.BrickPi3()
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)

tFLAG=0
edgeNew=0
edgeOld=0
fid = open("FieldMagData.csv","w")
fid2 = open("FieldVecData.csv","w")
fid.write("Points,")
fid2.write("Points,")

xwidth=int(input("Enter the total number of x steps: "))
ywidth=int(input("Enter the total number of y steps: "))

for q in range(0,xwidth+1):
    fid.write(str(q))
    fid.write(",")
    fid2.write(str(q))
    fid2.write(",")
    fid2.write(",")
    fid2.write(",")
    
fid.write("\n")
fid2.write("\n")

time.sleep(0.1)

try:
    for x in range(0,xwidth):
        fid.write(str(x))
        fid.write(",")
        fid2.write(str(x))
        fid2.write(",")
        for y in range(0,ywidth):
            print("Move to location ("+str(x)+" , "+str(y)+") and press the button")
            while not tFLAG:
                try:
                    edgeNew = BP.get_sensor(BP.PORT_1)
                    if edgeOld==1 and edgeNew==0:
                        tFLAG=1
                    edgeOld=edgeNew
                except brickpi3.SensorError as error:
                    print(error)
            try:
                mag = mpu9250.readMagnet()
                total_mag=math.sqrt(mag['x']*mag['x']+mag['y']*mag['y']+mag['z']*mag['z'])
                fid.write(str(total_mag))
                fid.write(",")
                fid2.write(str(mag['x']))
                fid2.write(",")
                fid2.write(str(mag['y']))
                fid2.write(",")
                fid2.write(str(mag['z']))
                fid2.write(",")
            except IOError:
                print ("IO Error")
            tFLAG=0
        fid.write("\n")
        fid2.write("\n")
    fid.close()
    fid2.close()
    print("Data Collection Completed.\n")


except KeyboardInterrupt:
    BP.reset_all()
    fid.close()
    fid2.close()
