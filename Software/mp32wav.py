import subprocess
import glob
import os

mypath = "./sounds"

audios = [os.path.abspath(file) for file in glob.glob(f"{mypath}/*.mp3")]

for audio in audios:
	print(f"Recieved file: {audio}")
	wav = audio.replace(".mp3", ".wav")
	print(f"Converting to wave: {wav}")
	command = f"sox -b 16 {audio} {wav} remix 1 rate 16000"
	print(command)
	subprocess.call(command, shell=True)