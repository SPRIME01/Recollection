from backend.services.screenshot import ScreenshotService
from backend.domain.commands import CaptureScreenshotCommand
from backend.domain.entities import Screenshot
from backend.repositories.libsql_repo import LibSQLRepository
from backend.repositories.minio_repo import MinIORepository
from fastapi import Depends
from pydantic import BaseModel

class CaptureScreenshotResponse(BaseModel):
    status: str
    screenshot: Screenshot

async def capture(service: ScreenshotService = Depends(ScreenshotService)) -> CaptureScreenshotResponse:
    command = CaptureScreenshotCommand()
    screenshot = await service.capture()
    return CaptureScreenshotResponse(status="success", screenshot=screenshot)
