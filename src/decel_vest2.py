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
strobe_controller.mute()
_thread.start_new_thread(strobe_controller.continuous_strobe, ())


# create the variables that we will use
gps = gps_driver.gps_driver()
strobe_calc = strobe_calculator.strobe_calculator()

# set up the GPS driver
print("Setting up GPS driver...")
gps.setup()
print("GPS driver set up!")

# print the headers
print("fix_speed_hz", False)

while True:
    try:

        # get the next sentence
        line = gps.collect_nmea_sentence()

        if line != None:
            if nmea.is_gprmc(line):
                fixed = nmea.get_gprmc_fixed(line)
                speed = nmea.get_speed_mph(line)
                if fixed != None and speed != None:
                    hz = strobe_calc.ingest(fixed, speed)
                    if hz != None:
                        #print("Hertz was something: " + str(hz))
                        strobe_controller.set_hertz(hz)
                        strobe_controller.unmute()
                    else:
                        #print("hertz was nothing")
                        strobe_controller.mute()

                    # log the data
                    print(str(fixed) + "_" + str(speed) + "_" + str(hz))


    except Exception as e:
        print("GOT AN ERROR!")
        print("Critical error! Msg: " + str(e))