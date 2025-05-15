from typing import Annotated

from databases import Database
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasic

from src.dependencies import get_db
from src.user import service as user_service
from src.user.authentication import get_current_user
from src.user.schemas import UserRegister, UserResponse
from src.user.schemas import UserVerificationActivate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

security = HTTPBasic()


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
    return {"detail": "User registered. Please check your email to activate it."}


@router.patch("/activate", status_code=status.HTTP_200_OK)
async def activate_user(
    verification_in: UserVerificationActivate,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Annotated[Database, Depends(get_db)],
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
    await user_service.activate_user(db, current_user, verification_in)
    return {
        "detail": "User activated successfully. Please check your email for confirmation."
    }
