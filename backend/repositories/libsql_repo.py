from libsql_client import Client
from backend.domain.entities import Screenshot, CaptureSettings
from typing import List
import os

class LibSQLRepository:
    def __init__(self):
        self.client = Client(url=os.getenv("LIBSQL_URL"))

    def save_screenshot(self, screenshot: Screenshot) -> None:
        self.client.execute(
            "INSERT INTO screenshots (timestamp, text, embedding, image_path) VALUES (?, ?, ?, ?)",
            [screenshot.timestamp, screenshot.text, screenshot.embedding.tobytes(), screenshot.image_path]
        )

    def get_timeline(self) -> List[Screenshot]:
        result = self.client.execute("SELECT * FROM screenshots ORDER BY timestamp DESC")
        return [Screenshot(**row) for row in result.rows]

    def save_capture_settings(self, settings: CaptureSettings) -> None:
        self.client.execute(
            "INSERT INTO capture_settings (continuous_capture_enabled, continuous_capture_interval) VALUES (?, ?)",
            [settings.continuous_capture_enabled, settings.continuous_capture_interval]
        )

    def get_capture_settings(self) -> CaptureSettings:
        result = self.client.execute("SELECT * FROM capture_settings LIMIT 1")
        if result.rows:
            return CaptureSettings(**result.rows[0])
        return CaptureSettings(continuous_capture_enabled=False, continuous_capture_interval=60)

    def get_all_embeddings(self) -> List[dict]:
        result = self.client.execute("SELECT timestamp, embedding, image_path FROM screenshots")
        return [{"timestamp": row["timestamp"], "embedding": row["embedding"], "image_path": row["image_path"]} for row in result.rows]
