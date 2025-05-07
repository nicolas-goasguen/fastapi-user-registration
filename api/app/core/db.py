import asyncio
import os
import time

from databases import Database

from app.core.config import settings

DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(settings.DATABASE_URL)
