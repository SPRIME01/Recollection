from pydantic import BaseModel

class CaptureScreenshotCommand(BaseModel):
    pass

class SearchCommand(BaseModel):
    query: str
    threshold: float = 0.7
