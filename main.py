from imu import MPU6050
import time
from machine import Pin, I2C
import attitude_math
import dlogging

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
imu = MPU6050(i2c)

# vars to contain max
max_g = 0.0

while True:

    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)

    # calculate a single g
    g = attitude_math.combine_gs(ax, ay, az)
    if (g > max_g):
        max_g = g
        dlogging.log("New max G: " + str(max_g))

    time.sleep(0.05)