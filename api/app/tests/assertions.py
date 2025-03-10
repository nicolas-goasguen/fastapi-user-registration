from fastapi import status

from app.tests.tools import get_code_from_email, get_user_new_emails


def assert_register_ok(response):
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": "User registered. Check your email to activate it."
    }


def assert_register_ko_already_registered(response):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Email is already in use."}


def assert_activate_ok(response):
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "User activated successfully."}


def assert_activate_ko_invalid_credentials(response):
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials."}


def assert_activate_ko_invalid_verification_code(response):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Invalid or expired verification code."
    }


def assert_activate_ko_expired_verification_code(response):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Invalid or expired verification code."
    }


def assert_activate_ko_already_activated(response):
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "User already activated."}


async def assert_only_one_correct_mail_sent(
        credentials,
        verification_data,
        emails
):
    new_emails = await get_user_new_emails(credentials, emails)
    assert len(new_emails) == 1
    assert get_code_from_email(new_emails[0]) == verification_data["code"]
