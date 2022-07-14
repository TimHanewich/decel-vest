from enum import IntEnum
import nmea
import strobe_tools
import settings


class InternalMode(IntEnum):
    AwaitingDeceleration = 0, # nothing is happening right now
    Decelerating = 1


class strobe_calculator:

    # variables for tracking
    __last_speed_mph__ = None #the speed that was most recently received
    __last_fixed__ = None #the last fixed time that the speed was received at
    __mode__ = InternalMode.AwaitingDeceleration

    # outputs a recommended hertz
    def ingest(self, fixed:int, speed_mph:float) -> float:

        # if we have old data
        if self.__last_speed_mph__ != None and self.__last_fixed__ != None:

            # calculate acceleration/deceleration - acceleration would be positie, deceleration would be negative
            accel_mphs = (speed_mph - self.__last_speed_mph__) / (fixed - self.__last_fixed__)


            if self.__mode__ == InternalMode.AwaitingDeceleration: #we are waiting for something to happen
                if speed_mph < self.__last_speed_mph__: # we are only looking for a deceleration to happen
                    if self.__last_speed_mph__ > 30: # only consider decelerations from above this MPH

                        # only continue if deceleration is greater than than a certain amount
                        if accel_mphs <= (settings.min_decel * -1): # if we are losing more than this many MPH per second 
                            
                            # turn it into a percentage that we will use to calculate the hz of the strobe
                            decel_percent = (abs(accel_mphs) - settings.min_decel) / (settings.max_decel - settings.min_decel)
                            decel_percent = min(decel_percent, 1.0) #make sure it doesn't exceed 100%
                            decel_percent = max(decel_percent, 0) #make sure it doesn't fall below 0%
                            hz = strobe_tools.select_hertz(decel_percent) # CALCULATING THE VALUE TO RETURN

                            # mark the status as decelerating
                            self.__mode__ = InternalMode.Decelerating

                            # RETURN!
                            return hz

            elif self.__mode__ == InternalMode.Decelerating: # we are currently decelerating
                if accel_mphs > (settings.min_decel * -1): # if we are no longer decelerating in the window

                    # mark the status as awaiting deceleration (neutral)
                    self.__mode__ = InternalMode.AwaitingDeceleration

                    # Return None, indicating that there isn't a deceleration going on
                    return None




        # set
        self.__last_speed_mph__ = speed_mph
        self.__last_fixed__ = fixed
