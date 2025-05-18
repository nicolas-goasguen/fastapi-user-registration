from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from src.user.utils import is_valid_password, is_valid_verification_code


class UserFromDB(BaseModel):
    id: int
    email: str
    password_hash: str
    is_active: bool


class UserRegister(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not is_valid_password(password):
            raise ValueError(
                "The password must be between 6 and 20 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        return password


class UserPublic(BaseModel):
    id: int
    email: str
    is_active: bool


class UserVerificationFromDB(BaseModel):
    id: int
    user_id: int
    code: str
    created_at: datetime


class UserVerificationActivate(BaseModel):
    code: str

    @field_validator("code")
    @classmethod
    def validate_code(cls, code: str) -> str:
        if not is_valid_verification_code(code):
            raise ValueError("The verification code must be exactly 4 digits.")
        return code
