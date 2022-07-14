import gps_driver
import nmea
import _thread
from machine import Pin
import speed_controller

# Turn on the LED
led = Pin(25, Pin.OUT)
led.value(1)

# create the variables that we will use
sc = speed_controller.speed_controller()


# write the function that will handle the receiving of gps
def process_gps_tele(tele:nmea.gps_telemetry):
    global sc
    if tele != None:
        if tele.fixed != None and tele.latitude != None and tele.longitude != None:
            sc.ingest(tele.fixed, tele.latitude, tele.longitude)
    
    print(str(tele.fixed) + " = " + str(sc.speed_mph))

# start the gps driver
gps = gps_driver.gps_driver()
gps.set_callback(process_gps_tele)
_thread.start_new_thread(gps.start(), ())