from typing import List
from at_common_schemas.base import BaseSchema
from at_common_schemas.common.stock import StockProfile
from pydantic import Field

class StockProfileRequest(BaseSchema):
    """Request for a stock profile."""
    symbol: str = Field(..., description="The stock symbol for which the profile is requested.")

class StockProfileResponse(StockProfile):
    """Response containing stock profile information."""
    pass

class StockProfileBatchRequest(BaseSchema):
    """Request for a batch of stock profiles."""
    symbols: List[str] = Field(..., description="A list of stock symbols for which profiles are requested.")

class StockProfileBatchResponse(BaseSchema):
    """Response containing a batch of stock profile information."""
    items: List[StockProfile] = Field(..., description="A list of stock profiles.")