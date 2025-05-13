from datetime import datetime, timedelta

import app.modules.user.crud as user_crud
import app.modules.verification.crud as verification_crud
from app.core.utils import (
    send_verification_email,
    hash_password,
    send_confirmation_email,
)
from app.modules.user.exceptions import (
    UserAlreadyRegisteredError,
    UserAlreadyActivatedError,
)
from app.modules.user.schemas import (
    UserRegister,
    UserResponse,
)
from app.modules.verification.exceptions import (
    VerificationCodeInvalidOrExpiredError,
)
from app.modules.verification.schemas import VerificationCodeActivate


async def register_user(db, user_in: UserRegister) -> UserResponse:
    """
    Register a new user and send a verification email.
    """

    async with db.transaction():
        existing_user = await user_crud.get_by_email(db, user_in.email)
        if existing_user:
            raise UserAlreadyRegisteredError

        password_hash = hash_password(user_in.password)
        created_user = await user_crud.create(db, str(user_in.email), password_hash)
        created_code = await verification_crud.create_code(db, created_user.id)

    await send_verification_email(created_user.email, created_code.code)

    return UserResponse(**created_user.model_dump())


async def activate_user(
    db, credentials, verification_code_in: VerificationCodeActivate
) -> UserResponse:
    """
    Activate authenticated user using a verification code if valid.
    """

    async with db.transaction():
        existing_user = await user_crud.get_by_email(db, credentials.username)
        if existing_user and existing_user.is_active is True:
            raise UserAlreadyActivatedError

        valid_verification_code = await verification_crud.get_valid_code(
            db, existing_user.id, verification_code_in.code
        )
        if not valid_verification_code:
            raise VerificationCodeInvalidOrExpiredError
        if valid_verification_code.created_at < datetime.now() - timedelta(minutes=1):
            raise VerificationCodeInvalidOrExpiredError

        activated_user = await user_crud.update_is_active(
            db, existing_user.id, is_active=True
        )

        await send_confirmation_email(activated_user.email)

        return UserResponse(**activated_user.model_dump())
