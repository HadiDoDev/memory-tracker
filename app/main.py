from fastapi import FastAPI

from memory_tracker.configs import ProjectConfig
from apps.logger.api import logger_router


app = FastAPI()

app.include_router(logger_router)
