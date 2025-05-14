from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.db import database
from app.core.exceptions.handlers_loader import register_all_exception_handlers
from app.modules.user.routes import router as user_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(
    title=f"{settings.PROJECT_NAME} - {settings.ENVIRONMENT}",
    description="""
**Overview**

User registration API in Python with FastAPI.

**Features**
* Create a user with an email and a password.
* Email the user with a 4 digits code.
* Activate a user account with the 4 digits code received using basic authentication.
* The user has only one minute to use this code. An error is raised if used after that.
""",
    lifespan=lifespan,
)

app.include_router(user_router)

register_all_exception_handlers(app)  # automatically load handlers from modules
