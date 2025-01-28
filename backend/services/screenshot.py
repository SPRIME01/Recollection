import time
import numpy as np
from PIL import Image
from backend.domain.entities import Screenshot
from backend.repositories.libsql_repo import LibSQLRepository
from backend.repositories.minio_repo import MinIORepository
from backend.services.ocr_tpu import CoralOCR
from backend.services.embedding import EmbeddingService
from backend.config import settings

class ScreenshotService:
    def __init__(self, db_repo: LibSQLRepository, storage_repo: MinIORepository):
        self.db_repo = db_repo
        self.storage_repo = storage_repo
        self.ocr = CoralOCR()
        self.embedding = EmbeddingService()

    def capture(self) -> Screenshot:
        # Simulate screenshot capture
        image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
        timestamp = int(time.time())
        text = self.ocr.extract_text(image)
        embedding = self.embedding.compute_embedding(text)

        # Save to storage
        image_path = f"{timestamp}.webp"
        self.storage_repo.save_image(image_path, image)

        # Save to database
        screenshot = Screenshot(
            timestamp=timestamp,
            text=text,
            embedding=embedding,
            image_path=image_path
        )
        self.db_repo.save_screenshot(screenshot)
        return screenshot

    def get_timeline(self) -> list[Screenshot]:
        return self.db_repo.get_timeline()

    def update_capture_settings(self, command):
        settings.continuous_capture_enabled = command.continuous_capture_enabled
        settings.continuous_capture_interval = command.continuous_capture_interval

    def continuous_capture_loop(self):
        while settings.continuous_capture_enabled:
            self.capture()
            time.sleep(settings.continuous_capture_interval)
