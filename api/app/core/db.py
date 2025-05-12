from typing import AsyncGenerator

from databases import Database

from app.core.config import settings

database = Database(settings.DATABASE_URL)


async def get_db() -> AsyncGenerator[Database, None]:
    yield database
