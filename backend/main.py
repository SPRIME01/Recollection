from fastapi import FastAPI, Depends
from backend.services.screenshot import ScreenshotService
from backend.repositories.libsql_repo import LibSQLRepository
from backend.repositories.minio_repo import MinIORepository
from backend.domain.commands import CaptureScreenshotCommand
from backend.domain.entities import Screenshot
from pydantic import BaseModel

app = FastAPI()

# Dependency injection
def get_screenshot_service(db_repo: LibSQLRepository = Depends(LibSQLRepository), storage_repo: MinIORepository = Depends(MinIORepository)) -> ScreenshotService:
    return ScreenshotService(
        db_repo=db_repo,
        storage_repo=storage_repo
    )

class CaptureScreenshotResponse(BaseModel):
    status: str
    screenshot: Screenshot

@app.post("/capture", response_model=CaptureScreenshotResponse)
def capture_screenshot(service: ScreenshotService = Depends(get_screenshot_service)) -> CaptureScreenshotResponse:
    command = CaptureScreenshotCommand()
    screenshot = service.capture()
    return CaptureScreenshotResponse(status="success", screenshot=screenshot)

class TimelineResponse(BaseModel):
    screenshots: list[Screenshot]

@app.get("/timeline", response_model=TimelineResponse)
def get_timeline(service: ScreenshotService = Depends(get_screenshot_service)) -> TimelineResponse:
    screenshots = service.get_timeline()
    return TimelineResponse(screenshots=screenshots)
