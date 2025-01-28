from fastapi import FastAPI, Depends
from backend.services.screenshot import ScreenshotService
from backend.repositories.libsql_repo import LibSQLRepository
from backend.repositories.minio_repo import MinIORepository
from backend.domain.commands import CaptureScreenshotCommand, UpdateCaptureSettingsCommand
from backend.domain.entities import Screenshot, CaptureSettings
from pydantic import BaseModel
from backend.use_cases.search import search as search_use_case
from backend.domain.commands import SearchCommand
from backend.domain.entities import SearchResult

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

class UpdateCaptureSettingsResponse(BaseModel):
    status: str

@app.post("/settings", response_model=UpdateCaptureSettingsResponse)
def update_capture_settings(command: UpdateCaptureSettingsCommand, service: ScreenshotService = Depends(get_screenshot_service)) -> UpdateCaptureSettingsResponse:
    service.update_capture_settings(command)
    return UpdateCaptureSettingsResponse(status="success")

class SearchRequest(BaseModel):
    query: str
    threshold: float

class SearchResponse(BaseModel):
    results: list[SearchResult]

@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest, service: ScreenshotService = Depends(get_screenshot_service)) -> SearchResponse:
    command = SearchCommand(query=request.query, threshold=request.threshold)
    results = search_use_case(command, service)
    return SearchResponse(results=results.results)
