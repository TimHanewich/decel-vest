from machine import Pin, UART
import time
import dlogging
import nmea
import speed_controller


# Turn on the LED
led = Pin(25, Pin.OUT)
led.value(1)

gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
sc = speed_controller.speed_controller()

while True:

    # collect line
    line = ""
    line_collected = False
    while line_collected == False:
        tidbit = gpsModule.readline()
        if tidbit != None:

            # Try to decode
            tidbit_txt = None
            try:
                tidbit_txt = tidbit.decode()
            except:
                tidbit_txt = None
            
            # if it decoded successfully, ad it to the line
            if tidbit_txt != None:
                line = line + tidbit_txt
                
            # is it now fully collected?
            if "*" in line:
                line_collected = True

    # now that the line is collected, parse it into GPS telemetry
    tele = None
    try:
        tele = nmea.parse(line)
    except:
        tele = None

    # if it parsed into a gps telemetry, feed it
    if tele != None:
        sc.ingest(tele)

    # save
    dlogging.log("MPH: " + str(sc.speed_mph) + "   MPH/S: " + str(sc.acceleration_mphs))