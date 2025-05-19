from src.auth.utils import verify_password, hash_password
from src.user.utils import is_valid_verification_code, generate_random_4_digits


def test_verify_password_valid():
    assert verify_password("abc123", hash_password("abc123"))


def test_verify_password_invalid():
    assert not verify_password("abc123", hash_password("wrong"))


def test_is_valid_verification_code_valid():
    assert is_valid_verification_code("1234")


def test_is_valid_verification_code_invalid_contains_letters():
    assert not is_valid_verification_code("12ab")


def test_is_valid_verification_code_invalid_too_long():
    assert not is_valid_verification_code("12345")


def test_is_valid_verification_code_ko_invalid_too_short():
    assert not is_valid_verification_code("123")


def test_generate_random_4_digits_ok():
    assert is_valid_verification_code(generate_random_4_digits())
