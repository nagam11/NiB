from tkinter import *
from PIL import ImageTk, Image
import board
import neopixel
import time
from digitalio import DigitalInOut, Direction
from gpiozero import PWMOutputDevice

class MainWindow():
    def __init__(self, main):
        # Setup pins
        pad_pin = board.D20
        pad = DigitalInOut(pad_pin)
        pixels = neopixel.NeoPixel(board.D21,30)
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

        # canvas for image
        self.canvas = Canvas(main, width=1850, height=890, bg = 'black')
        self.canvas.grid(row=0, column=0)

        # images
        self.my_images = []
        original = Image.open("owl.jpg")
        img = ImageTk.PhotoImage(original)
        self.my_images.append(img)
        original_1 = Image.open("con.jpg")
        img_1 = ImageTk.PhotoImage(original_1)
        self.my_images.append(img_1)
        original_2 = Image.open("touch.jpg")
        original_2 = original_2.resize((1450,890))
        img_2 = ImageTk.PhotoImage(original_2)
        self.my_images.append(img_2)
        self.my_image_number = 0

        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor = NW, image = self.my_images[self.my_image_number])

        # button to change image
        self.button = Button(main, text="Change", command=self.onButton)
        self.button.grid(row=1, column=0)

    #----------------

    def onButton(self):

        # next image
        self.my_image_number += 1

        # return to first image
        if self.my_image_number == len(self.my_images):
            self.my_image_number = 0

        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.my_images[self.my_image_number])

#----------------------------------------------------------------------

root = Tk()
MainWindow(root)
root.mainloop()
