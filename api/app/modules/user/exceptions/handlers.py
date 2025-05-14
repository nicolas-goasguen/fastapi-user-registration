from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.modules.user.exceptions import (
    UserAlreadyRegisteredError,
    UserAlreadyActivatedError,
)
from app.modules.user.exceptions.crud_errors import UserCrudError


def register_crud_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserCrudError)
    async def handle_crud_generic_error(request, exception):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": str(exception)},
        )


def register_service_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserAlreadyRegisteredError)
    async def handle_already_registered_error(request, exception):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": str(exception)},
        )

    @app.exception_handler(UserAlreadyActivatedError)
    async def handle_already_activated_error(request, exception):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": str(exception)},
        )


def register_all_exception_handlers(app: FastAPI) -> None:
    register_crud_handlers(app)
    register_service_handlers(app)
