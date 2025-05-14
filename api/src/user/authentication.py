from typing import Annotated

import bcrypt
from databases import Database
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.database import get_db
from src.user import crud as user_crud
from src.user.exceptions import (
    UserInvalidCredentialsError,
    UserNotActivatedError,
)
from src.user.schemas import UserResponse

security = HTTPBasic()


def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


async def get_current_user(
    db: Annotated[Database, Depends(get_db)],
    credentials: HTTPBasicCredentials = Depends(security),
) -> UserResponse:
    user = await user_crud.get_by_email(db, credentials.username)
    if not user:
        raise UserInvalidCredentialsError

    password_ok = verify_password(credentials.password, user.password_hash)
    if not password_ok:
        raise UserInvalidCredentialsError

    return UserResponse(**user.model_dump())


async def get_current_active_user(
    db: Annotated[Database, Depends(get_db)],
    credentials: HTTPBasicCredentials = Depends(security),
):
    user = await get_current_user(db, credentials)
    if not user.is_active:
        raise UserNotActivatedError
    return user
