from enum import Enum
from datetime import datetime
from typing import List
from at_common_schemas.base import BaseSchema
from pydantic import Field

class CalendarEarningPublishTime(Enum):
    BEFORE_MARKET_OPEN = "BEFORE_MARKET_OPEN"
    AFTER_MARKET_CLOSE = "AFTER_MARKET_CLOSE"
    UNKNOWN = "UNKNOWN"

# Earnings
class CalendarEarningItem(BaseSchema):
    symbol: str = Field(..., description="The stock symbol associated with the earnings report")
    publish_time: CalendarEarningPublishTime = Field(..., description="When earnings will be published: before market open, after market close, or unknown")
    eps_actual: float = Field(..., description="Actual earnings per share (EPS) reported by the company")
    eps_estimate: float = Field(..., description="Analysts' consensus estimate for earnings per share (EPS)")
    revenue_actual: float = Field(..., description="Actual revenue reported by the company in their base currency")
    revenue_estimate: float = Field(..., description="Analysts' consensus estimate for revenue in company's base currency")
    fiscal_date_ending: datetime = Field(..., description="The last date of the fiscal period this earnings report covers")

class CalendarEarnings(BaseSchema):
    date: datetime = Field(..., description="The scheduled date of the earnings announcement")
    items: List[CalendarEarningItem] = Field(..., description="List of companies reporting earnings on this date")

# Dividend
class CalendarDividendItem(BaseSchema):
    symbol: str = Field(..., description="The stock symbol associated with the dividend.")
    dividend: float = Field(..., description="The declared dividend amount per share.")
    adj_dividend: float = Field(..., description="The dividend amount adjusted for stock splits and other corporate actions.")
    record_date: datetime | None = Field(None, description="The date when stockholders must be on record to receive the dividend.")
    payment_date: datetime | None = Field(None, description="The date when the dividend will be paid to shareholders.")

class CalendarDividends(BaseSchema):
    date: datetime = Field(..., description="The announcement date of the dividends.")
    items: List[CalendarDividendItem] = Field(..., description="List of dividend declarations for the specified date.")

# Split
class CalendarSplitItem(BaseSchema):
    symbol: str = Field(..., description="The stock symbol associated with the stock split")
    numerator: int = Field(..., description="Top number in split ratio (e.g., 2 in a 2:1 split)")
    denominator: int = Field(..., description="Bottom number in split ratio (e.g., 1 in a 2:1 split)")

class CalendarSplits(BaseSchema):
    date: datetime = Field(..., description="The effective date when the stock split takes place")
    items: List[CalendarSplitItem] = Field(..., description="List of stock splits occurring on this date")