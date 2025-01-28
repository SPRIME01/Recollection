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

def test_update_capture_settings_integration():
    response = client.post("/settings", json={
        "continuous_capture_enabled": True,
        "continuous_capture_interval": 30
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_continuous_capture_integration():
    response = client.post("/settings", json={
        "continuous_capture_enabled": True,
        "continuous_capture_interval": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

    # Wait for a few seconds to allow multiple captures
    import time
    time.sleep(5)

    response = client.post("/settings", json={
        "continuous_capture_enabled": False,
        "continuous_capture_interval": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

    response = client.get("/timeline")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["screenshots"], list)
    assert len(data["screenshots"]) > 1
