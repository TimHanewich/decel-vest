import machine
import settings

led = machine.Pin(settings.gpio_strobe, machine.Pin.OUT)
led.value(1)