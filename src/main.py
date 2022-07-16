import gps_driver
import nmea
import _thread
from machine import Pin
import speed_controller
import dlogging
import strobe_calculator
import strobe_controller
import settings
import time

#set up LED pin
led = Pin(25, Pin.OUT)

# flash the strobe light and the onboard LED at the same time to confirm it is on
strobe_pin = Pin(settings.gpio_strobe, Pin.OUT)
strobe_pin.value(1)
led.value(1)
time.sleep(0.5)
strobe_pin.value(0)
led.value(0)
time.sleep(0.5)
strobe_pin.value(1)
led.value(1)
time.sleep(0.5)
strobe_pin.value(0)
led.value(0)
time.sleep(0.5)

# turn on LED hold
led.value(1)


# start the strobe light controller
_thread.start_new_thread(strobe_controller.continuous_strobe, ())
strobe_controller.mute()

# create the variables that we will use
gps = gps_driver.gps_driver()
sc = speed_controller.speed_controller()
strobe_calc = strobe_calculator.strobe_calculator()

# set up the GPS driver
print("Setting up GPS driver...")
gps.setup()
print("GPS driver set up!")

# print the headers
print("fix_speed_lat_lon_sats_hz", False)

while True:
    try:

        # get telemetry from the gps driver
        print("Getting telemetry")
        tele = gps.get_telemetry(3000)
        print("Telemetry received!")

        if tele != None:
            print("Telemetry was not None!")
            if tele.fixed != None and tele.latitude != None and tele.longitude != None:
                print("We have the necessary data...")
                
                # calculate  the speed
                print("Calculating speed...")
                sc.ingest(tele.fixed, tele.latitude, tele.longitude) #ingest the data to get the speed
                print("sc ingested.")
        
                # if we have the speed (which we should, try to calculate the strobe speed)
                if sc.speed_mph != None:
                    print("We have an MPH!")

                    # calculate the appropriate hertz of the light
                    print("Going to calculate hz")
                    hz = strobe_calc.ingest(tele.fixed, sc.speed_mph)
                    if hz != None:
                        print("Hertz was something: " + str(hz))
                        strobe_controller.set_hertz(hz)
                        strobe_controller.unmute()
                    else:
                        print("hertz was nothing")
                        strobe_controller.mute()

                    # log the data
                    print(str(tele.fixed) + "_" + str(sc.speed_mph) + "_" + str(tele.latitude) + "_" + str(tele.longitude) + "_" + str(tele.satellites) + "_" + str(hz), False)
    
    except Exception as e:
        print("GOT AN ERROR!")
        print("Critical error! Msg: " + str(e))
