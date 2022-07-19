import machine
import settings

led = machine.Pin(settings.gpio_strobe1, machine.Pin.OUT)
led.value(1)