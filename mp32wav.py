import subprocess
import glob
import os

mypath = "./mp3"

audios = [os.path.abspath(file) for file in glob.glob(f"{mypath}/*.mp3")]

for audio in audios:
	print(f"Recieved file: {audio}")
	process = subprocess.check_output(f"soxi -D {audio}", shell=True)
	seconds = int(float(process.decode('UTF-8').rstrip()))
	wav = audio.replace(".mp3", ".wav")
	wav = audio.replace("mp3", f"full_wav_x")
	print(f"Converting to wave: {wav}")
	command = f"sox -b 16 {audio} {wav} remix 1 rate 16000"
	print(command)
	subprocess.call(command, shell=True)

	for i in range(0, seconds * 2):
		wav = audio.replace(".mp3", f"_{i}.wav")
		wav = wav.replace("mp3", f"wav_x")
		print(f"Converting to wave: {wav}")
		command = f"sox -b 16 {audio} {wav} trim {i / 2} 0.5 remix 1 rate 16000"
		print(command)
		subprocess.call(command, shell=True)