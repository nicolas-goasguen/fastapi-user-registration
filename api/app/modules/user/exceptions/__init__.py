from app.modules.user.exceptions.db import (
    UserCrudInsertError,
    UserCrudUpdateIsActiveError,
)
from app.modules.user.exceptions.service import (
    UserAlreadyRegisteredError,
    UserAlreadyActivatedError,
)

__all__ = [
    # DB
    "UserCrudInsertError",
    "UserCrudUpdateIsActiveError",
    # Service
    "UserAlreadyRegisteredError",
    "UserAlreadyActivatedError",
]
