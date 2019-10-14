import board
import neopixel
import time
from digitalio import DigitalInOut, Direction

# Setup pins
pad_pin = board.D23
pad = DigitalInOut(pad_pin)
pixels = neopixel.NeoPixel(board.D18,30)
pad.direction = Direction.INPUT
# Status of device
device_on = False
# Turn off Neopixels on restart
pixels.fill((0,0,0))
pixels.show()

while True:
        if pad.value and not device_on:
                print("Turn on")
                device_on = pad.value
                pixels.fill((255,0,0))
                pixels.show()
                time.sleep(1)
        elif pad.value and device_on:
                print("Turn off")
                device_on = False
                pixels.fill((0,0,0))
                pixels.show()
                time.sleep(1)
