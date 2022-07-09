from imu import MPU6050
import time
from machine import Pin, I2C
import attitude_math
import dlogging

# log that I am turned on
dlogging.log("Turned on!")

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
imu = MPU6050(i2c)

while True:
    # Following print shows original data get from libary. You can uncomment to see raw data
    #print(imu.accel.xyz,imu.gyro.xyz,imu.temperature,end='\r')
    
    # Following rows round values get for a more pretty print:
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    dlogging.log("Got values")

    try:
        dlogging.log("Calculating attitude")
        attitude = attitude_math.attitude(ax, ay, az)
        pitch = round(attitude[0], 0)
        roll = round(attitude[1], 0)
        dlogging.log("pitch: " + str(pitch))
        dlogging.log("roll: " + str(roll))
        dlogging.log(str(pitch) + " " + str(roll))
    except Exception as e:
        dlogging.log("ERROR: " + e)

    
    # Following sleep statement makes values enought stable to be seen and
    # read by a human from shell
    time.sleep(0.2)