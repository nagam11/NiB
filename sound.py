#from subprocess import call
#cmd = ["aplay", "wood_thrush.wav"]
#call(cmd)
import os
import glob
import threading, time

filename = "barred_owl"
#print(os.listdir("/home/pi/Desktop/NiB/NiB/wav"))
list = []
j = 0

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

for name in glob.glob('/home/pi/Desktop/NiB/NiB/wav/'+filename+ '_*'):
        list.append(name)
        
list.sort(key = stringNumber)
predict()