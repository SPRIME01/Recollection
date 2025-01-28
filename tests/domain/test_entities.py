import pytest
import numpy as np
from backend.domain.entities import Screenshot, SearchResult

def test_screenshot_dict():
    embedding = np.array([0.1, 0.2, 0.3])
    screenshot = Screenshot(
        timestamp=1234567890,
        text="example text",
        embedding=embedding,
        image_path="path/to/image.webp"
    )
    screenshot_dict = screenshot.dict()
    assert screenshot_dict["embedding"] == embedding.tolist()

def test_screenshot_parse_obj():
    embedding = [0.1, 0.2, 0.3]
    screenshot_data = {
        "timestamp": 1234567890,
        "text": "example text",
        "embedding": embedding,
        "image_path": "path/to/image.webp"
    }
    screenshot = Screenshot.parse_obj(screenshot_data)
    assert isinstance(screenshot.embedding, np.ndarray)
    assert np.array_equal(screenshot.embedding, np.array(embedding))

def test_search_result():
    embedding = np.array([0.1, 0.2, 0.3])
    screenshot = Screenshot(
        timestamp=1234567890,
        text="example text",
        embedding=embedding,
        image_path="path/to/image.webp"
    )
    search_result = SearchResult(
        screenshot=screenshot,
        similarity_score=0.95
    )
    assert search_result.screenshot == screenshot
    assert search_result.similarity_score == 0.95
