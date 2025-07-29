from fastapi import APIRouter, Query, HTTPException, Path
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy.providers import HTTPProvider

from app.database import get_session
from app.pyd.response_models import PagResponse, WalletInfo
from app.service.service import TronService

from tronpy import Tron

from app.settings import settings

router = APIRouter(
    prefix="/tron",
    tags=['tron']
)

@router.get("/requests", response_model=PagResponse)
async def get_requests(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    session: AsyncSession = Depends(get_session)
) -> PagResponse:
    try:
        result = await TronService(session=session).get_requests(page, size)
        print(result)
    except Exception as e:
        raise e
    return result

@router.post("/get_info/{address}", response_model=WalletInfo)
async def get_wallet_info(
    address: str = Path(...),
    session: AsyncSession = Depends(get_session)
) -> WalletInfo:
    try:
        client = Tron(HTTPProvider(api_key=settings.API_KEY), network="mainnet")

        bandwidth = client.get_bandwidth(address)
        energy = client.get_energy(address)
        balance_trx = client.get_account_balance(address)

        await TronService(session=session).save_request(address)

        return WalletInfo(
            address=address,
            bandwidth=bandwidth,
            energy=energy,
            balance_trx=balance_trx
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))