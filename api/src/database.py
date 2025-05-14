from databases import Database

from src.config import settings

database = Database(settings.DATABASE_URL)


async def get_db():
    yield database
