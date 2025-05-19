import pytest

from src.auth.utils import hash_password, verify_password

DEFAULT_PASSWORD = "123Password?!"
ANOTHER_PASSWORD = "!?Another*$PassWord"


@pytest.mark.parametrize("password", [DEFAULT_PASSWORD, ANOTHER_PASSWORD])
def test_hash_and_verify_password_success(password):
    hashed_1 = hash_password(password)
    hashed_2 = hash_password(password)
    assert password != hashed_1
    assert password != hashed_2
    assert hashed_1.startswith("$2")
    assert hashed_2.startswith("$2")
    assert verify_password(password, hashed_1)
    assert verify_password(password, hashed_2)


@pytest.mark.parametrize("password", [DEFAULT_PASSWORD, ANOTHER_PASSWORD])
def test_hash_and_verify_password_failure(password):
    hashed = hash_password(password)
    if password == DEFAULT_PASSWORD:
        assert not verify_password(ANOTHER_PASSWORD, hashed)
    elif password == ANOTHER_PASSWORD:
        assert not verify_password(DEFAULT_PASSWORD, hashed)
