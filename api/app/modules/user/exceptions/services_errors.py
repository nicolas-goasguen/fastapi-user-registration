from app.core.exceptions.exceptions import ServiceBaseError


class UserServiceBaseError(ServiceBaseError):
    """Base class for service-level errors related to user operations."""

    def __init__(self, message="A service error occurred during user operation."):
        super().__init__(message)


class UserAlreadyRegisteredError(UserServiceBaseError):
    """
    Raised when an email has already been used for registration.
    """

    status_code = 409

    def __init__(self, message="This email has already been used for registration."):
        super().__init__(message)


class UserAlreadyActivatedError(UserServiceBaseError):
    """
    Raised when a user has already been activated.
    """

    status_code = 409

    def __init__(self, message="This account has already been activated."):
        super().__init__(message)
