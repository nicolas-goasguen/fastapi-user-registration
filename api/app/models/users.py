from datetime import datetime

from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    email: str
    password_hash: str
    is_active: bool


class VerificationCodeModel(BaseModel):
    id: int
    user_id: str
    code: str
    created_at: datetime
