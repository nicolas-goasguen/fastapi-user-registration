import httpx
import pytest

from asgi_lifespan import LifespanManager

from app.main import app as fastapi_app
from app.tests.assertions import (
    assert_register_ok,
    assert_only_one_correct_mail_sent,
    assert_activate_ok,
)
from app.tests.tools import (
    get_all_emails,
    get_last_verification_data,
    get_random_email,
)



@pytest.fixture
async def app():
    async with LifespanManager(fastapi_app) as manager:
        yield manager.app


@pytest.fixture
async def client(app):
    async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://api",
    ) as client:
        yield client


@pytest.fixture
async def emails_before(random_email):
    emails = await get_all_emails()
    return [
        email for email in emails
        if email["to"][0]["address"] == random_email
    ]


@pytest.fixture
def random_email():
    return get_random_email()


@pytest.fixture
def invalid_email():
    return "email@test"


@pytest.fixture
def valid_password():
    return "Password123!?"


@pytest.fixture
def invalid_password():
    return "password"


@pytest.fixture
def random_credentials(random_email, valid_password):
    return {
        "email": random_email,
        "password": valid_password
    }


@pytest.fixture
def random_credentials_invalid_email(invalid_email, valid_password):
    return {
        "email": invalid_email,
        "password": valid_password
    }


@pytest.fixture
def random_credentials_invalid_password(random_email, invalid_password):
    return {
        "email": random_email,
        "password": invalid_password
    }


@pytest.fixture
def random_auth(random_email, valid_password):
    return httpx.BasicAuth(username=random_email, password=valid_password)


@pytest.fixture
async def register_user(
        client,
        random_credentials,
        random_auth,
        emails_before
):
    response = await client.post("/users/register", json=random_credentials)
    assert_register_ok(response)


@pytest.fixture
async def verification_data(
        register_user,
        random_credentials,
        emails_before
):
    verif_data = await get_last_verification_data(random_credentials)
    assert verif_data is not None

    await assert_only_one_correct_mail_sent(
        random_credentials,
        verif_data,
        emails_before,
    )

    return verif_data


@pytest.fixture
async def activate_user(
        client,
        register_user,
        random_auth,
        verification_data,
):
    response_activate = await client.patch(
        "/users/activate",
        json={"verification_code": verification_data["code"]},
        auth=random_auth,
    )
    assert_activate_ok(response_activate)
