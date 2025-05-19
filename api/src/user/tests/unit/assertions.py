from pydantic_core import ErrorDetails


def assert_value_error_verification_code(errors: list[ErrorDetails]):
    assert len(errors) == 1
    err = errors[0]
    assert err["loc"] == ("code",)
    assert err["msg"] == "Value error, The verification code must be exactly 4 digits."


def assert_value_error_password_hash_empty(errors: list[ErrorDetails]):
    assert len(errors) == 1
    err = errors[0]
    assert err["loc"] == ("password_hash",)
    assert err["msg"] == "Value error, Password hash must be a non-empty string."


def assert_value_error_password_hash_invalid(errors: list[ErrorDetails]):
    assert len(errors) == 1
    err = errors[0]
    assert err["loc"] == ("password_hash",)
    assert err["msg"] == "Value error, Password hash must be a valid bcrypt hash."
