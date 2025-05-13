from app.modules.base.exceptions import DBBaseError


class VerificationCodeCrudError(DBBaseError):
    """Base class for db-level errors related to verification code operations."""


class VerificationCodeCrudInsertError(VerificationCodeCrudError):
    """Raised when a verification code cannot be created in the database."""

    pass
