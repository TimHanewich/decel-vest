# Strobe settings
gpio_strobe = 1
max_hz = 15
min_hz = 1

# Deceleration Settings - in MPH/S. For example, 1 would mean losing 1 MPH per second (decelerating)
min_decel = 1.0 # the minimum deceleration that has to occur for it to be registered as a deceleration and thus trigger a blink
max_decel = 3.0 # the maximum deceleration we would expect to see. Used to calculate the hz of the light (our maximum)