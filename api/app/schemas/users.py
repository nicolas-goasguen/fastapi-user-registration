from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    email: int
    password_hash: int
    is_active: int


class UserRegister(BaseModel):
    email: str
    password: str


class UserActivate(BaseModel):
    email: str
    code: str
