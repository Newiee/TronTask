from sqlalchemy import select, func, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Request


class TronRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_requests(self, page, size):
        query = select(Request).offset((page - 1) * size).limit(size)
        query_result = await self._session.execute(query)
        requests = query_result.scalars().all()
        count = select(func.count(Request.id))
        total = await self._session.execute(count)
        total_result = total.scalar_one()
        return requests, total_result

    async def save_request(self, address: str):
        query = insert(Request).values(wallet_address=address, time_of_request=func.now())
        await self._session.execute(query)
        await self._session.commit()
