from databases import Database

from src.user.exceptions import (
    UserCrudInsertError,
    UserCrudUpdateIsActiveError,
    UserVerificationCrudInsertError,
)
from src.user.schemas import UserFromDB, UserVerificationFromDB


# User


async def create_user(
    db: Database,
    email: str,
    password_hash: str,
) -> UserFromDB | None:
    """
    Create a new user.
    """

    query = """
        INSERT INTO user_data (email, password_hash) 
        VALUES (:email, :password_hash)
        RETURNING id, email, password_hash, is_active
        ;
    """

    row = await db.fetch_one(
        query,
        {
            "email": email,
            "password_hash": password_hash,
        },
    )

    if not row:
        raise UserCrudInsertError

    return UserFromDB(**dict(row))


async def get_user_by_email(
    db: Database,
    email: str,
) -> UserFromDB | None:
    """
    Get a specific user by email.
    """

    query = """
        SELECT id, email, password_hash, is_active
        FROM user_data 
        WHERE email = :email 
        LIMIT 1
        ;
    """

    row = await db.fetch_one(
        query,
        {
            "email": email,
        },
    )

    if not row:
        return None

    return UserFromDB(**dict(row))


async def update_user_is_active(
    db: Database,
    user_id: int,
    is_active: bool = True,
) -> UserFromDB | None:
    """
    Activate or deactivate a user.
    """

    query = """
        UPDATE user_data
        SET is_active = :is_active
        WHERE id = :user_id
        RETURNING id, email, password_hash, is_active
        ;
    """

    row = await db.fetch_one(
        query,
        {
            "user_id": user_id,
            "is_active": is_active,
        },
    )

    if not row:
        raise UserCrudUpdateIsActiveError

    return UserFromDB(**dict(row))


# User verification


async def create_user_verification(
    db: Database,
    user_id: int,
    code: str,
) -> UserVerificationFromDB | None:
    """
    Create a verification code for a user.
    """

    query = """
        INSERT INTO user_verification (user_id, code) 
        VALUES (:user_id, :code)
        RETURNING id, user_id, code, created_at
        ;
    """

    row = await db.fetch_one(
        query,
        {
            "user_id": user_id,
            "code": code,
        },
    )

    if not row:
        raise UserVerificationCrudInsertError

    return UserVerificationFromDB(**dict(row))


async def get_valid_user_verification(
    db: Database,
    user_id: int,
    code: str,
) -> UserVerificationFromDB | None:
    """
    Get user verification code from string code.
    """

    query = """
        SELECT id, user_id, code, created_at
        FROM user_verification
        WHERE 
            user_id = :user_id
            AND code = :code
            AND created_at > NOW() - INTERVAL '1 minute'
        ;
    """

    row = await db.fetch_one(
        query,
        {
            "user_id": user_id,
            "code": code,
        },
    )

    if not row:
        return None

    return UserVerificationFromDB(**dict(row))
