from app.modules.base.exceptions import ServiceBaseError


class UserVerificationServiceError(ServiceBaseError):
    """Base class for db-level errors related to verification code operations."""

    pass


class UserVerificationInvalidOrExpiredError(UserVerificationServiceError):
    """Raised when the provided verification code is invalid or has expired."""

    pass
