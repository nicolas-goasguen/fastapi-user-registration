from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    password: str


class UserActivate(BaseModel):
    code: str


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
