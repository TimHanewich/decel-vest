import machine
import settings
import time
import strobe_tools

# VARIABLES
wait_time = 0.25 #this sets the wait time in between each flash

def continuous_strobe():
    global wait_time

    strobe_output = machine.Pin(settings.gpio_strobe, machine.Pin.OUT)

    while True:
        strobe_output.value(1)
        time.sleep(wait_time)
        strobe_output.value(0)
        time.sleep(wait_time)


def set_hertz(hz:float):
    global wait_time
    wait_time = strobe_tools.hertz_to_seconds(hz)