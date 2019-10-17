import os

import librosa
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

from config import DURATION, SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW


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


def load2spectrogram(path: str):
    sr, a = read(path)
    a = np.array(a, dtype=float)
    if a.shape[0] == DURATION:
        datapoint = transform_audio(a, SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW)
        datapoint = np.reshape(datapoint, (np.product(datapoint.shape),))
        return datapoint
    return None


def plot_results(test, decoded, n=10):
    plt.figure(figsize=(20, 4))
    for i in range(n):
        # display original
        ax = plt.subplot(2, n, i + 1)
        plt.imshow(test[i].reshape(161, 51))
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # display reconstruction
        ax = plt.subplot(2, n, i + 1 + n)
        plt.imshow(decoded[i].reshape(161, 51))
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    plt.show()
