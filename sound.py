#from subprocess import call
#cmd = ["aplay", "wood_thrush.wav"]
#call(cmd)
import os
import board
import glob
import threading, time
from gpiozero import PWMOutputDevice

# filename = "barred_owl"
# #print(os.listdir("/home/pi/Desktop/NiB/NiB/wav"))
# list = []
# j = 0

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
motors = [r_1, r_2, r_3, r_4, r_5, l_1, l_2, l_3, l_4, l_5]

def stringNumber(elem):
    e = elem.split('/home/pi/Desktop/NiB/NiB/wav/'+filename+'_')[1].split('.wav')[0]
    return int(e)

def predict():
    global j
    print('Infering from ', list[j])
    j += 1
    if (j > len(list)-1):
        return
    threading.Timer(0.5, predict).start()

#for name in glob.glob('/home/pi/Desktop/NiB/NiB/wav/'+filename+ '_*'):
#        list.append(name)
        
#list.sort(key = stringNumber)
#predict()
while True:
    motors[0].value = 1
    motors[1].value = 1
    motors[2].value = 1
    motors[3].value = 1
    motors[4].value = 1
    
