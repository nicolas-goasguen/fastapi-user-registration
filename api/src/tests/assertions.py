from fastapi import status

from src.tests.tools import get_code_from_email, get_user_new_emails


def assert_register_ok(response):
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": "User registered. Check your email to activate it."
    }


def assert_register_ko_already_registered(response):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Email is already in use."}


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
    assert response.json() == {"message": "User activated successfully."}


def assert_activate_ko_invalid_credentials(response):
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials."}


def assert_activate_ko_invalid_verification_code(response):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Invalid or expired verification code."}


def assert_activate_ko_expired_verification_code(response):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Invalid or expired verification code."}


def assert_activate_ko_invalid_verification_code_format(response):
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert "detail" in response_json
    assert len(response_json["detail"]) == 1
    response_detail = response_json["detail"][0]
    assert response_detail["type"] == "value_error"
    assert response_detail["loc"] == ["body", "verification_code"]


def assert_activate_ko_already_activated(response):
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "User already activated."}


async def assert_only_one_correct_mail_sent(credentials, verification_data, emails):
    new_emails = await get_user_new_emails(credentials, emails)
    assert len(new_emails) == 1
    assert get_code_from_email(new_emails[0]) == verification_data["code"]
