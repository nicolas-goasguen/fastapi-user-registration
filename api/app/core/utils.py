import random
from email.message import EmailMessage

import aiosmtplib
import bcrypt

from app.core.config import settings

import re


def is_valid_password(password: str):
    pattern = re.compile(
        "^(?=.*[a-z])"
        "(?=.*[A-Z])"
        "(?=.*\d)"
        "(?=.*[@$!%*#?&])"
        "[A-Za-z\d@$!#%*?&]{6,20}$"
    )
    return re.search(pattern, password)


def is_valid_verification_code(code):
    pattern = re.compile("^[0-9]{4}$")
    return re.search(pattern, code)


def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def generate_4_digits():
    return ''.join(random.choices('0123456789', k=4))


async def send_email(user_email, code: str):
    from_ = "registration@example.com"
    to_ = user_email
    subject = f"Your verification code: {code}"
    body = f"Please use this code to verify your registration: {code}. This code is valid for 1 minute."

    message = EmailMessage()
    message["From"] = from_
    message["To"] = to_
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname="mail",
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD
    )
