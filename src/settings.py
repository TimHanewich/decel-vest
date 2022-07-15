# Strobe settings
gpio_strobe = 1
max_hz = 15
min_hz = 1

# Deceleration Settings - in MPH/S. For example, 1 would mean losing 1 MPH per second (decelerating)
min_decel_trigger = 1.0 # the minimum deceleration that has to occur for it to be registered as a deceleration and thus enter in decelerating mode
min_decel_sustained = 0.3 #when deceleration is first detected, this is the minimum deceleration that has to be sustained in order for deceleration to be sustained. The moment deceleration drops below this, we move to the "awaiting deceleration" mode.

# Deceleration settings for calculating hz - these are used to calcualte where we are in the range and thus calculate a hz for the strobe
min_decel_strobe = 0.3
max_decel_strobe = 3.0
