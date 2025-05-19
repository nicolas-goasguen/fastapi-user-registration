from datetime import datetime

from pydantic import BaseModel, field_validator, EmailStr

from src.user.utils import is_valid_password, is_valid_verification_code


class UserMixin:
    @field_validator("password", check_fields=False)
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not value or not isinstance(value, str):
            raise ValueError("Password must be a non-empty string.")
        if not is_valid_password(value):
            raise ValueError(
                "Password must be between 6 and 20 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        return value

    @field_validator("password_hash", check_fields=False)
    @classmethod
    def validate_password_hash(cls, value: str) -> str:
        if not value or not isinstance(value, str):
            raise ValueError("Password hash must be a non-empty string.")
        if not value.startswith("$2") or len(value) < 60:
            raise ValueError("Password hash must be a valid bcrypt hash.")
        return value


class UserFromDB(UserMixin, BaseModel):
    id: int
    email: EmailStr
    password_hash: str
    is_active: bool


class UserRegister(UserMixin, BaseModel):
    email: EmailStr
    password: str


class UserPublic(UserMixin, BaseModel):
    id: int
    email: EmailStr
    is_active: bool


class UserVerificationMixin:
    @field_validator("code")
    @classmethod
    def validate_code(cls, code: str) -> str:
        if not is_valid_verification_code(code):
            raise ValueError("The verification code must be exactly 4 digits.")
        return code


class UserVerificationFromDB(UserVerificationMixin, BaseModel):
    id: int
    user_id: int
    code: str
    created_at: datetime


class UserVerificationActivate(BaseModel):
    code: str
