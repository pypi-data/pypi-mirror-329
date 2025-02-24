from datetime import datetime
from typing import List
from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.common.stock import StockIndicatorDaily

class StockIndicatorDailyBatchRequest(BaseSchema):
    symbols: List[str] = Field(..., description="List of stock symbols")
    date_from: datetime = Field(..., description="Start date for the request")
    date_to: datetime = Field(..., description="End date for the request")

class StockIndicatorDailyBatchResponse(BaseSchema):
    items: List[StockIndicatorDaily] = Field(..., description="List of daily stock indicators")