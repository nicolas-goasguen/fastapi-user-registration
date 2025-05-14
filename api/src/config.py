from pydantic_settings import BaseSettings


class ProjectSettings(BaseSettings):
    PROJECT_NAME: str = "User Registration API"
    ENVIRONMENT: str


class DBSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASS: str
    DATABASE_URL: str


class SMTPSettings(BaseSettings):
    SMTP_PORT: int
    SMTP_WEB_PORT: int
    SMTP_USER: str
    SMTP_PASS: str


class BrokerSettings(BaseSettings):
    RABBITMQ_NODE_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASS: str


class WorkerSettings(BaseSettings):
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str


project_settings = ProjectSettings()
db_settings = DBSettings()
smtp_settings = SMTPSettings()
broker_settings = BrokerSettings()
worker_settings = WorkerSettings()
