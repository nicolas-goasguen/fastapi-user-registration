import asyncio
from email.message import EmailMessage

import aiosmtplib
from celery import shared_task

from src.config import smtp_settings


async def send_email(from_, to_, subject, body):
    from_ = from_
    to_ = to_
    subject = subject
    body = body

    message = EmailMessage()
    message["From"] = from_
    message["To"] = to_
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname="mail",
        port=smtp_settings.SMTP_PORT,
        username=smtp_settings.SMTP_USER,
        password=smtp_settings.SMTP_PASS,
    )


@shared_task(bind=True, default_retry_delay=5, time_limit=50)
def send_verification_email(self, user_email, code: str):
    from_ = "registration@example.com"
    to_ = user_email
    subject = f"Your verification code: {code}"
    body = f"Please use this code to verify your registration: {code}. This code is valid for 1 minute."
    try:
        asyncio.run(send_email(from_, to_, subject, body))
    except Exception as e:  # todo: more precise catch
        raise self.retry(exc=e)


@shared_task(bind=True, default_retry_delay=5, time_limit=50)
def send_confirmation_email(self, user_email):
    from_ = "registration@example.com"
    to_ = user_email
    subject = f"Your account has been activated."
    body = f"Your account has been successfully activated. Thank you for joining us!"
    try:
        asyncio.run(send_email(from_, to_, subject, body))
    except Exception as e:  # todo: more precise catch
        raise self.retry(exc=e)
