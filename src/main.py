import gps_driver
import nmea
import _thread
from machine import Pin

# Turn on the LED
led = Pin(25, Pin.OUT)
led.value(1)


# write the function that will handle the receiving of gps
def print_tele(tele:nmea.gps_telemetry):
    print(str(tele.fixed) + " - " + str(tele.latitude) + "," + str(tele.longitude))

# start the gps driver
gps = gps_driver.gps_driver()
gps.set_callback(print_tele)
_thread.start_new_thread(gps.start(), ())