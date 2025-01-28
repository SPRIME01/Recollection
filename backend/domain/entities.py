from pydantic import BaseModel
import numpy as np
from typing import Any

class Screenshot(BaseModel):
    timestamp: int
    text: str
    embedding: Any
    image_path: str

    class Config:
        arbitrary_types_allowed = True

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['embedding'] = self.embedding.tolist()
        return d

    @classmethod
    def parse_obj(cls, obj):
        obj['embedding'] = np.array(obj['embedding'])
        return super().parse_obj(obj)

class SearchResult(BaseModel):
    screenshot: Screenshot
    similarity_score: float
    embedding: Any

    class Config:
        arbitrary_types_allowed = True

class CaptureSettings(BaseModel):
    continuous_capture_enabled: bool
    continuous_capture_interval: int
