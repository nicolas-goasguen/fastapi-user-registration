from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.exceptions import DBBaseError, ServiceBaseError


# CRUD errors


class UserCrudBaseError(DBBaseError):
    """Base class for database errors related to user operations."""

    def __init__(self, message="A database error occurred during a user operation."):
        super().__init__(message)


class UserCrudInsertError(UserCrudBaseError):
    """Raised when a user cannot be created in the database."""

    def __init__(self, message="A database error occurred during user insertion."):
        super().__init__(message)


class UserCrudUpdateIsActiveError(UserCrudBaseError):
    """Raised when a user cannot be activated in the database."""

    def __init__(self, message="A database error occurred during user activation."):
        super().__init__(message)


class UserVerificationCrudInsertError(UserCrudBaseError):
    """Raised when a verification code cannot be created in the database."""

    def __init__(self, message="A database error occurred during user insertion."):
        super().__init__(message)


# Service errors


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


class UserVerificationCodeInvalidError(UserServiceBaseError):
    """Raised when the provided verification code is invalid or has expired."""

    status_code = 422

    def __init__(self, message="This verification code is invalid or has expired."):
        super().__init__(message)


# Handlers


def register_crud_exceptions_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserCrudBaseError)
    async def handle_crud_generic_error(request, exception):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": str(exception)},
        )


def register_service_exceptions_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserServiceBaseError)
    async def handle_service_generic_error(request, exception):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": str(exception)},
        )


def register_exceptions_handlers(app: FastAPI) -> None:
    register_crud_exceptions_handlers(app)
    register_service_exceptions_handlers(app)
