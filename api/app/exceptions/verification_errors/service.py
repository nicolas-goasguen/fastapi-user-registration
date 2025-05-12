from app.exceptions.base import ServiceBaseError


class VerificationCodeServiceError(ServiceBaseError):
    """Base class for db-level errors related to verification code operations."""

    pass


class VerificationCodeInvalidOrExpiredError(VerificationCodeServiceError):
    """Raised when the provided verification code is invalid or has expired."""

    pass
