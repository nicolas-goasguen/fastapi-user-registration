from datetime import datetime, timedelta
from unittest.mock import ANY

import pytest

from src.user.schemas import (
    UserFromDB,
    UserVerificationFromDB,
    UserPublic,
    UserRegister,
    UserVerificationActivate,
)


@pytest.fixture
def fake_user_id():
    return 1


@pytest.fixture
def fake_user_email():
    return "test@example.com"


@pytest.fixture
def fake_user_password():
    return "Password123!?"


@pytest.fixture
def fake_user_password_hash(
    fake_user_password,
):
    return "$2b$12$q1jZc9H7jm36Eu9TRn0uB.3Bmch9JasnMfhUD8IqdQsUR01afrWDm"


@pytest.fixture
def fake_db_inactive_user(
    fake_user_id,
    fake_user_email,
    fake_user_password_hash,
):
    return {
        "id": fake_user_id,
        "email": fake_user_email,
        "password_hash": fake_user_password_hash,
        "is_active": False,
    }


@pytest.fixture
def fake_db_active_user(
    fake_user_id,
    fake_user_email,
    fake_user_password_hash,
):
    return {
        "id": fake_user_id,
        "email": fake_user_email,
        "password_hash": fake_user_password_hash,
        "is_active": True,
    }


@pytest.fixture
def fake_crud_inactive_user(
    fake_user_id,
    fake_user_email,
    fake_user_password_hash,
):
    return UserFromDB(
        id=fake_user_id,
        email=fake_user_email,
        password_hash=fake_user_password_hash,
        is_active=False,
    )


@pytest.fixture
def fake_crud_active_user(
    fake_user_id,
    fake_user_email,
    fake_user_password_hash,
):
    return UserFromDB(
        id=fake_user_id,
        email=fake_user_email,
        password_hash=fake_user_password_hash,
        is_active=True,
    )


@pytest.fixture
def fake_router_inactive_user(
    fake_user_id,
    fake_user_email,
    fake_user_password_hash,
):
    return UserPublic(
        id=fake_user_id,
        email=fake_user_email,
        is_active=False,
    )


@pytest.fixture
def fake_router_active_user(
    fake_user_id,
    fake_user_email,
    fake_user_password_hash,
):
    return UserPublic(
        id=fake_user_id,
        email=fake_user_email,
        is_active=True,
    )


@pytest.fixture
def fake_router_user_register(
    fake_user_email,
    fake_user_password,
):
    return UserRegister(
        email=fake_user_email,
        password=fake_user_password,
    )


@pytest.fixture
def fake_verification_id():
    return 1


@pytest.fixture
def fake_verification_code():
    return "1234"


@pytest.fixture
def fake_db_verification(
    fake_verification_id,
    fake_verification_code,
    fake_user_id,
):
    return {
        "id": fake_verification_id,
        "user_id": fake_user_id,
        "code": fake_verification_code,
        "created_at": datetime.now(),
    }


@pytest.fixture
def fake_crud_verification(
    fake_verification_id,
    fake_verification_code,
    fake_user_id,
):
    return UserVerificationFromDB(
        id=fake_verification_id,
        user_id=fake_user_id,
        code=fake_verification_code,
        created_at=datetime.now(),
    )


@pytest.fixture
def fake_crud_expired_verification(
    fake_verification_id,
    fake_verification_code,
    fake_user_id,
):
    return UserVerificationFromDB(
        id=fake_verification_id,
        user_id=fake_user_id,
        code=fake_verification_code,
        created_at=datetime.now() - timedelta(minutes=1, seconds=1),
    )


@pytest.fixture
def fake_router_verification_activate(fake_verification_code):
    return UserVerificationActivate(
        code=fake_verification_code,
    )


@pytest.fixture
def fake_expect_verification(
    fake_verification_id,
    fake_verification_code,
    fake_user_id,
):
    return {
        "id": fake_verification_id,
        "user_id": fake_user_id,
        "code": fake_verification_code,
        "created_at": ANY,
    }
