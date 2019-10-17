import glob

import tensorflow as tf
import numpy as np
import os

from scipy.io.wavfile import read
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from util import transform_audio, sampling, plot_results
from config import DURATION, SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW

lr = 0.001

# Import data
path = "./wav"
audios = [os.path.abspath(file) for file in glob.glob(f"{path}/*.wav")]

datapoints = []

for audio in audios:
    sr, a = read(audio)
    a = np.array(a, dtype=float)
    if a.shape[0] == DURATION:
        datapoints.append(transform_audio(a, SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW))

# x_train, x_test = datapoints[:-20], datapoints[-20:]
x_train, x_test = train_test_split(datapoints, test_size=0.05, random_state=42)
x_train = np.array(x_train)
x_test = np.array(x_test)

print(f"Training size: {x_train.shape}")
print(f"Val size: {x_test.shape}")

x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
original_dim = x_train.shape[1]

# we will start simple with a single fully-connected neural layer as encoder and decoder
# this is the siez of our encoded representations
ENCODING_DIM = 5

input = tf.keras.layers.Input(shape=(original_dim,))
encoded = tf.keras.layers.Dense(ENCODING_DIM*100, activation='sigmoid')(input)
encoded2 = tf.keras.layers.Dense(ENCODING_DIM*10, activation='sigmoid')(encoded)
encoded3 = tf.keras.layers.Dense(ENCODING_DIM, activation='sigmoid')(encoded2)

decoded3 = tf.keras.layers.Dense(ENCODING_DIM*10, activation='sigmoid')(encoded3)
decoded2 = tf.keras.layers.Dense(ENCODING_DIM*100, activation='sigmoid')(decoded3)
decoded = tf.keras.layers.Dense(original_dim, activation='linear')(decoded2)

autoencoder = tf.keras.models.Model(input, decoded)
optimizer = tf.keras.optimizers.Adam(lr)
autoencoder.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['accuracy'])


# now let's train this for 100 epochs (with added regularization, the model is less likely to overfit and can be trained
# longer). The model ends with a train loss of 0.11 and test loss of 0.10. The difference is mostly due to
# the regularization term being added to the loss during training
autoencoder.fit(x_train, x_train, epochs=5, batch_size=16, shuffle=True, validation_data=(x_test, x_test))

# after 50 epochs the autoencoder seems to reach a stable train/test loss value of about 0.11. We can try to visualize
# the reconstructed inputs and the encoded representations. We will be using Matplotlib
# encode and decode some digits
# note that we take them from the "test" set
#encoded_audio = encoded3.predict(x_test)
decoded_audio = autoencoder.predict(x_test)

# now using Matplotlib to plot the images
n = 10  # how many images we will display
plt.figure(figsize=(20, 4))
for i in range(n):
    # display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(161, 51))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_audio[i].reshape(161, 51))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

plt.show()