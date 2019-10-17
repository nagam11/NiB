import glob
import os

import numpy as np
from autoencoder import Autoencoder
from scipy.io.wavfile import read
from sklearn.model_selection import train_test_split

from util import transform_audio
from config import DURATION, SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW

# Import data
path = "./wav"
audios = [os.path.abspath(file) for file in glob.glob(f"{path}/*.wav")]


datapoints = []

for audio in audios:
    sr, a = read(audio)
    a = np.array(a, dtype=float)
    if a.shape[0] == DURATION:
        datapoints.append(transform_audio(a, SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW))

x_train, x_test = train_test_split(datapoints, test_size=0.05, random_state=42)
x_train = np.array(x_train)
x_test = np.array(x_test)
print(f"Training size: {x_train.shape}")
print(f"Val size: {x_test.shape}")

# Prepare input
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

# Tensorflow implementation
autoencodertf = Autoencoder(x_train.shape[1], 5)
autoencodertf.train(x_train, x_test, 16, 1000)
encoded_img = autoencodertf.getEncoded(x_test[1])
decoded_img = autoencodertf.getDecoded(x_test[1])

# Tensorflow implementation results
print(x_test[1])
print(decoded_img)
