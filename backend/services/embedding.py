import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def compute_embedding(self, text: str) -> np.ndarray:
        return self.model.encode(text)
