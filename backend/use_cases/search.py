from backend.services.screenshot import ScreenshotService
from backend.domain.commands import SearchCommand
from backend.domain.entities import SearchResult
from backend.repositories.libsql_repo import LibSQLRepository
from backend.repositories.minio_repo import MinIORepository
from fastapi import Depends
from pydantic import BaseModel

class SearchResponse(BaseModel):
    results: list[SearchResult]

async def search(command: SearchCommand, service: ScreenshotService = Depends(ScreenshotService)) -> SearchResponse:
    results = await service.search(command.query, command.threshold)
    return SearchResponse(results=results)
