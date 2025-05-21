from fastapi import status

from src.user.tests.utils import get_code_from_email, get_user_new_emails


def assert_register_ok(response):
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "detail": "User registered. Please check your email to activate it."
    }


def assert_register_ko_already_registered(response):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "This email has already been used for registration."
    }


def assert_register_ko_invalid_email_format(response):
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert "detail" in response_json
    assert len(response_json["detail"]) == 1
    response_detail = response_json["detail"][0]
    assert response_detail["type"] == "value_error"
    assert response_detail["loc"] == ["body", "email"]


def assert_register_ko_invalid_password_format(response):
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert "detail" in response_json
    assert len(response_json["detail"]) == 1
    response_detail = response_json["detail"][0]
    assert response_detail["type"] == "value_error"
    assert response_detail["loc"] == ["body", "password"]
    assert response_detail["msg"] == (
        "Value error, The password must be between 6 and 20 characters long "
        "and include at least one uppercase letter, one lowercase letter, "
        "one digit, and one special character."
    )


def assert_activate_ok(response):
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "detail": "User activated successfully. Please check your email for confirmation."
    }


def assert_activate_ko_invalid_credentials(response):
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "You are not authorized to perform this action (invalid credentials)."
    }


def assert_activate_ko_invalid_verification_code(response):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "This verification code is invalid or has expired."
    }


def assert_activate_ko_expired_verification_code(response):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "This verification code is invalid or has expired."
    }


def assert_activate_ko_invalid_verification_code_format(response):
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert "detail" in response_json
    assert len(response_json["detail"]) == 1
    response_detail = response_json["detail"][0]
    assert response_detail["type"] == "value_error"
    assert response_detail["loc"] == ["body", "code"]


def assert_activate_ko_already_activated(response):
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "This account has already been activated."}


async def assert_only_one_correct_mail_sent(credentials, verification_data, emails):
    new_emails = await get_user_new_emails(credentials, emails)
    assert len(new_emails) == 1
    assert get_code_from_email(new_emails[0]) == verification_data["code"]


def assert_warning_logged(caplog, expected_message: str, logger_name: str):
    logs = [
        r for r in caplog.records if r.levelname == "WARNING" and r.name == logger_name
    ]
    assert any(
        expected_message in r.message for r in logs
    ), f"Expected warning '{expected_message}' not found in logs for logger '{logger_name}'"
