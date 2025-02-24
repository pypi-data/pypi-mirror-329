from typing import List
from at_common_schemas.base import BaseSchema
from pydantic import Field
from at_common_schemas.common.stock import StockEarningsCall

class StockEarningsCallBatchRequest(BaseSchema):
    symbol: str = Field(..., description="Stock symbol")
    year_from: int = Field(..., description="Start year for the request")
    year_to: int = Field(..., description="End year for the request")

class StockEarningsCallBatchResponse(BaseSchema):
    items: List[StockEarningsCall] = Field(..., description="List of earnings calls")