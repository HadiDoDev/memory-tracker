from typing import Optional, List

from fastapi import APIRouter, Query
from pydantic import BaseModel

from apps.logger.services import MemoryLoggerService

logger_router = APIRouter()
mem_log_service = MemoryLoggerService()


class Item(BaseModel):
    timestamp: int
    total: int
    free: int
    used: int


@logger_router.get("/memory-logs/", response_model=List[Item])
def memory_logs(
        limit: Optional[int] = Query(
            gt=0, lt=100000, default=10, description="Number of records to return from the end"),
        skip: Optional[int] = Query(None, gt=0, description="Number of records to skip")
):
    logs = MemoryLoggerService.get_logs(limit, skip)
    return logs
