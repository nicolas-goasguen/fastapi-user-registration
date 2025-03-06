from app.core.db import database


async def get_user_by_email(email: str):
    """
    Get a specific user by email.
    """
    query = "SELECT * FROM users WHERE email = :email;"
    return await database.fetch_one(query, {"email": email})


async def get_all_users():
    """
    Get all users.
    """
    query = "SELECT * FROM users;"
    return await database.fetch_all(query)
