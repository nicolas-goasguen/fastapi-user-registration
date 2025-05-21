from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import project_settings
from src.database import database
from src.exceptions import register_all_exception_handlers
from src.logging import setup_logging
from src.user.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


setup_logging()

app = FastAPI(
    title=f"{project_settings.PROJECT_NAME} - {project_settings.ENVIRONMENT}",
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
