import tflite_runtime.interpreter as tflite


class TFLiteLoader:
    """
    Loader for a tensorflow lite model
    """
    def __init__(self, path: str):
        # Load TFLite model and allocate tensors.
        self.interpreter = tflite.Interpreter(model_path=path)
        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, data):
        self.interpreter.set_tensor(self.input_details[0]['index'], data)
        self.interpreter.invoke()
        tflite_result = self.interpreter.get_tensor(self.output_details[0]['index'])
        return tflite_result
