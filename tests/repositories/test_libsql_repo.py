import pytest
from unittest.mock import MagicMock
from backend.repositories.libsql_repo import LibSQLRepository
from backend.domain.entities import Screenshot

@pytest.fixture
def mock_client():
    return MagicMock()

@pytest.fixture
def libsql_repo(mock_client):
    repo = LibSQLRepository()
    repo.client = mock_client
    return repo

def test_save_screenshot(libsql_repo, mock_client):
    screenshot = Screenshot(
        timestamp=1234567890,
        text="example text",
        embedding=[0.1, 0.2, 0.3],
        image_path="path/to/image.webp"
    )
    libsql_repo.save_screenshot(screenshot)
    assert mock_client.execute.called
    assert mock_client.execute.call_args[0][0] == "INSERT INTO screenshots (timestamp, text, embedding, image_path) VALUES (?, ?, ?, ?)"
    assert mock_client.execute.call_args[0][1] == [1234567890, "example text", b'\x9a\x99\x99\x99\x99\x99\xb9?', "path/to/image.webp"]

def test_get_timeline(libsql_repo, mock_client):
    mock_client.execute.return_value.rows = [
        {"timestamp": 1234567890, "text": "example text", "embedding": [0.1, 0.2, 0.3], "image_path": "path/to/image.webp"}
    ]
    timeline = libsql_repo.get_timeline()
    assert len(timeline) == 1
    assert isinstance(timeline[0], Screenshot)
    assert timeline[0].timestamp == 1234567890
    assert timeline[0].text == "example text"
    assert timeline[0].embedding == [0.1, 0.2, 0.3]
    assert timeline[0].image_path == "path/to/image.webp"
