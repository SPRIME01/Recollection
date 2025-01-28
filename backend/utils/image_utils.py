import numpy as np
from PIL import Image
import io

def preprocess_image(image: np.ndarray) -> np.ndarray:
    # Add preprocessing logic (e.g., resizing, normalization)
    return image

def optimize_image(image: np.ndarray) -> bytes:
    # Convert the image to a PIL Image
    pil_image = Image.fromarray(image)

    # Optimize the image by converting it to WEBP format
    buffer = io.BytesIO()
    pil_image.save(buffer, format="WEBP", quality=80)
    optimized_image = buffer.getvalue()

    return optimized_image
