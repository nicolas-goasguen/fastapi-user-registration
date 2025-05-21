from datetime import datetime, timedelta

from databases import Database

import src.user.crud as user_crud
from src.auth.utils import hash_password
from src.logging import get_logger
from src.user.exceptions import (
    UserAlreadyRegisteredError,
    UserAlreadyActivatedError,
    UserVerificationCodeInvalidError,
)
from src.user.schemas import (
    UserRegister,
    UserPublic,
    UserVerificationActivate,
)
from src.user.tasks.email import (
    send_confirmation_email,
    send_verification_email,
)
from src.user.utils import generate_random_4_digits

logger = get_logger(__name__)


async def register_user(
    db: Database,
    user_in: UserRegister,
) -> UserPublic:
    """
    Register a new user and send a verification email.
    """

    async with db.transaction():
        existing_user = await user_crud.get_user_by_email(db, user_in.email)
        if existing_user:
            raise UserAlreadyRegisteredError

        password_hash = hash_password(user_in.password)
        user = await user_crud.create_user(db, str(user_in.email), password_hash)
        code = generate_random_4_digits()
        verification = await user_crud.create_user_verification(db, user.id, code)

    logger.info(
        f"User ID {user.id} registered, verification code ID {verification.id} created."
    )
    try:
        send_verification_email.delay(user.email, verification.code)
    except Exception as e:
        logger.warning(
            f"Failed to enqueue verification email for user ID {user.id}: {e}"
        )

    return UserPublic(**user.model_dump())


async def activate_user(
    db: Database,
    user: UserPublic,
    verification_in: UserVerificationActivate,
) -> UserPublic:
    """
    Activate authenticated user using a verification code if valid.
    """
    if user.is_active is True:
        raise UserAlreadyActivatedError

    async with db.transaction():
        valid_verification = await user_crud.get_valid_user_verification(
            db, user.id, verification_in.code
        )
        if not valid_verification:
            raise UserVerificationCodeInvalidError
        if valid_verification.created_at < datetime.now() - timedelta(minutes=1):
            raise UserVerificationCodeInvalidError

        activated_user = await user_crud.update_user_is_active(
            db, user.id, is_active=True
        )

    logger.info(f"User ID {user.id} activated successfully.")
    try:
        send_confirmation_email.delay(activated_user.email)
    except Exception as e:
        logger.warning(
            f"Failed to enqueue confirmation email for user ID {activated_user.id}: {e}"
        )

    return UserPublic(**activated_user.model_dump())
