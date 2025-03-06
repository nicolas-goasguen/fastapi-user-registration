from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.db import database
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

app.include_router(users_router)
