import board
import neopixel
import time
from digitalio import DigitalInOut, Direction
from gpiozero import PWMOutputDevice

# Setup pins
pad_pin = board.D23
pad = DigitalInOut(pad_pin)
pixels = neopixel.NeoPixel(board.D24,30)
pad.direction = Direction.INPUT
# Motor vibration via PWM.
# Mapping: r_1 => right glove, first finger is thumb l_1 => left hand, first finger is small finger
r_1 = PWMOutputDevice(14)
r_2 = PWMOutputDevice(15)
r_3 = PWMOutputDevice(18)
r_4 = PWMOutputDevice(2)
r_5 = PWMOutputDevice(3)
l_1 = PWMOutputDevice(4)
l_2 = PWMOutputDevice(17)
l_3 = PWMOutputDevice(27)
l_4 = PWMOutputDevice(22)
l_5 = PWMOutputDevice(10)
# Status of device
device_on = False
# Turn off Neopixels on restart
pixels.fill((0,0,0))
pixels.show()
motors = [r_1, r_2, r_3, r_4, r_5, l_1, l_2, l_3, l_4, l_5]

while True:
        if pad.value and not device_on:
                print("Turn on")
                # Short double vibration to indicate turning on the device
                for m in motors:
                        m.value = 1
                time.sleep(0.3)
                for m in motors:
                        m.value = 0.0
                time.sleep(0.3)
                for m in motors:
                        m.value = 1
                time.sleep(0.3)
                for m in motors:
                        m.value = 0.0
                device_on = True
                pixels.fill((255,0,0))
                pixels.show()
                # Sleep to avoid conflicts
                time.sleep(1)
        elif pad.value and device_on:
                print("Turn off")
                for m in motors:
                        m.value = 0.0
                device_on = False
                pixels.fill((0,0,0))
                pixels.show()
                # Sleep to avoid conflicts
                time.sleep(1)
