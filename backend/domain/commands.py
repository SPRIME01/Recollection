from dataclasses import dataclass

@dataclass
class CaptureScreenshotCommand:
    pass

@dataclass
class SearchCommand:
    query: str
    threshold: float = 0.7
