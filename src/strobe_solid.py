import machine
import settings

led = machine.Pin(settings.gpio_strobe)
led.value(1)