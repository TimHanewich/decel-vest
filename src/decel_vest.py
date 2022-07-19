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
strobe_pin = Pin(settings.gpio_strobe1, Pin.OUT)
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
strobe_calc.setup() #parse the polygons from the onboard polygons.json file

# set up the GPS driver
print("Setting up GPS driver...")
gps.setup()
print("GPS driver set up!")

# print the headers
print("fix_speed_hz", False)

def act_on_speed(fixed:int, speed_mph:float):

    global strobe_calc

    hz = strobe_calc.ingest(fixed, speed)

    # set the hz that we have
    if hz == None: # nothing was provided, so mute the lights (show nothing)
        strobe_controller.mute()
    elif type(hz) == float: # a hz was provided, so make sure we are in hz mode, set the hz, and then show it!
        strobe_controller.set_mode(strobe_controller.mode_hz) #set to hz mode
        strobe_controller.set_hertz(hz)
        strobe_controller.unmute()
    elif type(hz) == str: # a string value was provided, signifying we are following a standard pattern
        if hz == "polygon": # we are within a polygon, so set the mode to pit lane mode
            strobe_controller.set_mode(strobe_controller.mode_pit) #set to pit lane mode

def act_on_gps(latitude:float, longitude:float):
    global strobe_calc
    strobe_calc.ingest_gps(tele.latitude, tele.longitude)

while True:
    try:

        # get the next sentence
        line = gps.collect_nmea_sentence()

        # try to get the hz to set
        if line != None:
            if nmea.is_gprmc(line): #a $GPRMC line, which contains the speed
                fixed = nmea.get_gprmc_fixed(line)
                speed = nmea.get_speed_mph(line)
                if fixed != None and speed != None:
                    act_on_speed(fixed, speed)
                    print(str(fixed) + "_" + str(speed) + "_" + str(hz))
            elif nmea.is_gpgga(line):
                tele = nmea.parse(line)
                if tele != None:
                    if tele.latitude != None and tele.longitude != None:
                        act_on_gps(tele.latitude, tele.longitude)
                        print("GPS logged: " + str(tele.latitude) + ", " + str(tele.longitude))


    except Exception as e:
        print("GOT AN ERROR!")
        print("Critical error! Msg: " + str(e))
