from datetime import datetime

import httpx
import pytest
from asgi_lifespan import LifespanManager

from src.auth.utils import hash_password
from src.main import app as fastapi_app
from src.user.schemas import UserFromDB, UserVerificationFromDB
from src.user.tests.utils import (
    get_all_emails,
    generate_random_email,
)
from src.user.utils import generate_random_4_digits


@pytest.fixture(autouse=True)
def app():
    fastapi_app.dependency_overrides.clear()
    yield fastapi_app
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
async def manager_app(app):
    async with LifespanManager(app) as manager:
        yield manager.app


@pytest.fixture
async def client(manager_app):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=manager_app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def fake_user_id():
    return 1


@pytest.fixture
def fake_user_email():
    return generate_random_email()


@pytest.fixture
def fake_user_password():
    return "Password123!?"


@pytest.fixture
def fake_user_password_hash(fake_user_password):
    return hash_password(fake_user_password)


@pytest.fixture
def fake_inactive_user(fake_user_id, fake_user_email, fake_user_password_hash):
    return UserFromDB(
        id=fake_user_id,
        email=fake_user_email,
        password_hash=fake_user_password_hash,
        is_active=False,
    )


@pytest.fixture
def fake_active_user(fake_inactive_user):
    return UserFromDB(
        **fake_inactive_user.model_copy(update={"is_active": True}).model_dump()
    )


@pytest.fixture
def verification_code():
    return generate_random_4_digits()


@pytest.fixture
def fake_user_verification(fake_user_id, verification_code):
    return UserVerificationFromDB(
        id=1,
        user_id=fake_user_id,
        code=verification_code,
        created_at=datetime.now(),
    )


@pytest.fixture
async def emails_before(fake_user_email):
    emails = await get_all_emails()
    return [email for email in emails if email["to"][0]["address"] == fake_user_email]


@pytest.fixture
def invalid_email():
    return "email@test"


@pytest.fixture
def invalid_password():
    return "password"


@pytest.fixture
def random_credentials(fake_user_email, fake_user_password):
    return {"email": fake_user_email, "password": fake_user_password}


@pytest.fixture
def random_credentials_invalid_email(invalid_email, fake_user_password):
    return {"email": invalid_email, "password": fake_user_password}


@pytest.fixture
def random_credentials_invalid_password(fake_user_email, invalid_password):
    return {"email": fake_user_email, "password": invalid_password}


@pytest.fixture
def random_auth(fake_user_email, fake_user_password):
    return httpx.BasicAuth(username=fake_user_email, password=fake_user_password)
