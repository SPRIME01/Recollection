from pydantic import BaseModel

class CaptureScreenshotCommand(BaseModel):
    pass

class SearchCommand(BaseModel):
    query: str
    threshold: float = 0.7

class UpdateCaptureSettingsCommand(BaseModel):
    continuous_capture_enabled: bool
    continuous_capture_interval: int
