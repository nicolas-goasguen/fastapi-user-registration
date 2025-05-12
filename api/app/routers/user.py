from typing import Annotated

from databases import Database
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.db import get_db
from app.schemas.user import UserRegister
from app.schemas.verification import VerificationCodeActivate
from app.services import user as user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

security = HTTPBasic()

# TODO: catch exceptions


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserRegister,
    db: Annotated[Database, Depends(get_db)],
):
    """
    Register a new user and send a verification email.

    **Parameters**:
    - **email**: The email of the user (must be unique).
    - **password**: The password of the user.

    **Responses**:
    - **201 Created**: User registered successfully.
    - **400 Bad Request**: Email already in use.
    - **503 Service Unavailable**: Failed to send verification email.
    """
    await user_service.register_user(db, user_in)
    return {"message": "User registered. Please check your email to activate it."}


@router.patch("/activate", status_code=status.HTTP_200_OK)
async def activate_user(
    verification_in: VerificationCodeActivate,
    db: Annotated[Database, Depends(get_db)],
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    """
    Activate authenticated user using a verification code.

    **Parameters**
    - **username (from Basic Auth)**: The email of the user.
    - **password (from Basic Auth)**: The password of the user.
    - **code**: The verification code (received by email).

    **Responses**:
    - **200 OK**: User activated successfully.
    - **400 Bad Request**: Invalid or expired verification code.
    - **401 Unauthorized**: Invalid credentials.
    - **403 Forbidden**: User already activated.
    """
    await user_service.activate_user(db, credentials, verification_in)
    return {
        "message": "User activated successfully. Please check your email for confirmation."
    }
