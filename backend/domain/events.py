from pydantic import BaseModel
from backend.domain.entities import Screenshot, SearchResult

class ScreenshotCapturedEvent(BaseModel):
    screenshot: Screenshot

class SearchPerformedEvent(BaseModel):
    query: str
    results: list[SearchResult]
