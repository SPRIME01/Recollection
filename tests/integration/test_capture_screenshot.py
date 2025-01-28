import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.domain.entities import Screenshot

client = TestClient(app)

def test_capture_screenshot_integration():
    response = client.post("/capture")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["screenshot"], dict)
    assert "timestamp" in data["screenshot"]
    assert "text" in data["screenshot"]
    assert "embedding" in data["screenshot"]
    assert "image_path" in data["screenshot"]

def test_get_timeline_integration():
    response = client.get("/timeline")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["screenshots"], list)
    for screenshot in data["screenshots"]:
        assert isinstance(screenshot, dict)
        assert "timestamp" in screenshot
        assert "text" in screenshot
        assert "embedding" in screenshot
        assert "image_path" in screenshot
