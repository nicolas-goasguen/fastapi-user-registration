from celery import Celery

from src.config import worker_settings

celery = Celery(
    "worker",
    broker=worker_settings.CELERY_BROKER_URL,
    backend=worker_settings.CELERY_RESULT_BACKEND,
)

celery.autodiscover_tasks(
    [
        "src.user",  # discovers src.user.tasks (thanks to __all__ declaration)
    ]
)
