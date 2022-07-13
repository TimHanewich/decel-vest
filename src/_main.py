from machine import Pin, UART
import time
import dlogging
import nmea

# Turn on the LED
led = Pin(25, Pin.OUT)
led.value(1)

gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
dlogging.log("Ready to go!")

while True:

    # collect line
    line = ""
    line_collected = False
    while line_collected == False:
        tidbit = gpsModule.readline()
        if tidbit != None:

            # Try to decode
            tidbit_txt = None
            try:
                tidbit_txt = tidbit.decode()
            except:
                tidbit_txt = None
            
            # if it decoded successfully, ad it to the line
            if tidbit_txt != None:
                line = line + tidbit_txt

            # is it now fully collected?
            if "*" in line:
                line_collected = True

    # now that the line is collected, parse it
    try:
        nmea.parse(line)
        dlogging.log(str(nmea.latitude) + "," + str(nmea.longitude) + " - " + str(nmea.satellites) + " on " + line)
    except Exception as e:
        dlogging.log("Failed: " + str(e))
        try:
            dlogging.log("From that error: " + line)
        except:
            pass


# import strobe_controller
# import _thread
# import time
# import settings
# from imu import MPU6050
# from machine import Pin, I2C
# import attitude_math
# import math
# import strobe_tools

# _thread.start_new_thread(strobe_controller.continuous_strobe, ())

# # Turn on the status LED
# led = Pin(25, Pin.OUT)
# led.value(1)

# i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
# imu = MPU6050(i2c)

# while True:

#     ax=round(imu.accel.x,2)
#     ay=round(imu.accel.y,2)
#     az=round(imu.accel.z,2)
    
#     attitude = attitude_math.attitude(ax, ay, az)
#     pitch = abs(attitude[0])
#     pitch_percentage = pitch / 90
    
#     hz = strobe_tools.select_hertz(pitch_percentage)
#     strobe_controller.set_hertz(hz)

#     time.sleep(0.5)