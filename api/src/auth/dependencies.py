from typing import Annotated

from databases import Database
from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from src.auth.utils import verify_password
from src.dependencies import get_db
from src.user.crud import get_user_by_email
from src.user.exceptions import (
    UserInvalidCredentialsError,
    UserNotActivatedError,
)
from src.user.schemas import UserPublic

security = HTTPBasic()


async def get_current_user(
    db: Annotated[Database, Depends(get_db)],
    credentials: HTTPBasicCredentials = Depends(security),
) -> UserPublic:
    user = await get_user_by_email(db, credentials.username)
    if not user:
        raise UserInvalidCredentialsError

    password_ok = verify_password(credentials.password, user.password_hash)
    if not password_ok:
        raise UserInvalidCredentialsError

    return UserPublic(**user.model_dump())


async def get_current_active_user(
    db: Annotated[Database, Depends(get_db)],
    credentials: HTTPBasicCredentials = Depends(security),
):
    user = await get_current_user(db, credentials)
    if not user.is_active:
        raise UserNotActivatedError
    return user
