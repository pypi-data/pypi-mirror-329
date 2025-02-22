from typing import List
from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.common.news import ( NewsMarket, NewsStock )

class NewsMarketBatchRequest(BaseSchema):
    limit: int = Field(..., description="Maximum number of news articles to retrieve (pagination limit)")

class NewsMarketBatchResponse(BaseSchema):
    items: List[NewsMarket] = Field(..., description="List of market news articles")

class NewsStockBatchRequest(BaseSchema):
    symbol: str = Field(..., description="The stock ticker symbol to fetch news for")
    limit: int = Field(..., description="Maximum number of news articles to retrieve (pagination limit)")

class NewsStockBatchResponse(BaseSchema):
    items: List[NewsStock] = Field(..., description="List of stock-specific news articles")