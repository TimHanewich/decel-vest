import settings
import strobe_controller
import _thread

strobe_controller.set_mode(strobe_controller.mode_pit)
_thread.start_new_thread(strobe_controller.continuous_strobe, ())
print("Started!")
