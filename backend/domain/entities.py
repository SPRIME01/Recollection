from dataclasses import dataclass
import numpy as np

@dataclass
class Screenshot:
    timestamp: int
    text: str
    embedding: np.ndarray
    image_path: str

@dataclass
class SearchResult:
    screenshot: Screenshot
    similarity_score: float
