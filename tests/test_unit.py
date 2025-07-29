import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text

from app.main import app
from app.repository.repository import TronRepository
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.models import Base


transport = ASGITransport(app=app)


@pytest_asyncio.fixture(scope='function')
async def client():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_save_request_db_success():
    test_engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=False)
    async with test_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
    test_session = async_sessionmaker(bind=test_engine, expire_on_commit=False)
    async with test_session() as session:
        repository = TronRepository(session=session)
        test_address = "test_address"

        await repository.save_request(address=test_address)

        query = await session.execute(
            text("SELECT wallet_address FROM requests WHERE wallet_address=:test_address"),
            {"test_address": test_address}
        )
        result = query.first()

        assert result is not None
        assert result[0] == test_address

