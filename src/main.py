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
    dlogging.log("Going to collect line now!")
    line = ""
    line_collected = False
    while line_collected == False:
        dlogging.log("reading lien now...")
        tidbit = gpsModule.readline()
        dlogging.log("Line read!")
        if tidbit != None:

            dlogging.log("line was not null!")

            # Try to decode
            tidbit_txt = None
            try:
                tidbit_txt = tidbit.decode()
                dlogging.log("Decoded!")
            except:
                tidbit_txt = None
                dlogging.log("Decoding failed.")
            
            # if it decoded successfully, ad it to the line
            if tidbit_txt != None:
                line = line + tidbit_txt
                dlogging.log("Appended to line!")
                
            # is it now fully collected?
            if "*" in line:
                dlogging.log("Marking as fully collected")
                line_collected = True
        else:
            dlogging.log("Line was NONE!")

    # now that the line is collected, parse it
    try:
        dlogging.log("Trying to parse now...")
        nmea.parse(line)
        dlogging.log(str(nmea.latitude) + "," + str(nmea.longitude) + " = " + str(nmea.speed_mph))
    except Exception as e:
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