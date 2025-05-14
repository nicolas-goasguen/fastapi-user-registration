from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.modules.user_verification.exceptions import (
    UserVerificationInvalidOrExpiredError,
)
from app.modules.user_verification.exceptions.crud_errors import (
    UserVerificationCrudError,
)


def register_crud_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserVerificationCrudError)
    async def handle_crud_generic_error(request, exception):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": str(exception)},
        )


def register_service_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserVerificationInvalidOrExpiredError)
    async def handle_invalid_or_expired_error(request, exception):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": str(exception)},
        )


def register_all_exception_handlers(app: FastAPI) -> None:
    register_crud_handlers(app)
    register_service_handlers(app)
