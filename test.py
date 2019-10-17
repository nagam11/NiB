# Import data
import glob
import os

import numpy as np
from scipy.io.wavfile import read
from sklearn.model_selection import train_test_split

from config import SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW, DURATION
from loader import Loader
from util import transform_audio

path = "./wav"
audios = [os.path.abspath(file) for file in glob.glob(f"{path}/*.wav")]

datapoints = []

for audio in audios:
    sr, a = read(audio)
    a = np.array(a, dtype=float)
    if a.shape[0] == DURATION:
        datapoints.append(transform_audio(a, SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW))

# x_train, x_test = datapoints[:-20], datapoints[-20:]
dataset = datapoints
dataset = np.array(dataset)

print(f"Dataset size: {dataset.shape}")

dataset = dataset.reshape((len(dataset), np.prod(dataset.shape[1:])))

loader = Loader(path="./saved_models/crazy_bird.h5")

encoded_dataset = loader.encode(dataset)

print(f"Maximum value: {np.max(encoded_dataset)}")
print(f"Minimum value: {np.min(encoded_dataset)}")
