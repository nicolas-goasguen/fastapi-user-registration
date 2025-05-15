import asyncio
from email.message import EmailMessage

import aiosmtplib
from celery import shared_task

from src.config import smtp_settings as settings


async def send_email(to_, subject, body):
    message = EmailMessage()
    message["From"] = settings.SMTP_SENDER
    message["To"] = to_
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_SERVER,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASS,
    )


@shared_task(bind=True, default_retry_delay=5, time_limit=50)
def send_verification_email(self, to_, code: str):
    to_ = to_
    subject = f"Your verification code: {code}"
    body = f"Please use this code to verify your registration: {code}. This code is valid for 1 minute."
    try:
        asyncio.run(send_email(to_, subject, body))
    except Exception as e:  # todo: more precise catch
        raise self.retry(exc=e)


@shared_task(bind=True, default_retry_delay=5, time_limit=50)
def send_confirmation_email(self, to_):
    to_ = to_
    subject = f"Your account has been activated."
    body = f"Your account has been successfully activated. Thank you for joining us!"
    try:
        asyncio.run(send_email(to_, subject, body))
    except Exception as e:  # todo: more precise catch
        raise self.retry(exc=e)
