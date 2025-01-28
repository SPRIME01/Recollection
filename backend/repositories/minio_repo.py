from minio import Minio
import numpy as np
from PIL import Image
import os

class MinIORepository:
    def __init__(self):
        self.client = Minio(
            os.getenv("MINIO_ENDPOINT", "localhost:9000"),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=False
        )

    def save_image(self, image_path: str, image: np.ndarray) -> None:
        try:
            image_pil = Image.fromarray(image)
            image_pil.save(image_path, format="WEBP")
            self.client.fput_object("screenshots", image_path, image_path)
        except Exception as e:
            print(f"Failed to save image {image_path}: {e}")
