import nmea
import strobe_tools
import settings
import boundary


# MODE VALUES
AwaitingDeceleration = 0, # nothing is happening right now
Decelerating = 1

class fixed_speed:
    fixed = 0.0 #time stamp of when the speed was detected
    speed = 0.0 #speed that was detected


class strobe_calculator:

    # variables for seeing if we are in one of the polygon areas
    __polygons__ = None
    __last_lat__ = None
    __last_lon__ = None

    # variables for tracking
    __last_speed_mph__ = None #the speed that was most recently received
    __last_fixed__ = None #the last fixed time that the speed was received at
    __mode__ = AwaitingDeceleration

    # averaging out the deceleration
    __fixed_speed_buff__ = []
    __buff_len__ = 9999 # how many speed logs will be considered as a buffer. You can rasie this to an extremely large number (like 9999) for it to just average out the entirety of the deceleration. So no longer how long the deceleration is, the hz of the strobe will be calculated on the average deceleration from the start of the deceleration to the end.

    def add_fixed_speed(self, fs:fixed_speed):
        self.__fixed_speed_buff__.append(fs)
        while len(self.__fixed_speed_buff__) > self.__buff_len__:
            self.__fixed_speed_buff__.pop(0)

    def avg_accel(self):

        if len(self.__fixed_speed_buff__) > 1:
            # Calculate by calculating the acceleration between the first and last one. This is apparently the same as the one above
            # get speeds
            speed1 = self.__fixed_speed_buff__[len(self.__fixed_speed_buff__)-1].speed
            speed2 = self.__fixed_speed_buff__[0].speed

            # get fixed
            fixed1 = self.__fixed_speed_buff__[len(self.__fixed_speed_buff__)-1].fixed
            fixed2 = self.__fixed_speed_buff__[0].fixed

            # calculate accel
            accel = (speed2 - speed1) / (fixed2 - fixed1)
            return accel
        else:
            return None

    def ingest_gps(self, lat:float, lon:float):
        self.__last_lat__ = lat
        self.__last_lon__ = lon

    def setup(self):
        try:
            polygons = boundary.parse_file(settings.polygon_file_path)
            self.__polygons__ = polygons
        except:
            pass

    # outputs a recommended hertz
    def ingest(self, fixed:int, speed_mph:float):

        # take a copy of what the old data is. We do this because we need to use it later, but must set it right after this (before calculations) because the calculations may return a value and therefore terminate the program. So therefore we need to set it up here, not after the calculation
        old_speed = self.__last_speed_mph__
        old_fixed = self.__last_fixed__

        # set the old data
        self.__last_speed_mph__ = speed_mph
        self.__last_fixed__ = fixed

        # Check if we are inside a polygon
        if self.__last_lat__ != None and self.__last_lon__ != None:
            if self.__polygons__ != None:
                for polygon in self.__polygons__:
                    loc = boundary.Point()
                    loc.X = self.__last_lat__
                    loc.Y = self.__last_lon__
                    inside = boundary.IsPointInPolygon(loc, polygon)
                    if inside:
                        return "polygon"

            

        # Now that none of the above returned anything, we get to this point, meaning that we will have to check what the hz will be based on the decelration or lack of deceleration
        # at this point, we will either be returning None or a float, representing the hz to adjust to
        # if we have old data
        if old_speed != None and old_fixed != None:

            # calculate acceleration/deceleration - acceleration would be positie, deceleration would be negative
            accel_mphs = (speed_mph - old_speed) / (fixed - old_fixed)

            # if we are currently in decelerating mode, check to see if it is over. If it is over, return none
            if self.__mode__ == Decelerating: # we are currently decelerating
                if accel_mphs > (settings.min_decel_sustained * -1): # if we are no longer decelerating in the window

                    # clear the deceleration log
                    self.__fixed_speed_buff__.clear()

                    # mark the status as awaiting deceleration (neutral)
                    self.__mode__ = AwaitingDeceleration

                    # Return None, indicating that there isn't a deceleration going on
                    return None                

            # if we are currently cruising, check to see if we are now decelerating
            if self.__mode__ == AwaitingDeceleration: #we are waiting for something to happen
                if speed_mph < old_speed: # we are only looking for a deceleration to happen
                    if old_speed >= settings.min_decel_trigger_speed_mph: # only consider decelerations from above this MPH

                        # only continue if deceleration is greater than than a certain amount
                        if accel_mphs <= (settings.min_decel_trigger * -1): # if we are losing more than this many MPH per second, we are NOW DECELERTING!

                            # clear the speed log
                            self.__fixed_speed_buff__.clear()

                            # log the old speed (that is our starting point)
                            fs = fixed_speed()
                            fs.fixed = old_fixed
                            fs.speed = old_speed
                            self.add_fixed_speed(fs)
                            
                            # mark the status as decelerating
                            self.__mode__ = Decelerating

            
            # if we are currently decelerating, calculate the hz of the strobe and return it
            if self.__mode__ == Decelerating:

                # log the current speed
                fs = fixed_speed()
                fs.fixed = fixed
                fs.speed = speed_mph
                self.add_fixed_speed(fs)

                # Get a percentage that we will use to calcualte the hz of the strobe
                average_acceleration = self.avg_accel()
                decel_percent = (abs(average_acceleration) - settings.min_decel_trigger) / (settings.max_decel_strobe - settings.min_decel_strobe)
                decel_percent = min(decel_percent, 1.0) #make sure it doesn't exceed 100%
                decel_percent = max(decel_percent, 0) #make sure it doesn't fall below 0%
                hz = strobe_tools.select_hertz(decel_percent) # CALCULATING THE VALUE TO RETURN
                return hz

