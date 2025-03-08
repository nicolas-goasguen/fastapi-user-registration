from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    password: str


class UserActivate(BaseModel):
    verification_code: str


class UserResponse(BaseModel):
    email: str
    is_active: bool
