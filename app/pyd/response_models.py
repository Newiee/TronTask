from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict


class Request(BaseModel):
    id: int
    wallet_address: str
    time_of_request: datetime

    model_config = ConfigDict(from_attributes=True)

class PagResponse(BaseModel):
    page: int
    items_per_page: int
    total: int
    items: List[Request]

    model_config = ConfigDict(from_attributes=True)


class WalletInfo(BaseModel):
    address: str
    bandwidth: int
    energy: int
    balance_trx: Decimal