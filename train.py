import glob

import tensorflow as tf
from tensorflow.python.client import device_lib
print(f"Available: {[x.name for x in device_lib.list_local_devices()]}")

import numpy as np
import os

from scipy.io.wavfile import read
from sklearn.model_selection import train_test_split

from util import transform_audio, plot_results
from config import DURATION, SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW

lr = 0.001

# Import data
path = "./wav_x"
audios = [os.path.abspath(file) for file in glob.glob(f"{path}/*.wav")]

datapoints = []

for audio in audios:
    sr, a = read(audio)
    a = np.array(a, dtype=float)
    if a.shape[0] != DURATION:
        a = np.pad(a, (0, DURATION - a.shape[0]), 'constant')
    datapoints.append(transform_audio(a, SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW))

# x_train, x_test = datapoints[:-20], datapoints[-20:]
print(f"Dataset size: {len(datapoints)} samples")
x_train, x_test = train_test_split(datapoints, test_size=0.1, random_state=42)
x_train = np.array(x_train)
x_test = np.array(x_test)

print(f"Training size: {x_train.shape}")
print(f"Val size: {x_test.shape}")

x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
original_dim = x_train.shape[1]

# this is the siez of our encoded representations
ENCODING_DIM = 5

input = tf.keras.layers.Input(shape=(original_dim,))
encoded = tf.keras.layers.Dense(ENCODING_DIM*100, activation='relu')(input)
encoded2 = tf.keras.layers.Dense(ENCODING_DIM*10, activation='relu')(encoded)
encoded3 = tf.keras.layers.Dense(ENCODING_DIM*5, activation='relu')(encoded2)
encoded4 = tf.keras.layers.Dense(ENCODING_DIM, activation='relu', activity_regularizer=tf.keras.regularizers.l1(10e-5), name='encoder')(encoded3)
decoded3 = tf.keras.layers.Dense(ENCODING_DIM*5, activation='relu')(encoded4)
decoded2 = tf.keras.layers.Dense(ENCODING_DIM*10, activation='relu')(decoded3)
decoded = tf.keras.layers.Dense(ENCODING_DIM*100, activation='relu')(decoded2)
output = tf.keras.layers.Dense(original_dim, activation='linear')(decoded)

autoencoder = tf.keras.models.Model(input, output)
print(autoencoder.summary())
optimizer = tf.keras.optimizers.Adam(lr=lr)
autoencoder.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['accuracy'])
encoder = tf.keras.models.Model(inputs=autoencoder.input, outputs=autoencoder.get_layer('encoder').output)

# with added regularization, the model is less likely to overfit and can be trained
# longer. The model ends with a train loss of 0.11 and test loss of 0.10. The difference is mostly due to
# the regularization term being added to the loss during training
autoencoder.fit(x_train, x_train, epochs=5000, batch_size=64, shuffle=True, validation_data=(x_test, x_test))

encoded_audio = encoder.predict(x_test)
print(encoded_audio)
decoded_audio = autoencoder.predict(x_train)

plot_results(test=x_train, decoded=decoded_audio, n=12)

autoencoder.save('./saved_models/crazy_bird_max.h5')
