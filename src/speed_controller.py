import nmea

class speed_controller:

    # public variables
    speed_mph = None
    acceleration_mphs = None

    # private variables
    __speed_at__ = None
    __acceleration_at__ = None
    __last_gps_tele__= None

    def ingest(self, tele:nmea.gps_telemetry):

        # if speed is not set, just set it to 0
        if self.speed_mph == None and self.__speed_at__ == None:
            self.speed_mph = 0
            self.__speed_at__ = 0

        # do we have enough to calculate?
        if tele.fixed != None and tele.latitude != None and tele.longitude != None: #this package contains all of the things we need
            
            # calculate speed?
            if self.__last_gps_tele__ != None: # we have old data
                if tele.fixed > self.__last_gps_tele__.fixed: # this telemetry occurs after the last received
                    if tele.latitude != self.__last_gps_tele__ .latitude or tele.longitude != self.__last_gps_tele__ .longitude: #we have moved from the last position

                        # calculate speed
                        dist = nmea.distance(self.__last_gps_tele__ .latitude, self.__last_gps_tele__ .longitude, tele.latitude, tele.longitude)
                        hours = (tele.fixed - self.__last_gps_tele__ .fixed) / 60 / 60
                        speed_mph = dist / hours

                        # Now that we have the current speed, calculate acceleration in mph/s
                        if self.speed_mph != None and self.__speed_at__ != None:
                            acc = (speed_mph - self.speed_mph) / (tele.fixed - self.__speed_at__)
                            
                            # if the acceleration is deemed realistic, save it
                            if acc < 32.0:

                                # save them
                                self.speed_mph = speed_mph
                                self.__speed_at__ = tele.fixed
                                self.acceleration_mphs = acc
                                self.__acceleration_at__ = tele.fixed

                        

            # Since this has the data we need, save it
            self.__last_gps_tele__ = tele