from minio import Minio
import numpy as np
from PIL import Image

class MinIORepository:
    def __init__(self):
        self.client = Minio(
            os.getenv("MINIO_ENDPOINT", "localhost:9000"),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=False
        )

    def save_image(self, image_path: str, image: np.ndarray) -> None:
        image_pil = Image.fromarray(image)
        image_pil.save(image_path, format="WEBP")
        self.client.fput_object("screenshots", image_path, image_path)
