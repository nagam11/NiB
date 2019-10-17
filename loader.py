import tensorflow as tf


class Loader:

    def __init__(self, path: str):
        self.model = tf.keras.models.load_model(path)
        self.encoder = tf.keras.models.Model(inputs=self.model.input, outputs=self.model.get_layer('encoder').output)

    def get_model(self):
        return self.model

    def get_encoder(self):
        return self.encoder

    def encode(self, input):
        return self.encoder.predict(input)

    def decode(self, input):
        return self.model.predict(input)
