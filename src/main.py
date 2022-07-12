import strobe_controller
import _thread
import time
import dlogging

dlogging.log("About to kick off thread...")
_thread.start_new_thread(strobe_controller.continuous_strobe, ())
dlogging.log("Kicked off!")
dlogging.log("Waiting now...")
time.sleep(10)
dlogging.log("Done waiting.")

dlogging.log("Cycling now...")
for hz in range(2, 40):
    strobe_controller.set_hertz(hz)
    time.sleep(1)

dlogging.log("DONE")

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