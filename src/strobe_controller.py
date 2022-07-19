import machine
import settings
import time
import strobe_tools
import dlogging

# strobe modes
mode_hz = 0 # we are in the mode where we are prepared for deceleration. So we will show the hz when unmuted and shut up when muted
mode_pit = 1 # we are in pit mode, so strobe #1 and #2 will constantly alternate

# VARIABLES
STROBE_MODE = mode_hz
wait_time = 1 #this sets the wait time in between each flash
muted = False

def continuous_strobe():

    global wait_time

    global STROBE_MODE
    global mode_hz
    global mode_pit

    strobe1 = machine.Pin(settings.gpio_strobe1, machine.Pin.OUT)
    strobe2 = machine.Pin(settings.gpio_strobe2, machine.Pin.OUT)

    while True:
        if STROBE_MODE == mode_hz:
            if muted == False:
                strobe1.toggle()
                strobe2.toggle()
                time.sleep(wait_time)
            else:
                strobe1.value(0)
                strobe2.value(0)
                time.sleep(0.1)
        elif STROBE_MODE == mode_pit:
            while STROBE_MODE == mode_pit:

                #First pattern
                strobe1.value(1)
                strobe2.value(0)
                time.sleep(1)

                #second pattern
                strobe1.value(0)
                strobe2.value(1)
                time.sleep(1)
            
            # turn both off so they are both on the same value
            strobe1.value(0)
            strobe2.value(0)


def set_hertz(hz:float):
    global wait_time
    wait_time = strobe_tools.hertz_to_seconds(hz)

def mute():
    try:
        #print("Making variable global")
        global muted
        #print("Turning muted to true")
        muted = True
        #print("Success!")
    except Exception as e:
        pass
        #print("Failure while muting: " + str(e))

def unmute():
    global muted
    muted = False