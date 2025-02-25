from datetime import datetime
from typing import List
from at_common_schemas.base import BaseSchema
from pydantic import Field
from at_common_schemas.common.stock import StockCandlestickDaily

class StockCandlestickDailyBatchRequest(BaseSchema):
    symbol: str = Field(..., description="Stock symbol")
    date_from: datetime = Field(..., description="Start date for the request")
    date_to: datetime = Field(..., description="End date for the request")

class StockCandlestickDailyBatchResponse(BaseSchema):
    items: List[StockCandlestickDaily] = Field(..., description="List of daily candlestick data")