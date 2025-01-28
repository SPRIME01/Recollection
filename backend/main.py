from fastapi import FastAPI, Depends
from backend.services.screenshot import ScreenshotService
from backend.repositories.libsql_repo import LibSQLRepository
from backend.repositories.minio_repo import MinIORepository
from backend.domain.commands import CaptureScreenshotCommand
from backend.domain.entities import Screenshot
from pydantic import BaseModel

app = FastAPI()

# Dependency injection
def get_screenshot_service() -> ScreenshotService:
    return ScreenshotService(
        db_repo=LibSQLRepository(),
        storage_repo=MinIORepository()
    )

class CaptureScreenshotResponse(BaseModel):
    status: str
    screenshot: Screenshot

@app.post("/capture", response_model=CaptureScreenshotResponse)
async def capture_screenshot(service: ScreenshotService = Depends(get_screenshot_service)) -> CaptureScreenshotResponse:
    command = CaptureScreenshotCommand()
    screenshot = await service.capture()
    return CaptureScreenshotResponse(status="success", screenshot=screenshot)

class TimelineResponse(BaseModel):
    screenshots: list[Screenshot]

@app.get("/timeline", response_model=TimelineResponse)
async def get_timeline(service: ScreenshotService = Depends(get_screenshot_service)) -> TimelineResponse:
    screenshots = await service.get_timeline()
    return TimelineResponse(screenshots=screenshots)
