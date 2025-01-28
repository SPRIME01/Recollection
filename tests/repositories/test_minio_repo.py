import pytest
from unittest.mock import patch, MagicMock
from backend.repositories.minio_repo import MinIORepository
import numpy as np

@pytest.fixture
def minio_repo():
    with patch('backend.repositories.minio_repo.Minio') as MockMinio:
        yield MinIORepository()

def test_save_image(minio_repo):
    image_path = "test_image.webp"
    image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

    with patch('backend.repositories.minio_repo.Image.fromarray') as mock_fromarray, \
         patch('backend.repositories.minio_repo.Minio.fput_object') as mock_fput_object:
        
        mock_image = MagicMock()
        mock_fromarray.return_value = mock_image

        minio_repo.save_image(image_path, image)

        mock_fromarray.assert_called_once_with(image)
        mock_image.save.assert_called_once_with(image_path, format="WEBP")
        mock_fput_object.assert_called_once_with("screenshots", image_path, image_path)
