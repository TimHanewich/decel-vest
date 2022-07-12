import time
import machine

led = machine.Pin(1, machine.Pin.OUT)
while True:
    led.value(1)
    time.sleep(1)
    led.value(0)
    time.sleep(1)


# from imu import MPU6050
# import time
# from machine import Pin, I2C
# import dlogging

# # log an "I'm on!" message
# dlogging.log("main.py started! Hello world!")

# # Turn on the status LED
# led = Pin(25, Pin.OUT)
# led.value(1)

# i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
# imu = MPU6050(i2c)

# while True:

#     try:

#         ax=round(imu.accel.x,2)
#         ay=round(imu.accel.y,2)
#         az=round(imu.accel.z,2)
#         tem=round(imu.temperature,2)

#         # Log it
#         dlogging.log(str(ax) + "_" + str(ay) + "_" + str(az) + "_" + str(tem))

#     except:
#         dlogging.log("Critical failure while reading!")

#     time.sleep(0.5)