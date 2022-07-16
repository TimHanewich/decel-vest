import machine
import settings
import time
import strobe_tools
import dlogging

# VARIABLES
wait_time = 1 #this sets the wait time in between each flash
muted = False

def continuous_strobe():
    global wait_time

    strobe_output = machine.Pin(settings.gpio_strobe, machine.Pin.OUT)

    while True:
        if muted == False:
            strobe_output.toggle()
            time.sleep(wait_time)
        else:
            strobe_output.value(0)
            time.sleep(0.1)


def set_hertz(hz:float):
    global wait_time
    wait_time = strobe_tools.hertz_to_seconds(hz)

def mute():
    try:
        print("Making variable global")
        global muted
        print("Turning muted to true")
        muted = True
        print("Success!")
    except Exception as e:
        print("Failure while muting: " + str(e))

def unmute():
    global muted
    muted = False