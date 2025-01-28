from libsql_client import Client
from backend.domain.entities import Screenshot

class LibSQLRepository:
    def __init__(self):
        self.client = Client(url=os.getenv("LIBSQL_URL"))

    async def save_screenshot(self, screenshot: Screenshot) -> None:
        await self.client.execute(
            "INSERT INTO screenshots (timestamp, text, embedding, image_path) VALUES (?, ?, ?, ?)",
            [screenshot.timestamp, screenshot.text, screenshot.embedding.tobytes(), screenshot.image_path]
        )

    async def get_timeline(self) -> list[Screenshot]:
        result = await self.client.execute("SELECT * FROM screenshots ORDER BY timestamp DESC")
        return [Screenshot(**row) for row in result.rows]
