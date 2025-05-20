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
from src.user.tests.conftest import (
    fake_user_email,
    fake_crud_verification,
    fake_expect_verification,
)
from src.user.tests.mocks.db import (
    side_effect_db_create_user,
    side_effect_db_create_user_verification,
)
from src.user.tests.unit.assertions import (
    assert_value_error_verification_code,
    assert_value_error_password_hash_invalid,
    assert_value_error_password_hash_empty,
    assert_value_error_email_invalid,
)


@pytest.mark.asyncio
async def test_create_user_success(
    fake_user_email,
    fake_user_password_hash,
    fake_db_inactive_user,
    fake_crud_inactive_user,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = fake_db_inactive_user

    user = await crud.create_user(
        mock_db,
        fake_user_email,
        fake_user_password_hash,
    )

    mock_db.fetch_one.assert_called_once_with(
        ANY,
        {"email": fake_user_email, "password_hash": fake_user_password_hash},
    )
    assert isinstance(user, UserFromDB)
    assert user.model_dump() == fake_crud_inactive_user.model_dump()


@pytest.mark.asyncio
async def test_create_user_failure_db_error(
    fake_user_email,
    fake_user_password_hash,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = Exception()

    with pytest.raises(DBBaseError):
        await crud.create_user(mock_db, fake_user_email, fake_user_password_hash)


@pytest.mark.asyncio
async def test_create_user_failure_not_created(
    fake_user_email,
    fake_user_password_hash,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = None

    with pytest.raises(UserCrudInsertError):
        await crud.create_user(mock_db, fake_user_email, fake_user_password_hash)


@pytest.mark.asyncio
async def test_create_user_failure_email_empty(
    fake_user_password_hash,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user

    with pytest.raises(ValidationError) as e:
        await crud.create_user(mock_db, "", fake_user_password_hash)

    assert_value_error_email_invalid(e.value.errors())


@pytest.mark.asyncio
async def test_create_user_failure_email_invalid(
    fake_user_password_hash,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user

    with pytest.raises(ValidationError) as e:
        await crud.create_user(mock_db, "test.com", fake_user_password_hash)

    assert_value_error_email_invalid(e.value.errors())


@pytest.mark.asyncio
async def test_create_user_failure_password_hash_empty(
    fake_user_email,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user

    with pytest.raises(ValidationError) as e:
        await crud.create_user(mock_db, fake_user_email, "")

    assert_value_error_password_hash_empty(e.value.errors())


async def test_create_user_failure_password_hash_invalid(
    fake_user_email,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user

    with pytest.raises(ValidationError) as e:
        await crud.create_user(
            mock_db,
            fake_user_email,
            "b12$q1jZc9H7jm36Eu9TRn0uB.3Bmch9JasnMfhUD8IqdQsUR01afrWDm",
        )

    assert_value_error_password_hash_invalid(e.value.errors())


async def test_create_user_failure_password_hash_too_short(
    fake_user_email,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user

    with pytest.raises(ValidationError) as e:
        await crud.create_user(
            mock_db,
            fake_user_email,
            "$2b$12$q1jZc9H7jm36Eu9TRn0uB",
        )

    assert_value_error_password_hash_invalid(e.value.errors())


@pytest.mark.asyncio
async def test_get_user_by_email_success(
    fake_user_email,
    fake_db_inactive_user,
    fake_crud_inactive_user,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = fake_db_inactive_user

    user = await crud.get_user_by_email(mock_db, fake_user_email)

    mock_db.fetch_one.assert_called_once_with(
        ANY,
        {"email": fake_user_email},
    )
    assert isinstance(user, UserFromDB)
    assert user.model_dump() == fake_crud_inactive_user.model_dump()


@pytest.mark.asyncio
async def test_get_user_by_email_failure_db_error(
    fake_user_email,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = Exception()

    with pytest.raises(DBBaseError):
        await crud.get_user_by_email(mock_db, fake_user_email)


@pytest.mark.asyncio
async def test_get_user_by_email_failure_not_found(
    fake_user_email,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = None

    user = await crud.get_user_by_email(mock_db, fake_user_email)

    mock_db.fetch_one.assert_called_once_with(
        ANY,
        {"email": fake_user_email},
    )
    assert user is None


@pytest.mark.asyncio
async def test_update_user_is_active_success(
    fake_user_id,
    fake_db_active_user,
    fake_crud_active_user,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = fake_db_active_user

    user = await crud.update_user_is_active(mock_db, fake_user_id, True)

    mock_db.fetch_one.assert_called_once_with(
        ANY,
        {"user_id": fake_user_id, "is_active": True},
    )
    assert isinstance(user, UserFromDB)
    assert user.model_dump() == fake_crud_active_user.model_dump()


@pytest.mark.asyncio
async def test_update_user_is_active_failure_db_error(
    fake_user_id,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = Exception()

    with pytest.raises(DBBaseError):
        await crud.update_user_is_active(mock_db, fake_user_id, True)


@pytest.mark.asyncio
async def test_update_user_is_active_failure_not_updated(
    fake_user_id,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = None

    with pytest.raises(UserCrudUpdateIsActiveError):
        await crud.update_user_is_active(mock_db, fake_user_id, True)


@pytest.mark.asyncio
async def test_create_user_verification_success(
    fake_user_id,
    fake_verification_id,
    fake_verification_code,
    fake_expect_verification,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user_verification

    datetime_before = datetime.now()
    verification = await crud.create_user_verification(
        mock_db, fake_user_id, fake_verification_code
    )
    datetime_after = datetime.now()

    mock_db.fetch_one.assert_called_once_with(
        ANY,
        {"user_id": fake_user_id, "code": fake_verification_code},
    )
    assert isinstance(verification, UserVerificationFromDB)
    assert verification.model_dump() == fake_expect_verification
    assert datetime_before < verification.created_at < datetime_after


@pytest.mark.asyncio
async def test_create_user_verification_failure_db_error(
    fake_user_id,
    fake_verification_code,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = Exception()

    with pytest.raises(DBBaseError):
        await crud.create_user_verification(
            mock_db,
            fake_user_id,
            fake_verification_code,
        )


@pytest.mark.asyncio
async def test_create_user_verification_failure_not_created(
    fake_user_id,
    fake_verification_code,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = None

    with pytest.raises(UserVerificationCrudInsertError):
        await crud.create_user_verification(
            mock_db,
            fake_user_id,
            fake_verification_code,
        )


@pytest.mark.asyncio
async def test_create_user_verification_failure_code_empty(
    fake_user_id,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user_verification

    with pytest.raises(ValidationError) as e:
        await crud.create_user_verification(mock_db, fake_user_id, "")

    assert_value_error_verification_code(e.value.errors())


@pytest.mark.asyncio
async def test_create_user_verification_failure_code_too_short(
    fake_user_id,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user_verification

    with pytest.raises(ValidationError) as e:
        await crud.create_user_verification(mock_db, fake_user_id, "12")

    assert_value_error_verification_code(e.value.errors())


@pytest.mark.asyncio
async def test_create_user_verification_failure_code_too_long(
    fake_user_id,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user_verification

    with pytest.raises(ValidationError) as e:
        await crud.create_user_verification(mock_db, fake_user_id, "12345")

    assert_value_error_verification_code(e.value.errors())


@pytest.mark.asyncio
async def test_create_user_verification_failure_code_contains_letter(
    fake_user_id,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = side_effect_db_create_user_verification

    with pytest.raises(ValidationError) as e:
        await crud.create_user_verification(mock_db, fake_user_id, "1ab2")

    assert_value_error_verification_code(e.value.errors())


@pytest.mark.asyncio
async def test_get_valid_user_verification_success(
    fake_user_id,
    fake_verification_code,
    fake_db_verification,
    fake_crud_verification,
    fake_expect_verification,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = fake_db_verification

    verification = await crud.get_valid_user_verification(
        mock_db, fake_user_id, fake_verification_code
    )

    mock_db.fetch_one.assert_called_once_with(
        ANY,
        {"user_id": fake_user_id, "code": fake_verification_code},
    )
    assert isinstance(verification, UserVerificationFromDB)
    assert verification.model_dump() == fake_expect_verification


@pytest.mark.asyncio
async def test_get_valid_user_verification_failure_db_error(
    fake_user_id,
    fake_verification_code,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.side_effect = Exception()

    with pytest.raises(DBBaseError):
        await crud.get_valid_user_verification(
            mock_db,
            fake_user_id,
            fake_verification_code,
        )


@pytest.mark.asyncio
async def test_get_valid_user_verification_failure_not_found(
    fake_user_id,
    fake_verification_code,
):
    mock_db = AsyncMock()
    mock_db.fetch_one.return_value = None

    verification = await crud.get_valid_user_verification(
        mock_db,
        fake_user_id,
        fake_verification_code,
    )

    mock_db.fetch_one.assert_called_once_with(
        ANY,
        {"user_id": fake_user_id, "code": fake_verification_code},
    )
    assert verification is None
