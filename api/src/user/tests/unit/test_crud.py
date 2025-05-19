from datetime import datetime
from unittest.mock import AsyncMock, ANY

import pytest
from pydantic import ValidationError

from src.exceptions import DBBaseError
from src.user import crud
from src.user.exceptions import (
    UserCrudUpdateIsActiveError,
    UserCrudInsertError,
    UserVerificationCrudInsertError,
)
from src.user.schemas import UserFromDB, UserVerificationFromDB
from src.user.tests.mocks.db import (
    side_effect_db_create_user,
    return_value_db_user,
    side_effect_db_create_user_verification,
    return_value_db_user_verification,
)
from src.user.tests.unit.assertions import (
    assert_value_error_verification_code,
    assert_value_error_password_hash_invalid,
    assert_value_error_password_hash_empty,
)

DEFAULT_ID = 1
DEFAULT_EMAIL = "test@example.com"
DEFAULT_PWD = "123Password?!"
DEFAULT_PWD_HASH = "$2b$12$q1jZc9H7jm36Eu9TRn0uB.3Bmch9JasnMfhUD8IqdQsUR01afrWDm"
DEFAULT_CODE = "1234"

DEFAULT_INACTIVE_USER = return_value_db_user(
    email=DEFAULT_EMAIL,
    password_hash=DEFAULT_PWD_HASH,
    is_active=False,
)
DEFAULT_ACTIVE_USER = return_value_db_user(
    email=DEFAULT_EMAIL,
    password_hash=DEFAULT_PWD_HASH,
    is_active=True,
)

DEFAULT_USER_VERIFICATION = return_value_db_user_verification(
    user_id=DEFAULT_ID,
    code=DEFAULT_CODE,
)
DEFAULT_EXPECTED_USER_VERIFICATION = return_value_db_user_verification(
    id_=ANY,
    user_id=DEFAULT_ID,
    code=DEFAULT_CODE,
    created_at=ANY,
)


@pytest.mark.asyncio
async def test_create_user_success():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user

    user = await crud.create_user(mock_db, DEFAULT_EMAIL, DEFAULT_PWD_HASH)

    assert isinstance(user, UserFromDB)
    assert user.model_dump() == DEFAULT_INACTIVE_USER


@pytest.mark.asyncio
async def test_create_user_failure_db_error():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = Exception()

    with pytest.raises(DBBaseError):
        await crud.create_user(mock_db, DEFAULT_EMAIL, DEFAULT_PWD_HASH)


@pytest.mark.asyncio
async def test_create_user_failure_not_created():
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = None

    with pytest.raises(UserCrudInsertError):
        await crud.create_user(mock_db, DEFAULT_EMAIL, DEFAULT_PWD_HASH)


@pytest.mark.asyncio
async def test_create_user_failure_email_empty():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user

    with pytest.raises(ValidationError) as e:
        await crud.create_user(mock_db, "", DEFAULT_PWD_HASH)

    assert len(e.value.errors()) == 1
    error = e.value.errors()[0]
    assert error["loc"] == ("email",)
    assert "value is not a valid email address" in error["msg"]


@pytest.mark.asyncio
async def test_create_user_failure_password_hash_empty():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user

    with pytest.raises(ValidationError) as e:
        await crud.create_user(mock_db, DEFAULT_EMAIL, "")

    assert_value_error_password_hash_empty(e.value.errors())


async def test_create_user_failure_password_hash_invalid():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user

    with pytest.raises(ValidationError) as e:
        await crud.create_user(
            mock_db,
            DEFAULT_EMAIL,
            "b12$q1jZc9H7jm36Eu9TRn0uB.3Bmch9JasnMfhUD8IqdQsUR01afrWDm",
        )

    assert_value_error_password_hash_invalid(e.value.errors())


async def test_create_user_failure_password_hash_too_short():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user

    with pytest.raises(ValidationError) as e:
        await crud.create_user(
            mock_db,
            DEFAULT_EMAIL,
            "$2b$12$q1jZc9H7jm36Eu9TRn0uB",
        )

    assert_value_error_password_hash_invalid(e.value.errors())


@pytest.mark.asyncio
async def test_get_user_by_email_success():
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = DEFAULT_INACTIVE_USER

    user = await crud.get_user_by_email(mock_db, DEFAULT_EMAIL)

    assert isinstance(user, UserFromDB)
    assert user.model_dump() == DEFAULT_INACTIVE_USER


@pytest.mark.asyncio
async def test_get_user_by_email_failure_db_error():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = Exception()

    with pytest.raises(DBBaseError):
        await crud.get_user_by_email(mock_db, DEFAULT_EMAIL)


@pytest.mark.asyncio
async def test_get_user_by_email_failure_not_found():
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = None

    user = await crud.get_user_by_email(mock_db, DEFAULT_EMAIL)

    assert user is None


@pytest.mark.asyncio
async def test_update_user_is_active_success():
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = DEFAULT_ACTIVE_USER

    user = await crud.update_user_is_active(mock_db, DEFAULT_ID, True)

    assert isinstance(user, UserFromDB)
    assert user.model_dump() == DEFAULT_ACTIVE_USER


@pytest.mark.asyncio
async def test_update_user_is_active_failure_db_error():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = Exception()

    with pytest.raises(DBBaseError):
        await crud.update_user_is_active(mock_db, DEFAULT_ID, True)


@pytest.mark.asyncio
async def test_update_user_is_active_failure_not_updated():
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = None

    with pytest.raises(UserCrudUpdateIsActiveError):
        await crud.update_user_is_active(mock_db, DEFAULT_ID, True)


@pytest.mark.asyncio
async def test_create_user_verification_success():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user_verification

    datetime_before = datetime.now()
    verification = await crud.create_user_verification(
        mock_db, DEFAULT_ID, DEFAULT_CODE
    )
    datetime_after = datetime.now()

    assert isinstance(verification, UserVerificationFromDB)
    assert verification.model_dump() == DEFAULT_EXPECTED_USER_VERIFICATION
    assert datetime_before < verification.created_at < datetime_after


@pytest.mark.asyncio
async def test_create_user_verification_failure_db_error():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = Exception()

    with pytest.raises(DBBaseError):
        await crud.create_user_verification(mock_db, DEFAULT_ID, DEFAULT_CODE)


@pytest.mark.asyncio
async def test_create_user_verification_failure_not_created():
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = None

    with pytest.raises(UserVerificationCrudInsertError):
        await crud.create_user_verification(mock_db, DEFAULT_ID, DEFAULT_CODE)


@pytest.mark.asyncio
async def test_create_user_verification_failure_code_empty():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user_verification

    with pytest.raises(ValidationError) as e:
        await crud.create_user_verification(mock_db, DEFAULT_ID, "")

    assert_value_error_verification_code(e.value.errors())


@pytest.mark.asyncio
async def test_create_user_verification_failure_code_too_short():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user_verification

    with pytest.raises(ValidationError) as e:
        await crud.create_user_verification(mock_db, DEFAULT_ID, "12")

    assert_value_error_verification_code(e.value.errors())


@pytest.mark.asyncio
async def test_create_user_verification_failure_code_too_long():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user_verification

    with pytest.raises(ValidationError) as e:
        await crud.create_user_verification(mock_db, DEFAULT_ID, "12345")

    assert_value_error_verification_code(e.value.errors())


@pytest.mark.asyncio
async def test_create_user_verification_failure_code_contains_letter():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user_verification

    with pytest.raises(ValidationError) as e:
        await crud.create_user_verification(mock_db, DEFAULT_ID, "1ab2")

    assert_value_error_verification_code(e.value.errors())


@pytest.mark.asyncio
async def test_get_valid_user_verification_success():
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = DEFAULT_USER_VERIFICATION

    verification = await crud.get_valid_user_verification(
        mock_db, DEFAULT_ID, DEFAULT_CODE
    )

    assert isinstance(verification, UserVerificationFromDB)
    assert verification.model_dump() == DEFAULT_USER_VERIFICATION


@pytest.mark.asyncio
async def test_get_valid_user_verification_failure_db_error():
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = Exception()

    with pytest.raises(DBBaseError):
        await crud.get_valid_user_verification(mock_db, DEFAULT_ID, DEFAULT_CODE)


@pytest.mark.asyncio
async def test_get_valid_user_verification_failure_not_found():
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = None

    verification = await crud.get_valid_user_verification(
        mock_db, DEFAULT_ID, DEFAULT_CODE
    )

    assert verification is None
