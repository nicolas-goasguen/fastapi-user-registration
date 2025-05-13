from app.modules.base.exceptions import ServiceBaseError


class UserServiceBaseError(ServiceBaseError):
    """Base class for service-level errors related to user operations."""

    pass


class UserAlreadyRegisteredError(UserServiceBaseError):
    """
    Raised when an email has already been used for registration.
    """

    pass


class UserAlreadyActivatedError(UserServiceBaseError):
    """
    Raised when a user has already been activated.
    """

    pass
