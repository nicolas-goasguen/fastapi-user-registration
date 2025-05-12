from typing import Annotated

from aiosmtplib import SMTPException
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.db import database
from app.core.utils import verify_password, send_email
from app.schemas.users import UserRegister, UserActivate
from app.services import users as users_services


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

security = HTTPBasic()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserRegister):
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
    async with database.transaction():
        user = await users_services.get_user_by_email(user_in.email)

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already in use."
            )

        user = await users_services.create_user(user_in)
        verification = await users_services.create_verification_code(user.id)
        await send_email(user.email, verification.code)

        return {"message": "User registered. Please check your email to activate it."}


@router.patch("/activate", status_code=status.HTTP_200_OK)
async def activate_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        data: UserActivate
):
    """
    Activate authenticated user using a verification code.

    **Parameters**
    - **username (from Basic Auth)**: The email of the user.
    - **password (from Basic Auth)**: The password of the user.
    - **verification_code**: The activation code (received by email).

    **Responses**:
    - **200 OK**: User activated successfully.
    - **400 Bad Request**: Invalid or expired verification code.
    - **401 Unauthorized**: Invalid credentials.
    - **403 Forbidden**: User already activated.
    """
    user = await users_services.get_user_by_email(credentials.username)

    if not user or not verify_password(credentials.password,
                                       user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )
    if user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already activated."
        )

    result = await users_services.activate_user(user.id, data.verification_code)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code."
        )

    return {"message": "User activated successfully."}
