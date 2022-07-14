import csv
import strobe_calculator
import time
import _thread
import strobe_controller
from machine import Pin

# Turn on the LED
led = Pin(25, Pin.OUT)
led.value(1)

sc = strobe_calculator.strobe_calculator()
_thread.start_new_thread(strobe_controller.continuous_strobe, ())

f = open(r"/pyboard/example-data.csv", "r")

reader = csv.reader(f, delimiter=",")
for row in reader:
    if reader.line_num > 1:
        fix = int(row[0])
        speed = float(row[1])
        lat = float(row[2])
        lon = float(row[3])
        sats = float(row[4])
        
        hz = sc.ingest(fix, speed)
        if hz != None:
            strobe_controller.set_hertz(hz)
            strobe_controller.unmute()
        else:
            strobe_controller.mute()

        time.sleep(1)