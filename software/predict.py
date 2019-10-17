import tensorflow as tf

import numpy as np
from scipy.io.wavfile import read

from autoencoder import Autoencoder
from util import transform_audio
from config import DURATION, SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW

INOUT_DIM = 161
ENCODED_DIM = 5

tf.reset_default_graph()

latest_checkpoint = tf.train.latest_checkpoint('./saved_models')

model = Autoencoder(inout_dim=INOUT_DIM, encoded_dim=ENCODED_DIM)
saver = tf.train.Saver()

session = tf.Session()

if latest_checkpoint:
    saver.restore(session, latest_checkpoint)

a = np.array(read("./wav/bahama_mockingbird_0.wav")[1], dtype=float)
if a.shape[0] == DURATION:
    print(model.getEncoded(transform_audio(a, SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW)))
