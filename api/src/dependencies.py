from src.database import database


def get_db():
    yield database
