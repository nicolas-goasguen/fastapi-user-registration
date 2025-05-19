from datetime import datetime


def side_effect_db_create_user(
    query: str,
    values: dict,
) -> dict:
    return {
        "id": 1,
        "email": values["email"],
        "password_hash": values["password_hash"],
        "is_active": False,
    }


def return_value_db_user(
    email: str,
    password_hash: str,
    id_: int = 1,
    is_active: bool = False,
) -> dict:
    return {
        "id": id_,
        "email": email,
        "password_hash": password_hash,
        "is_active": is_active,
    }


def side_effect_db_create_user_verification(
    query: str,
    values: dict,
) -> dict:
    return {
        "id": 1,
        "user_id": values["user_id"],
        "code": values["code"],
        "created_at": datetime.now(),
    }


def return_value_db_user_verification(
    user_id: int,
    code: str,
    id_: int = 1,
    created_at: datetime = datetime.now(),
) -> dict:
    return {
        "id": id_,
        "user_id": user_id,
        "code": code,
        "created_at": created_at,
    }
