from datetime import datetime

from pydantic import BaseModel, field_validator, Field

from app.core.utils import is_valid_verification_code


class VerificationCodeFromDB(BaseModel):
    id: int
    user_id: int
    code: str
    created_at: datetime


class VerificationCodeActivate(BaseModel):
    code: str = Field(..., alias="verification_code")

    @classmethod
    @field_validator("code")
    def validate_code(cls, code: str) -> str:
        if not is_valid_verification_code(code):
            raise ValueError("The verification code must be exactly 4 digits.")
        return code
