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

# vars to contain max
max_g = 0.0
last_pulse = time.time()

while True:

    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)

    # calculate a single g
    g = attitude_math.combine_gs(ax, ay, az)
    if (g > max_g):
        max_g = g
        dlogging.log("New max G: " + str(max_g))

    # is it time to log a pulse?
    since_pulse = time.time() - last_pulse # number of seconds since the last pulse was logged
    if since_pulse > 600: # if it has been more than 10 minutes
        dlogging.log("I am still alive!")
        last_pulse = time.time()


    time.sleep(0.05)