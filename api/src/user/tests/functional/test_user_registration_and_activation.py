from unittest.mock import patch

import databases.core
import pytest

from src.auth.dependencies import get_current_user
from src.auth.utils import verify_password
from src.user.tests.assertions import assert_register_ok, assert_activate_ok
from src.user.tests.mocks.crud import (
    side_effect_crud_create_user,
    side_effect_crud_create_verification,
)
from src.user.tests.utils import activate_user, register_user
from src.user.utils import is_valid_verification_code


@patch("src.user.service.send_confirmation_email.delay")
@patch("src.user.service.user_crud.update_user_is_active")
@patch("src.user.service.user_crud.get_valid_user_verification")
@patch("src.user.service.send_verification_email.delay")
@patch("src.user.service.user_crud.create_user_verification")
@patch("src.user.service.user_crud.create_user")
@pytest.mark.asyncio
async def test_user_register_and_activate(
    mock_create_user,
    mock_create_user_verification,
    mock_send_verification_email,
    mock_get_valid_user_verification,
    mock_update_user_is_active,
    mock_send_confirmation_email,
    app,
    client,
    fake_inactive_user,
    fake_active_user,
    fake_user_password,
    fake_user_verification,
):
    # ---------------
    # Registration
    # ---------------
    mock_create_user.side_effect = side_effect_crud_create_user
    mock_create_user_verification.side_effect = side_effect_crud_create_verification

    register_response = await register_user(
        client,
        fake_inactive_user.email,
        fake_user_password,
    )
    assert_register_ok(register_response)

    # Check: User creation call
    mock_create_user.assert_called_once()
    crud_args, _ = mock_create_user.call_args
    assert len(crud_args) == 3
    assert type(crud_args[0]) == databases.core.Database
    assert crud_args[1] == fake_inactive_user.email
    assert verify_password(fake_user_password, crud_args[2])

    # Check: User verification creation call
    mock_create_user_verification.assert_called_once()
    crud_verif_args, _ = mock_create_user_verification.call_args
    assert len(crud_verif_args) == 3
    assert type(crud_verif_args[0]) == databases.core.Database
    assert crud_verif_args[1] == fake_inactive_user.id
    created_verification_code = crud_verif_args[2]  # value will be ignored by the mock
    assert is_valid_verification_code(created_verification_code)

    # Check: Mailing task call
    mock_send_verification_email.assert_called_once_with(
        fake_inactive_user.email,
        created_verification_code,  # email is sent with the new code that will be ignored next
    )

    # ---------------
    # Activation
    # ---------------

    app.dependency_overrides[get_current_user] = lambda: fake_inactive_user

    mock_get_valid_user_verification.return_value = fake_user_verification
    mock_update_user_is_active.return_value = fake_active_user

    activate_response = await activate_user(
        client,
        fake_inactive_user.email,
        fake_user_password,
        fake_user_verification.code,
    )
    assert_activate_ok(activate_response)

    # Check: Search a valid verification record
    mock_get_valid_user_verification.assert_called_once()
    verif_args, _ = mock_get_valid_user_verification.call_args
    assert len(verif_args) == 3
    assert type(verif_args[0]) == databases.core.Database
    assert verif_args[1] == fake_active_user.id
    assert verif_args[2] == fake_user_verification.code
    assert is_valid_verification_code(verif_args[2])

    # Check: Valid update on is_active
    mock_update_user_is_active.assert_called_once()
    update_args, update_kwargs = mock_update_user_is_active.call_args
    assert len(update_args) == 2
    assert len(update_kwargs) == 1
    assert type(update_args[0]) == databases.core.Database
    assert update_args[1] == fake_active_user.id
    assert update_kwargs == {"is_active": True}

    # Check: Mailing task call
    mock_send_confirmation_email.assert_called_once_with(fake_inactive_user.email)
