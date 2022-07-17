from machine import Pin
import gps_driver
import speed_controller
import dlogging

# turn on onboard LED
led = Pin(25, Pin.OUT)
led.value(1)

# create the variables that we will use
gps = gps_driver.gps_driver()
gps.setup()
sc = speed_controller.speed_controller()

# print the headers
dlogging.log("fix_speed_lat_lon_sats", False)

while True:
    try:
        tele = gps.get_telemetry(3000)
        if tele != None:
            if tele.fixed != None and tele.latitude != None and tele.longitude != None:
                sc.ingest(tele.fixed, tele.latitude, tele.longitude) # ingest the speed
                dlogging.log(str(tele.fixed) + "_" + str(sc.speed_mph) + "_" + str(tele.latitude) + "_" + str(tele.longitude) + "_" + str(tele.satellites), False)

    except:
        pass

