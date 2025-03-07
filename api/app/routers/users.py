from typing import Annotated

from aiosmtplib import SMTPException
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.utils import verify_password
from app.schemas.users import UserRegister, UserResponse
from app.services import users as users_services

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

security = HTTPBasic()


@router.get("/")
async def read_all_users():
    return await users_services.get_all_users()


@router.get("/codes")
async def read_all_verification_codes():
    return await users_services.get_all_verification_codes()


@router.get("/me", response_model=UserResponse)
async def read_current_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    user = await users_services.get_user_by_email(credentials.username)

    if not user or not verify_password(
            credentials.password,
            user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )

    return user


@router.post("/register")
async def register_user(user_in: UserRegister):
    user = await users_services.get_user_by_email(user_in.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already in use."
        )

    try:
        await users_services.register_user(user_in)
    except SMTPException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Verification email failed to send. Retry registration later.")

    return {"message": "User registered. Check your email to activate it."}


@router.patch("/activate")
async def activate_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        verification_code: str
):
    user = await users_services.get_user_by_email(credentials.username)

    if not user or not verify_password(credentials.password,
                                       user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )
    if user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already activated."
        )

    result = await users_services.activate_user(user.id, verification_code)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code."
        )

    return {"message": "User activated successfully."}
