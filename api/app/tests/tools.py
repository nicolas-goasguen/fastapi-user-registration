import random
import re
import string
from datetime import datetime

import httpx

from app.core.config import settings
from app.core.db import database

MAILDEV_API_URL = f"http://mail:{settings.SMTP_WEB_PORT}/email"


async def get_all_emails():
    async with httpx.AsyncClient(
            auth=(settings.SMTP_USER, settings.SMTP_PASSWORD)
    ) as client:
        response = await client.get(MAILDEV_API_URL)
        response.raise_for_status()
        emails = response.json()
        if not emails:
            return []
        return emails


async def get_user_new_emails(credentials, emails_before):
    emails_after = await get_all_emails()
    return [
        email for email in emails_after
        if email not in emails_before
           and email["to"][0]["address"] == credentials["email"]
    ]


def get_code_from_email(email):
    code, = re.findall(r'\d+', email["subject"])
    return code


async def get_last_verification_data(credentials):
    query = """
        SELECT *
        FROM verification_codes
        WHERE user_id = (
            SELECT id
            FROM users
            WHERE email = :email
        )
        ORDER BY created_at DESC
        LIMIT 1;
    """
    row = await database.fetch_one(
        query, {"email": credentials["email"]}
    )
    return row


def get_random_email():
    random.seed(datetime.now().timestamp())
    choices = string.ascii_lowercase + string.digits
    prefix = ''.join(random.choice(choices) for _ in range(15))
    return f"{prefix}@test.com"


def get_random_password():
    random.seed(datetime.now().timestamp())
    choices = string.ascii_letters + string.digits
    return ''.join(random.choice(choices) for _ in range(20))


async def expire_verification_code(verification_data):
    query = """
        UPDATE verification_codes
        SET created_at = NOW() - INTERVAL '2 minutes'
        WHERE id = :id;
    """
    await database.execute(query, {"id": verification_data["id"]})
