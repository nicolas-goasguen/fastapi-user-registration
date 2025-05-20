from unittest.mock import MagicMock, AsyncMock

import httpx
import pytest
from asgi_lifespan import LifespanManager

from src.main import app as fastapi_app


@pytest.fixture(autouse=True)
def app():
    fastapi_app.dependency_overrides.clear()
    yield fastapi_app
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
async def manager_app(app):
    async with LifespanManager(app) as manager:
        yield manager.app


@pytest.fixture
async def client(manager_app):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=manager_app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def mock_db():
    db = MagicMock()
    tx = AsyncMock()
    db.transaction.return_value = tx
    tx.__aenter__.return_value = db
    tx.__aexit__.return_value = None
    return db
