import datetime

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database import get_session
from app.main import app
from app.models import Base, Request

test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
test_session = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def override_get_db():
    async def _override_get_db():
        async with test_session() as session:
            yield session
    app.dependency_overrides[get_session] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_requests_from_db_success(override_get_db):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session() as session:
        session.add(Request(wallet_address="test_address", time_of_request=datetime.datetime.now()))
        await session.commit()

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/tron/requests")
        assert response.status_code == 200
        assert "test_address" in str(response.content)