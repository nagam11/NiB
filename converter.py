import glob
import os

import numpy as np
import tensorflow as tf
from scipy.io.wavfile import read

from config import SAMPLE_RATE, WINDOW_SIZE, WINDOW_STRIDE, WINDOW, DURATION
from loader import Loader

# Load the tf.keras model.
from util import transform_audio, load2spectrogram

# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model_file("./saved_models/crazy_bird_encoder.h5")
tflite_encoder = converter.convert()

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_content=tflite_encoder)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(input_details)
print(output_details)

# Test the TensorFlow Lite model on input data.
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

input_shape = input_details[0]['shape']
input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], dataset[[0], :])
interpreter.invoke()
tflite_results = interpreter.get_tensor(output_details[0]['index'])

# Test the TensorFlow model on random input data.
loader = Loader(path="./saved_models/crazy_bird.h5")
tf_results = loader.encode(dataset[[0], :])

# Compare the result.
for tf_result, tflite_result in zip(tf_results, tflite_results):
  np.testing.assert_almost_equal(tf_result, tflite_result, decimal=5)

print("Done")
