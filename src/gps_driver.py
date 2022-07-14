from machine import Pin, UART
import nmea

# handles the parsing of data from the NEO-6M module to a telemtry object.
class gps_driver:

    # call back function when telemetry is received
    __callback__ = None

    def start(self):

        # Create the GPS Module and speed controller, these will be used in the program
        gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

        # continuously collect GPS information and make calculations based on this
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
                if self.__callback__ != None:
                    self.__callback__(tele)

    def set_callback(self, cb):
        self.__callback__ = cb