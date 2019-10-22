import board
import neopixel
import time
from digitalio import DigitalInOut, Direction
from gpiozero import PWMOutputDevice
from tkinter import *
from PIL import ImageTk, Image
import os, sys,random
import logging
import threading
import glob
import time
from util import load2spectrogram
from tfloader import TFLiteLoader
import numpy as np

# Setup pins
pad_pin = board.D20
pad = DigitalInOut(pad_pin)
pixels = neopixel.NeoPixel(board.D21,30)
pad.direction = Direction.INPUT
# Status of device
device_on = False
testing_mode = False
# Motor vibration via PWM.
# Mapping: r_1 => right glove, first finger is thumb l_1 => left hand, first finger is small finger
r_1 = PWMOutputDevice(14)
r_2 = PWMOutputDevice(15)
r_3 = PWMOutputDevice(18)
r_4 = PWMOutputDevice(2)
r_5 = PWMOutputDevice(3)
l_1 = PWMOutputDevice(10)
l_2 = PWMOutputDevice(22)
l_3 = PWMOutputDevice(27)
l_4 = PWMOutputDevice(17)
l_5 = PWMOutputDevice(4)
# l_1 = PWMOutputDevice(4)
# l_2 = PWMOutputDevice(17)
# l_3 = PWMOutputDevice(27)
# l_4 = PWMOutputDevice(22)
# l_5 = PWMOutputDevice(10)
motors = [r_1, r_2, r_3, r_4, r_5, l_1, l_2, l_3, l_4, l_5]
# Turn off Neopixels on restart
pixels.fill((0,0,0))
pixels.show()
# Variable used to loop through the list of sound subfiles for prediction
j = 0

# Loading TF Lite model
loader = TFLiteLoader(path="./saved_models/crazy_bird_encoder_max.tflite")
# Maxima for each latent dimension
MX_VAL = np.array([25.497225, 37.466076, 17.507608, 37.70733, 32.484062])

# This method plays a sound to the speakers
def play_on_speaker(file):
    os.system("aplay /home/pi/Desktop/NiB/NiB/full_wav/"+ file)

# This method return an Int key used for sorting subfiles
def stringNumber(elem):
    key = elem.split('/home/pi/Desktop/NiB/NiB/wav/'+filename+'_')[1].split('.wav')[0]
    return int(key)

# This method finishes up the demo.
def finishDemo(image_on_canvas, canvas):
    print("Finishing demo")
    black_screen =  Image.open("thanks.jpg")
    img = ImageTk.PhotoImage(black_screen)              
    image_on_canvas = canvas.itemconfig(image_on_canvas,image = img)
                
    for m in motors:
        m.value = 0.0
    # Sleep to avoid conflicts
    time.sleep(1)

# This method feeds the subfiles to the model
def predict(dataset):
    global j
    print('Infering from', list[j])
    i = 0
    motor_values = []
    if testing_mode:
        motor_values = [random.uniform(0.6, 1) for i in range(0, 5)]
    else:
        print('predicting')
        motor_values = loader.predict(dataset[[j], :]) / MX_VAL
        motor_values = np.clip(motor_values * 2, 0, 1)
        #motor_values = loader.predict(dataset[[j], :]) / 22.85 
        print(motor_values)
        for i in range(len(motor_values[0])):
            motors[i].value = motor_values[0][i]
            motors[i+5].value = motor_values[0][i]
        
    j += 1
    t = threading.Timer(0.5, predict, args = (dataset,))
    t.start()
    if (j > len(list)-1):
        t.cancel()
        sys.exit()
    
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
                # show black entry screen
                root = Tk()                
                # canvas for image
                canvas = Canvas(root, width=1850, height=890, bg = 'black')
                canvas.grid(row=0, column=0)
                black_screen =   Image.open("black.jpg")
                img = ImageTk.PhotoImage(black_screen)              
                image_on_canvas = canvas.create_image(0, 0, anchor = NW, image = img)                
                # Start demo
                # 1. Randomly select one file from full_wav
                bird_full_wav = random.choice(os.listdir("/home/pi/Desktop/NiB/NiB/full_wav"))
                print('Selected bird:',bird_full_wav)
                filename_w_ext = os.path.basename("/home/pi/Desktop/NiB/NiB/full_wav/"+bird_full_wav)
                filename, file_extension = os.path.splitext(filename_w_ext)
                print(filename)
                # 2. Play it to speakers using a separate thread
                speaker_thread = threading.Thread(target = play_on_speaker, args = (bird_full_wav,))
                speaker_thread.start()
                # 3. Projector shows bird based on filename
                bird_image = Image.open("/home/pi/Desktop/NiB/NiB/Images/"+filename+".jpg")
                img = ImageTk.PhotoImage(bird_image)
                image_on_canvas = canvas.itemconfig(image_on_canvas,image = img)
                # 4. Get all sub-files from this file /wav/
                list = []
                for name in glob.glob('/home/pi/Desktop/NiB/NiB/wav/'+filename+ '_*'):
                    list.append(name)
                # Sort files by ascending number in name
                list.sort(key = stringNumber)
                dataset = []
                for l in list:
                    dataset.append(load2spectrogram(l))
                dataset = np.array(dataset)
                    
                # 5. Feed these files every 0.5 sec with timer to predictor
                predict(dataset)
                #print("Continue")
                finishDemo(image_on_canvas, canvas)
                root.update_idletasks()
                root.update()
                 # Sleep to avoid conflicts
                time.sleep(1)                
        elif pad.value and device_on:
                print("Turn off")
                # destroy and cannot init canvas again, change image but cannot find reference
                #canvas.destroy()
                black_screen =   Image.open("black.jpg")
                img = ImageTk.PhotoImage(black_screen)              
                image_on_canvas = canvas.itemconfig(image_on_canvas,image = img)
                
                for m in motors:
                        m.value = 0.0
                device_on = False
                pixels.fill((0,0,0))
                pixels.show()
                # Sleep to avoid conflicts
                time.sleep(1)