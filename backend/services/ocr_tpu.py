import numpy as np
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter

class CoralOCR:
    def __init__(self) -> None:
        self.interpreter = make_interpreter("backend/models/ocr_edgetpu.tflite")
        self.interpreter.allocate_tensors()

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        # Resize and normalize image for TPU
        return image

    def extract_text(self, image: np.ndarray) -> str:
        input_tensor = self.preprocess_image(image)
        common.set_input(self.interpreter, input_tensor)
        self.interpreter.invoke()
        return self.postprocess_output(
            common.output_tensor(self.interpreter, 0)
        )

    def postprocess_output(self, output: np.ndarray) -> str:
        # Convert model output to text
        return "extracted text"
