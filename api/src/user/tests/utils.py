import random
import re
import string
from datetime import datetime

import httpx

from src.config import smtp_settings
from src.database import database

MAILDEV_API_URL = (
    f"http://{smtp_settings.SMTP_SERVER}:{smtp_settings.SMTP_WEB_PORT}/email"
)


async def register_user(client, email: str, password: str):
    credentials = {"email": email, "password": password}
    return await client.post("/users/register", json=credentials)


async def activate_user(client, email: str, password: str, code: str):
    auth = get_auth_from_credentials(email, password)
    return await client.patch(
        "/users/activate",
        json={"code": code},
        auth=auth,
    )


def get_auth_from_credentials(username: str, password: str) -> httpx.BasicAuth:
    return httpx.BasicAuth(username=username, password=password)


async def get_all_emails() -> list:
    async with httpx.AsyncClient(
        auth=(smtp_settings.SMTP_USER, smtp_settings.SMTP_PASS)
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
        email
        for email in emails_after
        if email not in emails_before
        and email["to"][0]["address"] == credentials["email"]
    ]


def get_code_from_email(email):
    (code,) = re.findall(r"\d+", email["subject"])
    return code


async def get_last_verification_data(credentials):
    query = """
        SELECT *
        FROM user_verification
        WHERE user_id = (
            SELECT id
            FROM user_data
            WHERE email = :email
        )
        ORDER BY created_at DESC
        LIMIT 1;
    """
    row = await database.fetch_one(query, {"email": credentials["email"]})
    return row


def generate_random_email():
    random.seed(datetime.now().timestamp())
    choices = string.ascii_lowercase
    prefix = "".join(random.choice(choices) for _ in range(20))
    return f"{prefix}@test.com"


async def expire_verification_code(verification_data):
    query = """
        UPDATE user_verification
        SET created_at = NOW() - INTERVAL '2 minutes'
        WHERE id = :id;
    """
    await database.execute(query, {"id": verification_data["id"]})
