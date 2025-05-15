from databases import Database

from src.config import db_settings as settings

database = Database(settings.DATABASE_URL)
