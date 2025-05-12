from app.schemas.user import UserFromDB


async def create(db, email: str, password_hash: str) -> UserFromDB | None:
    """
    Create a new user.
    """

    query = """
        INSERT INTO users (email, password_hash) 
        VALUES (:email, :password_hash)
        RETURNING id, email, is_active
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
        pass  # TODO: raise custom exception

    return UserFromDB(**row)


async def get_by_email(db, email: str) -> UserFromDB | None:
    """
    Get a specific user by email.
    """

    query = """
        SELECT id, email, is_active
        FROM users 
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
        UPDATE users
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
        pass  # TODO: raise custom exception

    return UserFromDB(**row)
