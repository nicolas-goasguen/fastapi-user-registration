from datetime import datetime

from databases import Database

from src.user.schemas import UserFromDB, UserVerificationFromDB


def side_effect_crud_create_user(
    db: Database,
    email: str,
    pwd_hash: str,
) -> UserFromDB:
    return UserFromDB(
        id=1,
        email=email,
        password_hash=pwd_hash,
        is_active=False,
    )


def side_effect_crud_create_verification(
    db: Database,
    user_id: int,
    code: str,
) -> UserVerificationFromDB:
    return UserVerificationFromDB(
        id=1,
        user_id=user_id,
        code=code,
        created_at=datetime.now(),
    )
