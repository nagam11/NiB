# Import data
import glob
import os

import numpy as np
from scipy.io.wavfile import read

from config import SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW, DURATION
from loader import Loader
from util import transform_audio, plot_results

path = "./wav_x"
audios = [os.path.abspath(file) for file in glob.glob(f"{path}/*.wav")]

datapoints = []

for audio in audios:
    sr, a = read(audio)
    a = np.array(a, dtype=float)
    if a.shape[0] != DURATION:
        a = np.pad(a, (0, DURATION - a.shape[0]), 'constant')
    datapoints.append(transform_audio(a, SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW))

dataset = datapoints
dataset = np.array(dataset)

print(f"Dataset size: {dataset.shape}")

dataset = dataset.reshape((len(dataset), np.prod(dataset.shape[1:])))

loader = Loader(path="./saved_models/crazy_bird_5000.h5")

loader.get_encoder().save('./saved_models/crazy_bird_encoder_5000.h5')

encoded_dataset = loader.encode(dataset)

maxes = np.max(encoded_dataset, axis=0)
print(f"Maximum values: {maxes}")
print(f"Minimum value: {np.min(encoded_dataset, axis=0)}")
print(f"Mean: {encoded_dataset.mean(axis=0)}")
print(f"Std: {encoded_dataset.std(axis=0)}")
print(encoded_dataset)
norm = encoded_dataset / maxes
print(f"Maximum values: {np.max(norm, axis=0)}")
print(f"Minimum value: {np.min(norm, axis=0)}")
print(f"Mean: {norm.mean(axis=0)}")
print(f"Std: {norm.std(axis=0)}")
print(norm)


decoded_audio = loader.predict(dataset)
plot_results(test=dataset, decoded=decoded_audio, n=12)

