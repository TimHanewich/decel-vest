import strobe_calculator
import time
import _thread
import strobe_controller
from machine import Pin

# Turn on the LED
print("LED on!")
led = Pin(25, Pin.OUT)
led.value(1)

sc = strobe_calculator.strobe_calculator()
_thread.start_new_thread(strobe_controller.continuous_strobe, ())
strobe_controller.mute()

print("Opening file...")
f = open(r"/example-data.csv", "r")

while True:
    print("Reading line...")
    line = f.readline()

    if not line:
        break

    if "fix" not in line:
        print("I got a good line!")
        

        row = line.split(",")
        fix = int(row[0])
        speed = float(row[1])
        lat = float(row[2])
        lon = float(row[3])
        sats = float(row[4])

        print("All converted!")

        print("Now on: " + str(fix))
        
        hz = sc.ingest(fix, speed)
        if hz != None:
            strobe_controller.set_hertz(hz)
            strobe_controller.unmute()
        else:
            strobe_controller.mute()

        print("Sleeping...")
        time.sleep(1)