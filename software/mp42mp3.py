import subprocess
import glob
import os

mypath = "./sounds"

files = [os.path.abspath(file) for file in glob.glob(f"{mypath}/*.mp4")]

for file in files:
	print(f"Recieved file: {file}")
	mp3_file = file.replace(".mp4", ".mp3")
	print(f"Converting to wave: {mp3_file}")
	command = f"ffmpeg -y -i {file} {mp3_file}"
	print(command)
	subprocess.call(command, shell=True)