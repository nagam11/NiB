import glob
import os

import numpy as np
from tensorflow.keras.datasets import fashion_mnist
from autoencoder import Autoencoder
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

# Import data
path = "/Users/wagram/NiB/software/wav"
audios = [os.path.abspath(file) for file in glob.glob(f"{path}/*.wav")]

DURATION = 8000

datapoints = []

for audio in audios:
    a = read(audio)
    a = np.array(a[1], dtype=float)
    if a.shape[0] == DURATION:
        datapoints.append(a)

x_train, x_test = datapoints[:-200], datapoints[-200:]
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
autoencodertf = Autoencoder(x_train.shape[1], 10)
autoencodertf.train(x_train, x_test, 5, 500)
encoded_img = autoencodertf.getEncodedImage(x_test[1])
decoded_img = autoencodertf.getDecodedImage(x_test[1])

# Tensorflow implementation results
print(x_test[1])
print(decoded_img)