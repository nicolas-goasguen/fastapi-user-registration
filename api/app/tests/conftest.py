import httpx
import pytest

from app.tests.tools import (
    get_all_emails, get_random_email, get_random_password
)


@pytest.fixture
async def emails():
    emails = await get_all_emails()
    return emails


@pytest.fixture
def random_email():
    return get_random_email()


@pytest.fixture
def random_password():
    return get_random_password()


@pytest.fixture
def random_credentials(random_email, random_password):
    return {
        "email": random_email,
        "password": random_password
    }


@pytest.fixture
def random_auth(random_email, random_password):
    return httpx.BasicAuth(username=random_email, password=random_password)
