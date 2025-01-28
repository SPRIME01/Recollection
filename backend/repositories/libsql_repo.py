from libsql_client import Client
from backend.domain.entities import Screenshot
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
