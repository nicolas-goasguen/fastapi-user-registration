from unittest.mock import patch, ANY

import pytest

from src.auth.dependencies import get_current_user
from src.auth.utils import verify_password
from src.user.exceptions import (
    UserAlreadyRegisteredError,
    UserAlreadyActivatedError,
    UserVerificationCodeInvalidError,
)
from src.user.schemas import UserPublic
from src.user.service import logger as service_logger
from src.user.service import register_user, activate_user
from src.user.tests.assertions import assert_warning_logged
from src.user.tests.conftest import (
    fake_router_inactive_user,
    fake_router_active_user,
    fake_router_user_register,
)
from src.user.utils import is_valid_verification_code


@patch("src.user.service.send_verification_email.delay")
@patch("src.user.service.user_crud.create_user_verification")
@patch("src.user.service.user_crud.create_user")
@patch("src.user.service.user_crud.get_user_by_email")
@pytest.mark.asyncio
async def test_register_success(
    mock_crud_get_user_by_email,
    mock_crud_create_user,
    mock_crud_create_user_verification,
    mock_task_send_verification_email,
    mock_db,
    fake_user_password,
    fake_crud_inactive_user,
    fake_crud_verification,
    fake_router_user_register,
    fake_router_inactive_user,
):
    fake_crud_user = fake_crud_inactive_user

    mock_crud_get_user_by_email.return_value = None
    mock_crud_create_user.return_value = fake_crud_user
    mock_crud_create_user_verification.return_value = fake_crud_verification

    user = await register_user(
        db=mock_db,
        user_in=fake_router_user_register,
    )

    # mock: crud doesn't find an already registered user
    mock_crud_get_user_by_email.assert_called_once_with(
        mock_db,
        fake_crud_user.email,
    )

    # mock: crud creates a new user
    mock_crud_create_user.assert_called_once_with(
        mock_db,
        fake_crud_user.email,
        ANY,
    )
    (_, _, created_hashed_pwd), _ = mock_crud_create_user.call_args
    assert verify_password(fake_user_password, created_hashed_pwd)

    # mock: crud creates a new user verification
    mock_crud_create_user_verification.assert_called_once_with(
        mock_db,
        fake_crud_user.id,
        ANY,
    )
    (_, _, created_code), _ = mock_crud_create_user_verification.call_args
    assert is_valid_verification_code(created_code)

    # mock: service sends a new email task
    mock_task_send_verification_email.assert_called_once_with(
        fake_crud_user.email,
        fake_crud_verification.code,
    )

    # mock: service returns a correct inactive UserPublic object
    assert isinstance(user, UserPublic)
    assert user.model_dump() == fake_router_inactive_user.model_dump()


@patch("src.user.service.user_crud.get_user_by_email")
@pytest.mark.asyncio
async def test_register_failure_already_registered(
    mock_crud_get_user_by_email,
    mock_db,
    fake_crud_inactive_user,
    fake_router_user_register,
):
    mock_crud_get_user_by_email.return_value = fake_crud_inactive_user

    with pytest.raises(UserAlreadyRegisteredError):
        await register_user(db=mock_db, user_in=fake_router_user_register)


@patch("src.user.service.send_verification_email.delay")
@patch("src.user.service.user_crud.create_user_verification")
@patch("src.user.service.user_crud.create_user")
@patch("src.user.service.user_crud.get_user_by_email")
@pytest.mark.asyncio
async def test_register_failure_email_task_error(
    mock_crud_get_user_by_email,
    mock_crud_create_user,
    mock_crud_create_user_verification,
    mock_task_send_verification_email,
    mock_db,
    fake_user_password,
    fake_crud_inactive_user,
    fake_crud_verification,
    fake_router_user_register,
    fake_router_inactive_user,
    caplog,
):
    mock_crud_get_user_by_email.return_value = None
    mock_crud_create_user.return_value = fake_crud_inactive_user
    mock_crud_create_user_verification.return_value = fake_crud_verification
    mock_task_send_verification_email.side_effect = Exception("fail")

    await register_user(
        db=mock_db,
        user_in=fake_router_user_register,
    )

    assert_warning_logged(
        caplog, "Failed to enqueue verification email", service_logger.name
    )


@patch("src.user.service.send_confirmation_email.delay")
@patch("src.user.service.user_crud.update_user_is_active")
@patch("src.user.service.user_crud.get_valid_user_verification")
@pytest.mark.asyncio
async def test_activate_success(
    mock_crud_get_valid_user_verification,
    mock_crud_update_user_is_active,
    mock_task_send_confirmation_email,
    app,
    mock_db,
    fake_user_password,
    fake_crud_inactive_user,
    fake_crud_active_user,
    fake_crud_verification,
    fake_router_active_user,
    fake_router_verification_activate,
):
    fake_crud_user = fake_crud_inactive_user
    app.dependency_overrides[get_current_user] = lambda: fake_crud_user

    mock_crud_get_valid_user_verification.return_value = fake_crud_verification
    mock_crud_update_user_is_active.return_value = fake_crud_active_user

    user = await activate_user(
        db=mock_db,
        user=fake_crud_user,
        verification_in=fake_router_verification_activate,
    )

    # mock: crud finds a valid user validation
    mock_crud_get_valid_user_verification.assert_called_once_with(
        mock_db,
        fake_crud_user.id,
        ANY,
    )
    (_, _, created_code), _ = mock_crud_get_valid_user_verification.call_args
    assert is_valid_verification_code(created_code)

    # mock: crud updates is_active on current user
    mock_crud_update_user_is_active.assert_called_once_with(
        mock_db,
        fake_crud_user.id,
        is_active=True,
    )

    # mock: service sends a new email task
    mock_task_send_confirmation_email.assert_called_once_with(
        fake_crud_inactive_user.email
    )

    # mock: service returns a correct active UserPublic object
    assert isinstance(user, UserPublic)
    assert user.model_dump() == fake_router_active_user.model_dump()


@pytest.mark.asyncio
async def test_activate_failure_already_activated(
    app,
    mock_db,
    fake_crud_active_user,
    fake_router_verification_activate,
):
    fake_crud_user = fake_crud_active_user
    app.dependency_overrides[get_current_user] = lambda: fake_crud_user

    with pytest.raises(UserAlreadyActivatedError):
        await activate_user(
            db=mock_db,
            user=fake_crud_user,
            verification_in=fake_router_verification_activate,
        )


@patch("src.user.service.send_confirmation_email.delay")
@patch("src.user.service.user_crud.update_user_is_active")
@patch("src.user.service.user_crud.get_valid_user_verification")
@pytest.mark.asyncio
async def test_activate_failure_verification_not_found(
    mock_crud_get_valid_user_verification,
    app,
    mock_db,
    fake_crud_inactive_user,
    fake_router_verification_activate,
):
    fake_crud_user = fake_crud_inactive_user
    app.dependency_overrides[get_current_user] = lambda: fake_crud_user

    mock_crud_get_valid_user_verification.return_value = None

    with pytest.raises(UserVerificationCodeInvalidError):
        await activate_user(
            db=mock_db,
            user=fake_crud_user,
            verification_in=fake_router_verification_activate,
        )


@patch("src.user.service.send_confirmation_email.delay")
@patch("src.user.service.user_crud.update_user_is_active")
@patch("src.user.service.user_crud.get_valid_user_verification")
@pytest.mark.asyncio
async def test_activate_failure_verification_expired(
    mock_crud_get_valid_user_verification,
    mock_crud_update_user_is_active,
    app,
    mock_db,
    fake_crud_inactive_user,
    fake_crud_active_user,
    fake_crud_expired_verification,
    fake_router_verification_activate,
):
    fake_crud_user = fake_crud_inactive_user
    app.dependency_overrides[get_current_user] = lambda: fake_crud_user

    mock_crud_get_valid_user_verification.return_value = fake_crud_expired_verification
    mock_crud_update_user_is_active.return_value = fake_crud_active_user

    with pytest.raises(UserVerificationCodeInvalidError):
        await activate_user(
            db=mock_db,
            user=fake_crud_user,
            verification_in=fake_router_verification_activate,
        )


@patch("src.user.service.send_confirmation_email.delay")
@patch("src.user.service.user_crud.update_user_is_active")
@patch("src.user.service.user_crud.get_valid_user_verification")
@pytest.mark.asyncio
async def test_activate_failure_email_task_error(
    mock_crud_get_valid_user_verification,
    mock_crud_update_user_is_active,
    mock_task_send_verification_email,
    app,
    mock_db,
    fake_crud_inactive_user,
    fake_crud_active_user,
    fake_crud_verification,
    fake_router_verification_activate,
    fake_router_active_user,
    caplog,
):
    fake_crud_user = fake_crud_inactive_user
    app.dependency_overrides[get_current_user] = lambda: fake_crud_user

    mock_crud_get_valid_user_verification.return_value = fake_crud_verification
    mock_crud_update_user_is_active.return_value = fake_crud_active_user
    mock_task_send_verification_email.side_effect = Exception()

    await activate_user(
        db=mock_db,
        user=fake_crud_user,
        verification_in=fake_router_verification_activate,
    )

    assert_warning_logged(
        caplog, "Failed to enqueue confirmation email", service_logger.name
    )
