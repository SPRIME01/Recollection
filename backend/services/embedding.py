import numpy as np
from sentence_transformers import SentenceTransformer
from backend.config import settings
from PIL import Image
import tensorflow as tf

class EmbeddingService:
    def __init__(self) -> None:
        self.text_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.image_model = tf.lite.Interpreter(model_path=settings.clip_model_path)
        self.image_model.allocate_tensors()

    def compute_embedding(self, text: str) -> np.ndarray:
        return self.text_model.encode(text)

    def compute_image_embedding(self, image: Image) -> np.ndarray:
        input_details = self.image_model.get_input_details()
        output_details = self.image_model.get_output_details()

        image = np.array(image, dtype=np.float32)
        image = np.expand_dims(image, axis=0)
        self.image_model.set_tensor(input_details[0]['index'], image)
        self.image_model.invoke()
        embedding = self.image_model.get_tensor(output_details[0]['index'])
        return embedding.flatten()
