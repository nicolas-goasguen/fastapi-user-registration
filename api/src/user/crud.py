from src.user.exceptions import (
    UserCrudInsertError,
    UserCrudUpdateIsActiveError,
    UserVerificationCrudInsertError,
)
from src.user.schemas import UserFromDB, UserVerificationFromDB
from src.user.utils import generate_4_digits


# User


async def create(db, email: str, password_hash: str) -> UserFromDB | None:
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

    return UserFromDB(**row)


async def get_by_email(db, email: str) -> UserFromDB | None:
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

    return UserFromDB(**row)


async def update_is_active(
    db, user_id: int, is_active: bool = True
) -> UserFromDB | None:
    """
    Activate or deactivate a user.
    """

    query = """
        UPDATE user_data
        SET is_active = :is_active
        WHERE id = :user_id
        RETURNING id, email, is_active
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

    return UserFromDB(**row)


# User verification


async def create_verification(db, user_id: int) -> UserVerificationFromDB | None:
    """
    Create a verification code for a user.
    """

    query = """
        INSERT INTO user_verification (user_id, code) 
        VALUES (:user_id, :code)
        RETURNING id, user_id, code, created_at
        ;
    """

    code = generate_4_digits()

    row = await db.fetch_one(
        query,
        {
            "user_id": user_id,
            "code": code,
        },
    )

    if not row:
        raise UserVerificationCrudInsertError

    return UserVerificationFromDB(**row)


async def get_valid_verification(
    db, user_id: int, code: str
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

    return UserVerificationFromDB(**row)
