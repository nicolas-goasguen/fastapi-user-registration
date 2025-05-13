from app.modules.base.exceptions import DBBaseError


class UserCrudError(DBBaseError):
    """Base class for db-level errors related to user operations."""

    pass


class UserCrudInsertError(UserCrudError):
    """Raised when a user cannot be created in the database."""

    pass


class UserCrudUpdateIsActiveError(UserCrudError):
    """Raised when a user cannot be activated in the database."""

    pass
