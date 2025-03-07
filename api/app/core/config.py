from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    # PROJECT
    PROJECT_NAME: str = "User Registration API"

    # DATABASE
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_URL: str

    # SMTP
    SMTP_PORT: int
    SMTP_WEB_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    class Config:
        env_file = ENV_FILE
        env_file_encoding = "utf-8"


settings = Settings()
