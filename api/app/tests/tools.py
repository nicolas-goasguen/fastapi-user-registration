import random
import re
import string
from datetime import datetime

import httpx

from app.core.config import settings

MAILDEV_API_URL = "http://mail:1080/email"


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


async def get_last_email():
    emails = await get_all_emails()
    if not emails:
        return None
    return emails[-1]


async def get_last_code():
    last_email = await get_last_email()
    if not last_email:
        return None
    code, = re.findall(r'\d+', last_email['subject'])
    return code


def get_random_email():
    random.seed(datetime.now().timestamp())
    choices = string.ascii_lowercase + string.digits
    prefix = ''.join(random.choice(choices) for _ in range(15))
    return f"{prefix}@test.com"


def get_random_password():
    random.seed(datetime.now().timestamp())
    choices = string.ascii_letters + string.digits
    return ''.join(random.choice(choices) for _ in range(20))
