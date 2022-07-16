from machine import Pin, UART
import nmea

# handles the parsing of data from the NEO-6M module to a telemtry object.
class gps_driver:


    # gpsModule object - set up UART (serial) communication
    __gpsModule__ = None

    def setup(self):
        if self.__gpsModule__ == None:
            self.__gpsModule__ = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

    def get_telemetry(self) -> nmea.gps_telemetry:

        # if the gpsModule hasn't been set up, return none
        if self.__gpsModule__ == None:
            return None

        # get the to return object
        ToReturn = None
        while ToReturn == None:
            # collect line
            line = ""
            line_collected = False
            while line_collected == False:
                tidbit = self.__gpsModule__.readline()
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
                ToReturn = tele
            
        return ToReturn