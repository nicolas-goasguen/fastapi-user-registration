from databases import Database

from src.config import db_settings

database = Database(db_settings.DATABASE_URL)


async def get_db():
    yield database
