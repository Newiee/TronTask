from sqlalchemy.ext.asyncio import AsyncSession

from app.pyd.response_models import PagResponse, Request
from app.repository.repository import TronRepository


class TronService:
    _session = AsyncSession()

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = TronRepository(session=self._session)

    async def get_requests(self, page, size) -> PagResponse:
        requests, total = await self._repository.get_requests(page, size)

        schema = PagResponse(page=page, items_per_page=size, total=total, items=requests)
        return schema

    async def save_request(self, address: str):
        await self._repository.save_request(address)