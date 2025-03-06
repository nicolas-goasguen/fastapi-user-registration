from app.core.db import database
from app.core.utils import hash_password
from app.schemas.users import UserRegister


async def get_all_users():
    """
    Get all users.
    """
    query = "SELECT * FROM users;"
    return await database.fetch_all(query)


async def get_user_by_email(email: str):
    """
    Get a specific user by email.
    """
    query = "SELECT * FROM users WHERE email = :email;"
    return await database.fetch_one(query, {"email": email})


async def register_user(user_in: UserRegister):
    """
    Register a new user.
    """
    query = "INSERT INTO users (email, password_hash) VALUES (:email, :password_hash);"
    password_hash = hash_password(user_in.password)
    return await database.execute(query, {
        "email": user_in.email,
        "password_hash": password_hash
    })
