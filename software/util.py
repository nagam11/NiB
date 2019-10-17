import os

import librosa
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


def transform_audio(sound: np.ndarray, sample_rate, window_size, window_stride, window):
    n_fft = int(sample_rate * window_size)
    win_length = n_fft
    hop_length = int(sample_rate * window_stride)
    D = librosa.stft(sound, n_fft=n_fft, hop_length=hop_length,
                     win_length=win_length, window=window)
    spectrogram, phase = librosa.magphase(D)

    spectrogram = np.log1p(spectrogram)
    mean = spectrogram.mean()
    std = spectrogram.std()
    spectrogram = spectrogram - mean
    spectrogram = spectrogram / std

    return spectrogram


def sampling(args):
    z_mean, z_log_var = args
    batch = tf.keras.backend.shape(z_mean)[0]
    dim = tf.keras.backend.int_shape(z_mean)[1]
    # by default, random_normal has mean=0 and std=1.0
    epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
    return z_mean + tf.keras.backend.exp(0.5 * z_log_var) * epsilon


def plot_results(models, data, batch_size=128, model_name="vae"):
    """Plots labels and MNIST digits as function of 2-dim latent vector
    # Arguments:
        models (tuple): encoder and decoder models
        data (tuple): test data and label
        batch_size (int): prediction batch size
        model_name (string): which model is using this function
    """

    encoder, decoder = models
    x_test = data
    os.makedirs(model_name, exist_ok=True)

    filename = os.path.join(model_name, "vae_mean.png")
    # display a 2D plot of the digit classes in the latent space
    z_mean, _, _ = encoder.predict(x_test,
                                   batch_size=batch_size)
    plt.figure(figsize=(12, 10))
    plt.scatter(z_mean[:, 0], z_mean[:, 1])
    plt.colorbar()
    plt.xlabel("z[0]")
    plt.ylabel("z[1]")
    plt.savefig(filename)
    plt.show()
