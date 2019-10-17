import board
import neopixel
import time
from digitalio import DigitalInOut, Direction
from gpiozero import PWMOutputDevice
from tkinter import *
from PIL import ImageTk, Image

# Setup pins
pad_pin = board.D20
pad = DigitalInOut(pad_pin)
pixels = neopixel.NeoPixel(board.D21,30)
pad.direction = Direction.INPUT
# Status of device
device_on = False
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
motors = [r_1, r_2, r_3, r_4, r_5, l_1, l_2, l_3, l_4, l_5]
# Turn off Neopixels on restart
pixels.fill((0,0,0))
pixels.show()

while True:
        # 1. Load model
        # TODO: load model when script started
        # 2. User wears headphones with white sound or noise-cancelling
        # 3. User sits down
        # 4. User wears gloves and connects them to the box
        # 5. Organizer clicks on pad
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
                # Show red light for Neopixels to indicate recording
                pixels.fill((255,0,0))
                pixels.show()
                # Start sound demo
                # 
                root = Tk()                
                # canvas for image
                canvas = Canvas(root, width=1850, height=890, bg = 'black')
                canvas.grid(row=0, column=0)
                
                # images
                my_images = []
                original = Image.open("owl.jpg")
                img = ImageTk.PhotoImage(original)
                my_images.append(img)
                original_1 = Image.open("con.jpg")
                img_1 = ImageTk.PhotoImage(original_1)
                my_images.append(img_1)
                original_2 = Image.open("touch.jpg")
                original_2 = original_2.resize((1450,890))
                img_2 = ImageTk.PhotoImage(original_2)
                my_images.append(img_2)
                my_image_number = 0

                # set first image on canvas
                #image_on_canvas = canvas.create_image(0, 0, anchor = NW, image = my_images[my_image_number])
                image_on_canvas = canvas.create_image(0, 0, anchor = NW, image = img_1)
                
                root.update_idletasks()
                root.update()
                 # Sleep to avoid conflicts
                time.sleep(1)                
        elif pad.value and device_on:
                print("Turn off")
                # destroy and cannot init canvas again, change image but cannot find reference
                #canvas.destroy()
                #canvas.itemconfig(image_on_canvas, image = img_2) 
                for m in motors:
                        m.value = 0.0
                device_on = False
                pixels.fill((0,0,0))
                pixels.show()
                # Sleep to avoid conflicts
                time.sleep(1)