import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import status

from app.main import app as fastapi_app


@pytest_asyncio.fixture
async def app():
    async with LifespanManager(fastapi_app) as manager:
        yield manager.app


@pytest_asyncio.fixture
async def client(app):
    async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://api"
    ) as client:
        # client.get_io_loop = asyncio.get_running_loop
        yield client


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/users/register",
        json={
            "email": "aaa.bbb@ccc.com",
            "password": "password"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": "User registered. Check your email to activate it."
    }
