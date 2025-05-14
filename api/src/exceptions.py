import importlib
from pathlib import Path

from fastapi import FastAPI


# Exceptions


class DBBaseError(Exception):
    """Base class for all database-level operation errors."""

    status_code = 500


class ServiceBaseError(Exception):
    """Base class for all service-level operation errors."""

    status_code = 500


# Handlers loader


def register_all_exception_handlers(app: FastAPI):
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
