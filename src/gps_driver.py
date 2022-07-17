from machine import Pin, UART
import nmea
import time
import dlogging
import settings

# handles the parsing of data from the NEO-6M module to a telemtry object.
class gps_driver:


    # gpsModule object - set up UART (serial) communication
    __gpsModule__ = None

    def setup(self):
        if self.__gpsModule__ == None:
            self.__gpsModule__ = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(settings.gpio_gps_rx))


    def collect_nmea_sentence(self, timeout_ms:int = 5000) -> str:
        
        # if the gpsModule hasn't been set up, return none
        if self.__gpsModule__ == None:
            return None
        
        # collect line
        line = ""
        line_collected = False
        StartedCollectionAt = time.ticks_ms()
        while line_collected == False and (time.ticks_ms() - StartedCollectionAt) < timeout_ms:
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

        # at this point, we have either collected it successfully (the hope) or reached the timeout.
        if line != "" and "*" in line:
            return line
        else: # a sentence was not collected successfully
            return None
        

    def get_telemetry(self, timeout_ms:int = 5000) -> nmea.gps_telemetry:

        # get the to return object
        ToReturn = None
        StartedSearchAt = time.ticks_ms()
        while ToReturn == None and (time.ticks_ms() - StartedSearchAt) < timeout_ms:
            
            # collect an nmea scentence
            line = self.collect_nmea_sentence(timeout_ms)

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