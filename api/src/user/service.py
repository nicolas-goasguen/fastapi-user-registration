from datetime import datetime, timedelta

import src.user.crud as user_crud
from src.user.authentication import hash_password
from src.user.exceptions import (
    UserAlreadyRegisteredError,
    UserAlreadyActivatedError,
    UserVerificationCodeInvalidError,
)
from src.user.schemas import (
    UserRegister,
    UserResponse,
    UserVerificationActivate,
)
from src.user.utils import (
    send_verification_email,
    send_confirmation_email,
)


async def register_user(db, user_in: UserRegister) -> UserResponse:
    """
    Register a new user and send a verification email.
    """

    async with db.transaction():
        existing_user = await user_crud.get_by_email(db, user_in.email)
        if existing_user:
            raise UserAlreadyRegisteredError

        password_hash = hash_password(user_in.password)
        user = await user_crud.create(db, str(user_in.email), password_hash)
        verification = await user_crud.create_verification(db, user.id)

    await send_verification_email(user.email, verification.code)

    return UserResponse(**user.model_dump())


async def activate_user(
    db, user, verification_code_in: UserVerificationActivate
) -> UserResponse:
    """
    Activate authenticated user using a verification code if valid.
    """
    if user.is_active is True:
        raise UserAlreadyActivatedError

    async with db.transaction():
        valid_verification = await user_crud.get_valid_code(
            db, user.id, verification_code_in.code
        )
        if not valid_verification:
            raise UserVerificationCodeInvalidError
        if valid_verification.created_at < datetime.now() - timedelta(minutes=1):
            raise UserVerificationCodeInvalidError

        activated_user = await user_crud.update_is_active(db, user.id, is_active=True)

        await send_confirmation_email(activated_user.email)

        return UserResponse(**activated_user.model_dump())
