from typing import List
from at_common_schemas.base import BaseSchema
from pydantic import Field

class StockSymbolListRequest(BaseSchema):
    """Request for a list of stocks."""
    exchanges: List[str] = Field(..., description="List of stock exchange codes (e.g., NYSE, NASDAQ)")

class StockSymbolListResponse(BaseSchema):
    """Response containing a list of stocks."""
    items: List[str] = Field(..., description="A list of stock symbols.")