import settings

# percentage supplied between 0.0 and 1.0
def select_hertz(percentage:float) -> float:
    if percentage < 0.0:
        return settings.min_hz
    elif percentage > 1.0:
        return settings.max_hz

    to_add = (settings.max_hz - settings.min_hz) * percentage
    to_return = settings.min_hz + to_add
    return to_return

# calculates the number of seconds in between each pulse
def hertz_to_seconds(hertz:float) -> float:
    val = 1 / hertz
    return val

d = hertz_to_seconds(0.5)
print(d)