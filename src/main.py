import gps_driver
import nmea
import _thread
from machine import Pin
import speed_controller
import dlogging
import strobe_calculator
import strobe_controller

# Set up the on-board LED
led = Pin(25, Pin.OUT)
led.value(1)

# start the strobe light controller
_thread.start_new_thread(strobe_controller.continuous_strobe, ())
strobe_controller.mute()

# create the variables that we will use
sc = speed_controller.speed_controller()
strobe_calc = strobe_calculator.strobe_calculator()

# print the headers
dlogging.log("fix_speed_lat_lon_sats_hz", False)

# write the function that will handle the receiving of gps
def process_gps_tele(tele:nmea.gps_telemetry):
    try:
        global sc
        global strobe_calc

        if tele != None:
            if tele.fixed != None and tele.latitude != None and tele.longitude != None:
                
                # calculate  the speed
                sc.ingest(tele.fixed, tele.latitude, tele.longitude) #ingest the data to get the speed
        
                # calculate the appropriate hertz of the light
                hz = strobe_calc.ingest(tele.fixed, sc.speed_mph)
                if hz != None:
                    strobe_controller.set_hertz(hz)
                    strobe_controller.unmute()
                else:
                    strobe_controller.mute()

                # log the data
                dlogging.log(str(tele.fixed) + "_" + str(sc.speed_mph) + "_" + str(tele.latitude) + "_" + str(tele.longitude) + "_" + str(tele.satellites) + "_" + str(hz), False)
    except Exception as e:
        dlogging.log("Critical error! Msg: " + str(e))

# start the gps driver
gps = gps_driver.gps_driver()
gps.set_callback(process_gps_tele)
_thread.start_new_thread(gps.start(), ())