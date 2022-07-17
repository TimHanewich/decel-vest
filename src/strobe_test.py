import strobe_controller
import settings
import _thread
import time

# fire the strobe controller
strobe_controller.mute()
_thread.start_new_thread(strobe_controller.continuous_strobe, ())

# cycle through
print("Going to cycle up...")
hz = settings.min_hz
strobe_controller.unmute()
while hz < settings.max_hz:
    print(hz)
    strobe_controller.set_hertz(hz)
    hz = hz + 1
    time.sleep(2)

# wait 5 seconds
print("Waiting 5 seconds...")
time.sleep(5)

# mute for a second
print("Muting for 2 seconds...")
strobe_controller.mute()
time.sleep(2)

# cycle down
print("Going to cycle down...")
strobe_controller.unmute()
while hz > settings.max_hz:
    print(hz)
    strobe_controller.set_hertz(hz)
    hz = hz - 1
    time.sleep(1)

# wait 5 seconds
print("Waiting 5 seconds...")
time.sleep(5)

# mute
print("Muting...")
strobe_controller.mute()
print("Bye bye!")


