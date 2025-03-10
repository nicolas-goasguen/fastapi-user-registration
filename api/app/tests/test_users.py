import pytest

from app.core.utils import generate_4_digits
from app.tests.assertions import (
    assert_register_ok,
    assert_register_ko_already_registered,
    assert_activate_ok,
    assert_activate_ko_invalid_credentials,
    assert_activate_ko_already_activated,
    assert_activate_ko_invalid_verification_code,
    assert_activate_ko_expired_verification_code,
    assert_only_one_correct_mail_sent,
)
from app.tests.tools import expire_verification_code


@pytest.mark.asyncio
async def test_register(
        register_user,  # this called as a fixture triggers registration
):
    pass


@pytest.mark.asyncio
async def test_register_already_registered(
        client,
        register_user,
        random_credentials,
        verification_data,
        emails_before,
):
    response = await client.post("/users/register", json=random_credentials)
    assert_register_ko_already_registered(response)
    await assert_only_one_correct_mail_sent(
        random_credentials, verification_data, emails_before
    )


@pytest.mark.asyncio
async def test_activate(
        client,
        activate_user,  # this called as a fixture triggers activation
        random_credentials,
        random_auth,
):
    pass


@pytest.mark.asyncio
async def test_activate_invalid_credentials(
        client,
        register_user,
        random_credentials,
        verification_data,
        random_auth,
):
    response = await client.patch(
        "/users/activate",
        json={"verification_code": verification_data["code"]},
        auth=("invalid", "credentials"),
    )
    assert_activate_ko_invalid_credentials(response)


@pytest.mark.asyncio
async def test_activate_already_activated(
        client,
        activate_user,
        verification_data,
        random_auth,
):
    response = await client.patch(
        "/users/activate",
        json={"verification_code": verification_data["code"]},
        auth=random_auth,
    )
    assert_activate_ko_already_activated(response)


@pytest.mark.asyncio
async def test_activate_invalid_verification_code(
        client,
        register_user,
        verification_data,
        random_auth,
):
    invalid_code = verification_data["code"]
    while invalid_code == verification_data["code"]:
        invalid_code = generate_4_digits()

    response = await client.patch(
        "/users/activate",
        json={"verification_code": invalid_code},
        auth=random_auth,
    )
    assert_activate_ko_invalid_verification_code(response)


@pytest.mark.asyncio
async def test_activate_expired_verification_code(
        client,
        register_user,
        verification_data,
        random_credentials,
        random_auth,
):
    await expire_verification_code(verification_data)

    response = await client.patch(
        "/users/activate",
        json={"verification_code": verification_data["code"]},
        auth=random_auth,
    )
    assert_activate_ko_expired_verification_code(response)
