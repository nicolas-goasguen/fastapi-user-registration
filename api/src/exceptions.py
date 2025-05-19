import importlib
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse


# Exceptions


class DBBaseError(Exception):
    """Base class for all database-level operation errors."""

    status_code = 500


class ServiceBaseError(Exception):
    """Base class for all service-level operation errors."""

    status_code = 500


# Handlers loader


def register_db_base_exceptions_handlers(app: FastAPI) -> None:
    @app.exception_handler(DBBaseError)
    async def handle_db_generic_error(request, exception):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": str(exception)},
        )


def register_service_base_exceptions_handlers(app: FastAPI) -> None:
    @app.exception_handler(ServiceBaseError)
    async def handle_service_generic_error(request, exception):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": str(exception)},
        )


def register_all_exception_handlers(app: FastAPI):
    # static imports
    register_db_base_exceptions_handlers(app)
    register_service_base_exceptions_handlers(app)

    # dynamic imports
    ignore = ["tests"]
    base_path = Path(__file__).resolve().parents[0]
    for module_path in base_path.iterdir():
        if not module_path.is_dir() or module_path in ignore:
            continue
        try:
            dotted = f"src.{module_path.name}.exceptions"
            mod = importlib.import_module(dotted)
            getattr(mod, "register_exceptions_handlers")(app)
        except (ModuleNotFoundError, AttributeError):
            continue  # TODO: log as a warning when not found
