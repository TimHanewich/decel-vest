import gps_driver
import dlogging

# set up vars
gps = gps_driver.gps_driver()
gps.setup()

while True:
    sentence = gps.collect_nmea_sentence()
    if sentence != None:
        dlogging.log(sentence, True)
