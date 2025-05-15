import httpx
import pytest
from asgi_lifespan import LifespanManager

from src.main import app as fastapi_app


@pytest.fixture
async def app():
    async with LifespanManager(fastapi_app) as manager:
        yield manager.app


@pytest.fixture
async def client(app):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://api",
    ) as client:
        yield client
