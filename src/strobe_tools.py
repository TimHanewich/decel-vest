
# Settings
max_hz = 20.0
min_hz = 2.0

# percentage supplied between 0.0 and 1.0
def select_hertz(percentage:float) -> float:
    if percentage < 0.0:
        return min_hz
    elif percentage > 1.0:
        return max_hz

    to_add = (max_hz - min_hz) * percentage
    to_return = min_hz + to_add
    return to_return

# calculates the number of seconds in between each pulse
def hertz_to_seconds(hertz:float) -> float:
    val = 1 / hertz
    return val

d = hertz_to_seconds(0.5)
print(d)