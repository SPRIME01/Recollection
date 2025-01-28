from pydantic import BaseModel
import numpy as np

class Screenshot(BaseModel):
    timestamp: int
    text: str
    embedding: np.ndarray
    image_path: str

class SearchResult(BaseModel):
    screenshot: Screenshot
    similarity_score: float
