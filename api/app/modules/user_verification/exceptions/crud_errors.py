from app.core.exceptions.exceptions import DBBaseError


class UserVerificationCrudError(DBBaseError):
    """Base class for db-level errors related to verification code operations."""

    def __init__(
        self, message="A database error occurred during a user verification operation."
    ):
        super().__init__(message)


class UserVerificationCrudInsertError(UserVerificationCrudError):
    """Raised when a verification code cannot be created in the database."""

    def __init__(self, message="A database error occurred during user insertion."):
        super().__init__(message)
