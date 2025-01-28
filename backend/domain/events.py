from dataclasses import dataclass
from backend.domain.entities import Screenshot, SearchResult

@dataclass
class ScreenshotCapturedEvent:
    screenshot: Screenshot

@dataclass
class SearchPerformedEvent:
    query: str
    results: list[SearchResult]
