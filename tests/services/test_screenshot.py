import pytest
import numpy as np
from unittest.mock import MagicMock
from backend.services.screenshot import ScreenshotService
from backend.domain.entities import Screenshot

@pytest.fixture
def mock_db_repo():
    return MagicMock()

@pytest.fixture
def mock_storage_repo():
    return MagicMock()

@pytest.fixture
def screenshot_service(mock_db_repo, mock_storage_repo):
    return ScreenshotService(db_repo=mock_db_repo, storage_repo=mock_storage_repo)

def test_capture_screenshot(screenshot_service, mock_db_repo, mock_storage_repo):
    mock_db_repo.save_screenshot = MagicMock()
    mock_storage_repo.save_image = MagicMock()

    screenshot = screenshot_service.capture()

    assert isinstance(screenshot, Screenshot)
    assert mock_db_repo.save_screenshot.called
    assert mock_storage_repo.save_image.called

def test_get_timeline(screenshot_service, mock_db_repo):
    mock_db_repo.get_timeline = MagicMock(return_value=[])

    timeline = screenshot_service.get_timeline()

    assert isinstance(timeline, list)
    assert mock_db_repo.get_timeline.called
