import importlib
from pathlib import Path

from fastapi import FastAPI


def register_all_exception_handlers(app: FastAPI):
    base_path = Path(__file__).resolve().parents[2] / "modules"
    for module_path in base_path.iterdir():
        if not module_path.is_dir():
            continue
        try:
            dotted = f"app.modules.{module_path.name}.exceptions.handlers"
            mod = importlib.import_module(dotted)
            getattr(mod, "register_all_exception_handlers")(app)
        except (ModuleNotFoundError, AttributeError):
            continue  # TODO: log as a warning when not found
