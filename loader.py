import tensorflow as tf


class Loader:

    def __init__(self, path: str):
        self.model = tf.keras.models.load_model(path)
        self.encoder = tf.keras.models.Model(inputs=self.model.input, outputs=self.model.get_layer('encoder').output)

    def get_model(self):
        return self.model

    def get_encoder(self):
        return self.encoder

    def encode(self, data):
        return self.encoder.predict(data)

    def predict(self, data):
        return self.model.predict(data)


class TFLiteLoader:
    def __init__(self, path: str):
        converter = tf.lite.TFLiteConverter.from_keras_model_file(path)
        self.tflite_encoder = converter.convert()
        # Load TFLite model and allocate tensors.
        self.interpreter = tf.lite.Interpreter(model_content=self.tflite_encoder)
        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, data):
        self.interpreter.set_tensor(self.input_details[0]['index'], data)
        self.interpreter.invoke()
        tflite_result = self.interpreter.get_tensor(self.output_details[0]['index'])
        return tflite_result
