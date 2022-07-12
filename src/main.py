from machine import Pin, UART
import time
import dlogging

# Turn on the LED
led = Pin(25, Pin.OUT)
led.value(1)

gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
dlogging.log(str(gpsModule))

buff = bytearray(255)
TIMEOUT = False
FIX_STATUS = False

latitude = ""
longitude = ""
satellites = ""
GPStime = ""

def convertToDegree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)

def getGPS(gpsModule):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime
    
    timeout = time.time() + 8 
    while True:
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')
    
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                #print(buff)
                
                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = -longitude
                satellites = parts[7]
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                break
                
        if (time.time() > timeout):
            TIMEOUT = True
            break
        time.sleep_ms(500)


while True:
    
    getGPS(gpsModule)

    if(FIX_STATUS == True):
        dlogging.log("dlogging.loging GPS data...")
        dlogging.log(" ")
        dlogging.log("Latitude: "+latitude)
        dlogging.log("Longitude: "+longitude)
        dlogging.log("Satellites: " +satellites)
        dlogging.log("Time: "+GPStime)
        
        FIX_STATUS = False
        
    if(TIMEOUT == True):
        dlogging.log("No GPS data is found.")
        TIMEOUT = False


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