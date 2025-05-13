from app.modules.base.exceptions import DBBaseError


class UserVerificationCrudError(DBBaseError):
    """Base class for db-level errors related to verification code operations."""


class UserVerificationCrudInsertError(UserVerificationCrudError):
    """Raised when a verification code cannot be created in the database."""

    pass
