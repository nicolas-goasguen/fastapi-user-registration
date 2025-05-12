from pydantic import BaseModel, EmailStr, field_validator

from app.core.utils import is_valid_password


class UserFromDB(BaseModel):
    id: int
    email: str
    is_active: bool


class UserRegister(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        if not is_valid_password(password):
            raise ValueError(
                "The password must be between 6 and 20 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        return password


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
