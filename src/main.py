import gps_driver
import nmea
import _thread
from machine import Pin
import speed_controller
import dlogging

# Turn on the LED
led = Pin(25, Pin.OUT)
led.value(1)

# create the variables that we will use
sc = speed_controller.speed_controller()

# print the headers
dlogging.log("fix_speed_lat_lon_sats", False)

# write the function that will handle the receiving of gps
def process_gps_tele(tele:nmea.gps_telemetry):
    global sc
    if tele != None:
        if tele.fixed != None and tele.latitude != None and tele.longitude != None:
            sc.ingest(tele.fixed, tele.latitude, tele.longitude)
    
    dlogging.log(str(tele.fixed) + "_" + str(sc.speed_mph) + "_" + str(tele.latitude) + "_" + str(tele.longitude) + "_" + str(tele.satellites))

# start the gps driver
gps = gps_driver.gps_driver()
gps.set_callback(process_gps_tele)
_thread.start_new_thread(gps.start(), ())