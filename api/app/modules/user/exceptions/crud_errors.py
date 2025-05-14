from app.core.exceptions.exceptions import DBBaseError


class UserCrudError(DBBaseError):
    """Base class for database errors related to user operations."""

    def __init__(self, message="A database error occurred during a user operation."):
        super().__init__(message)


class UserCrudInsertError(UserCrudError):
    """Raised when a user cannot be created in the database."""

    def __init__(self, message="A database error occurred during user insertion."):
        super().__init__(message)


class UserCrudUpdateIsActiveError(UserCrudError):
    """Raised when a user cannot be activated in the database."""

    def __init__(self, message="A database error occurred during user activation."):
        super().__init__(message)
