from app.core.db import database
from app.core.utils import hash_password, generate_4_digits, send_email
from app.models.users import UserModel
from app.schemas.users import UserRegister


async def get_user_by_email(email: str) -> UserModel:
    """
    Get a specific user by email.
    """
    query = "SELECT * FROM users WHERE email = :email LIMIT 1;"
    return await database.fetch_one(query, {"email": email})


async def register_user(user_in: UserRegister):
    """
    Register a new user.
    """
    async with database.transaction():
        user_query = "INSERT INTO users (email, password_hash) VALUES (:email, :password_hash);"
        password_hash = hash_password(user_in.password)

        code_query = "INSERT INTO verification_codes (user_id, code) VALUES (:user_id, :code);"
        code = generate_4_digits()

        await database.execute(user_query, {
            "email": user_in.email,
            "password_hash": password_hash
        })

        user = await get_user_by_email(user_in.email)
        await database.execute(code_query, {
            "user_id": user.id,
            "code": code
        })

        await send_email(user.email, code)


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
