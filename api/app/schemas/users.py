from pydantic import BaseModel, EmailStr, field_validator

from app.core.utils import is_valid_password, is_valid_verification_code


class UserRegister(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not is_valid_password(password):
            raise ValueError(
                "The password must be between 6 and 20 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character.")
        return password


class UserActivate(BaseModel):
    verification_code: str

    @field_validator("verification_code")
    @classmethod
    def validate_verification_code(cls, verification_code: str) -> str:
        if not is_valid_verification_code(verification_code):
            raise ValueError("The verification code must be exactly 4 digits.")
        return verification_code


class UserResponse(BaseModel):
    email: EmailStr
    is_active: bool
