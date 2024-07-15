import asyncio
import random
from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient
from sqlalchemy import text

from src.main import app
from src.core.config import settings
from src.core.constants import Environment
from src.core.database import engine, sync_engine, metadata, execute, get_async_session


@pytest.fixture(autouse=True, scope="session")
def check_env() -> None:
    assert settings.ENVIRONMENT == Environment.TESTING


@pytest.fixture(autouse=True, scope="session")
def setup_db():
    metadata.drop_all(sync_engine)
    print("DROP DB")
    metadata.create_all(sync_engine)
    print("CREATED DB")
    yield
    metadata.drop_all(sync_engine)


@pytest.fixture
def user_payload() -> dict[str, str]:
    user = {"login": "superuser1000" + str(random.randint(1, 10000)),
            "password": "iFetup66!",
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "env": "stage",
            "domain": "canary"}
    return user


# @pytest.fixture(scope="session")
# def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    async with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True, scope="function")
def truncate_users():
    delete_query1 = text("TRUNCATE TABLE auth_refresh_token")
    delete_query2 = text("TRUNCATE TABLE auth_user")
    asyncio.run(execute(delete_query1))
    asyncio.run(execute(delete_query2))
