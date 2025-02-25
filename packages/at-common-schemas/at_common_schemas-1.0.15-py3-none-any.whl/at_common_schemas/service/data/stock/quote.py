from typing import List
from at_common_schemas.common.stock import StockQuote
from at_common_schemas.base import BaseSchema
from pydantic import Field

class StockQuoteRequest(BaseSchema):
    """Request for a stock quote."""
    symbol: str = Field(..., description="The stock symbol for which the quote is requested.")

class StockQuoteResponse(StockQuote):
    """Response containing stock quote information."""
    pass
    
class StockQuoteBatchRequest(BaseSchema):
    """Request for a batch of stock quotes."""
    symbols: List[str] = Field(..., description="A list of stock symbols for which quotes are requested.")

class StockQuoteBatchResponse(BaseSchema):
    """Response containing a batch of stock quote information."""
    items: List[StockQuote] = Field(..., description="A list of stock quote responses.")