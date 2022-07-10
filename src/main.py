from imu import MPU6050
import time
from machine import Pin, I2C
import attitude_math
import dlogging
import _thread

# log an "I'm on!" message
dlogging.log("main.py started! Hello world!")

# Kick off thread to handle blinking LED
led = Pin(25, Pin.OUT)
def ContinuousBlinking():
    while True:
        led.value(1)
        time.sleep(0.5)
        led.value(0)
        time.sleep(0.5)
_thread.start_new_thread(ContinuousBlinking, ())


i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
imu = MPU6050(i2c)


while True:

    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    tem=round(imu.temperature,2)

    # Log it
    dlogging.log(str(ax) + "_" + str(ay) + "_" + str(az) + "_" + str(tem))

    time.sleep(0.6)