from app.core.db import database
from app.core.utils import hash_password, generate_4_digits, send_email
from app.schemas.users import (
    UserRegister, UserResponse, VerificationCodeResponse
)

async def get_user_by_email(email: str) -> UserResponse:
    """
    Get a specific user by email.
    """
    query = "SELECT * FROM users WHERE email = :email LIMIT 1;"
    return await database.fetch_one(query, {"email": email})


async def create_user(user_in: UserRegister) -> UserResponse:
    """
    Create a new user.
    """
    user_query = """
    INSERT INTO users (email, password_hash) 
    VALUES (:email, :password_hash)
    RETURNING id, email, is_active;
    """
    password_hash = hash_password(user_in.password)

    return await database.fetch_one(user_query, {
        "email": user_in.email,
        "password_hash": password_hash
    })

async def create_verification_code(user_id: int) -> VerificationCodeResponse:
    """
    Create a verification code for a user.
    """
    code_query = """
    INSERT INTO verification_codes (user_id, code) 
    VALUES (:user_id, :code)
    RETURNING id, code, created_at;
    """
    code = generate_4_digits()

    return await database.fetch_one(code_query, {
        "user_id": user_id,
        "code": code
    })


async def activate_user(user_id: int, code: str):
    """
    Activate a user.
    """
    async with database.transaction():
        query_valid_codes = """
            SELECT *
            FROM verification_codes
            WHERE 
                user_id = :user_id
                AND code = :code
                AND created_at > NOW() - INTERVAL '1 minute'
        """
        verification_code = await database.fetch_one(
            query_valid_codes,
            {"user_id": user_id, "code": code}
        )

        if not verification_code:
            return None

        query_activate = """
            UPDATE users
            SET is_active = True
            WHERE id = :user_id
        """

        await database.execute(query_activate, {
            "user_id": user_id,
        })

        return True
