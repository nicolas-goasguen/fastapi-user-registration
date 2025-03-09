import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager

from app.main import app as fastapi_app
from app.core.utils import generate_4_digits
from app.tests.assertions import (
    assert_register_ok,
    assert_register_ko_already_registered,
    assert_activate_ok,
    assert_activate_ko_invalid_credentials,
    assert_activate_ko_already_activated,
    assert_activate_ko_invalid_verification_code,
    assert_activate_ko_expired_verification_code,
    assert_only_one_email_sent,
)
from app.tests.tools import get_code_from_last_email


@pytest_asyncio.fixture
async def app():
    async with LifespanManager(fastapi_app) as manager:
        yield manager.app


@pytest_asyncio.fixture
async def client(app):
    async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://api",
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_register(client, random_credentials, emails):
    response = await client.post("/users/register", json=random_credentials)
    assert_register_ok(response)
    await assert_only_one_email_sent(emails)


@pytest.mark.asyncio
async def test_register_already_registered(client, random_credentials, emails):
    response_1 = await client.post("/users/register", json=random_credentials)
    assert_register_ok(response_1)
    await assert_only_one_email_sent(emails)

    response_2 = await client.post("/users/register", json=random_credentials)
    assert_register_ko_already_registered(response_2)
    await assert_only_one_email_sent(emails)


@pytest.mark.asyncio
async def test_activate(client, random_credentials, random_auth, emails):
    response_register = await client.post(
        "/users/register",
        json=random_credentials,
    )
    assert_register_ok(response_register)
    await assert_only_one_email_sent(emails)

    verification_code = await get_code_from_last_email()

    response_activate = await client.patch(
        "/users/activate",
        json={"verification_code": verification_code},
        auth=random_auth,
    )
    assert_activate_ok(response_activate)


@pytest.mark.asyncio
async def test_activate_invalid_credentials(
        client, random_credentials, random_auth, emails
):
    response_register = await client.post(
        "/users/register",
        json=random_credentials,
    )
    assert_register_ok(response_register)
    await assert_only_one_email_sent(emails)

    verification_code = await get_code_from_last_email()

    response_activate = await client.patch(
        "/users/activate",
        json={"verification_code": verification_code},
        auth=("invalid", "credentials"),
    )
    assert_activate_ko_invalid_credentials(response_activate)


@pytest.mark.asyncio
async def test_activate_already_activated(
        client, random_credentials, random_auth, emails
):
    response_register = await client.post(
        "/users/register",
        json=random_credentials,
    )
    assert_register_ok(response_register)
    await assert_only_one_email_sent(emails)

    verification_code = await get_code_from_last_email()

    response_activate_1 = await client.patch(
        "/users/activate",
        json={"verification_code": verification_code},
        auth=random_auth,
    )
    assert_activate_ok(response_activate_1)

    response_activate_2 = await client.patch(
        "/users/activate",
        json={"verification_code": verification_code},
        auth=random_auth,
    )
    assert_activate_ko_already_activated(response_activate_2)


@pytest.mark.asyncio
async def test_activate_invalid_verification_code(
        client, random_credentials, random_auth, emails
):
    response_register = await client.post(
        "/users/register",
        json=random_credentials,
    )
    assert_register_ok(response_register)
    await assert_only_one_email_sent(emails)

    verification_code = await get_code_from_last_email()

    invalid_code = verification_code
    while invalid_code == verification_code:
        invalid_code = generate_4_digits()

    response_activate_1 = await client.patch(
        "/users/activate",
        json={"verification_code": invalid_code},
        auth=random_auth,
    )
    assert_activate_ko_invalid_verification_code(response_activate_1)


@pytest.mark.skip(reason="further implementation")
@pytest.mark.asyncio
async def test_activate_expired_verification_code(
        client, random_credentials, random_auth, emails
):
    response_register = await client.post(
        "/users/register",
        json=random_credentials,
    )
    assert_register_ok(response_register)
    await assert_only_one_email_sent(emails)

    verification_code = await get_code_from_last_email()

    # TODO: update code created_at to past

    response_activate = await client.patch(
        "/users/activate",
        json={"verification_code": verification_code},
        auth=random_auth,
    )
    assert_activate_ko_expired_verification_code(response_activate)
