from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PROJECT
    PROJECT_NAME: str = "User Registration API"
    ENVIRONMENT: str

    # DATABASE
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASS: str
    DATABASE_URL: str

    # SMTP
    SMTP_PORT: int
    SMTP_WEB_PORT: int
    SMTP_USER: str
    SMTP_PASS: str


settings = Settings()
