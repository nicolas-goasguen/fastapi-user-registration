from app.core.exceptions.exceptions import ServiceBaseError


class UserVerificationServiceError(ServiceBaseError):
    """Base class for db-level errors related to verification code operations."""

    def __init__(
        self, message="A service error occurred during user verification operation."
    ):
        super().__init__(message)


class UserVerificationInvalidOrExpiredError(UserVerificationServiceError):
    """Raised when the provided verification code is invalid or has expired."""

    status_code = 422

    def __init__(self, message="This verification code is invalid or has expired."):
        super().__init__(message)
