from fastapi import FastAPI, Depends
from backend.services.screenshot import ScreenshotService
from backend.repositories.libsql_repo import LibSQLRepository
from backend.repositories.minio_repo import MinIORepository
from backend.domain.commands import CaptureScreenshotCommand
from backend.domain.entities import Screenshot

app = FastAPI()

# Dependency injection
def get_screenshot_service():
    return ScreenshotService(
        db_repo=LibSQLRepository(),
        storage_repo=MinIORepository()
    )

@app.post("/capture")
async def capture_screenshot(service: ScreenshotService = Depends(get_screenshot_service)):
    command = CaptureScreenshotCommand()
    screenshot = await service.execute(command)
    return {"status": "success", "screenshot": screenshot}

@app.get("/timeline")
async def get_timeline(service: ScreenshotService = Depends(get_screenshot_service)):
    screenshots = await service.get_timeline()
    return {"screenshots": screenshots}
