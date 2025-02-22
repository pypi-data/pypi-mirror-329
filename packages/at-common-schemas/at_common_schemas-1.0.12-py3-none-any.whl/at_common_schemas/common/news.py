from datetime import datetime
from pydantic import Field
from at_common_schemas.base import BaseSchema

class News(BaseSchema):
    published_date: datetime = Field(..., description="The UTC timestamp when the news article was published")
    headline: str = Field(..., description="The main title/headline of the news article")
    image: str = Field(..., description="The URL of the featured image or thumbnail for the news article")
    source: str = Field(..., description="The name of the news publisher or media outlet")
    summary: str = Field(..., description="A concise summary or excerpt of the news article content")
    url: str = Field(..., description="The direct URL link to read the full news article")

class NewsMarket(News):
    pass

class NewsStock(News):
    symbol: str = Field(..., description="The stock ticker symbol the news article relates to")