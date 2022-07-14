import nmea

class speed_controller:

    # public variables
    speed_mph = 0.0 # starts off at 0
    acceleration_mphs = 0.0

    # private variables
    __last_fix__ = None
    __last_lat__ = None
    __last_lon__ = None

    # private variables - used for checking if the calculated speed is legit. Is it feasible?
    __speed_fix__ = None # the fixed time the speed was determined

    def ingest(self, fix:int, lat:float, lon:float):

        # Set the last time speed was fixed to now if it is blank. Just set it to a second ago.
        if self.__speed_fix__ == None:
            self.__speed_fix__ = fix - 1

        # Try to calculate speed, if we have the data of course
        if self.__last_fix__ != None and self.__last_lat__ != None and self.__last_lon__ != None:
            if fix > self.__last_fix__: #this occurs after the data we already have (error prevention)

                # distance calculation
                distance_miles = nmea.distance(self.__last_lat__, self.__last_lon__, lat, lon)

                # hours calculation
                hours = (fix - self.__last_fix__) / 60 / 60 # calculate the hours since the last one we received. Divide by 60 twice to go from seconds to hours

                # caculate apparent MPH
                apparent_speed_mph = distance_miles / hours

                # calculate the MPH/S to determine if this is feasible
                apparent_acceleration_mphs = (apparent_speed_mph - self.speed_mph) / (fix - self.__speed_fix__)

                # if the apparent acceleration is feasible, believe it and log the new speed
                if abs(apparent_acceleration_mphs) < 32:
                    print("Aparent acceleration feasible")
                    self.speed_mph = apparent_speed_mph
                    self.__speed_fix__ = fix
                    self.acceleration_mphs = apparent_acceleration_mphs
                else:
                    print("Aparent acceleration NOT FEASIBLE")
                    print("P1: " + str(self.__last_lat__) + "," + str(self.__last_lon__ + " --> " + str(lat) + "," + str(lon)))
                    print("Distance: " + str(distance_miles))
                    print("Hours: " + str(hours))
                    print("Apparent speed MPH: " + str(apparent_speed_mph))
                    print("Apparent acceleration MPH/s: " + str(apparent_acceleration_mphs))

        # set them
        self.__last_fix__ = fix
        self.__last_lat__ = lat
        self.__last_lon__ = lon
