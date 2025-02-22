from typing import List
from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.common.stock import StockFinancialPeriod, StockFinancialStatement, StockFinancialAnalysisKeyMetric, StockFinancialAnalysisKeyMetricTTM, StockFinancialAnalysisRatio, StockFinancialAnalysisRatioTTM

# Batch request and response for financial statements
class StockFinancialStatementBatchRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StockFinancialPeriod = Field(..., description="The financial period for the request.")
    limit: int = Field(..., description="The limit on the number of results returned.")

class StockFinancialStatementBatchResponse(BaseSchema):
    items: List[StockFinancialStatement] = Field(..., description="List of financial statements.")

# Batch request and response for financial key metrics
class StockFinancialAnalysisKeyMetricBatchRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StockFinancialPeriod = Field(..., description="The financial period for the request.")
    limit: int = Field(..., description="The limit for the number of results.")

class StockFinancialAnalysisKeyMetricBatchResponse(BaseSchema):
    items: List[StockFinancialAnalysisKeyMetric] = Field(..., description="List of key metrics for the stock.")

class StockFinancialAnalysisKeyMetricTTMRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the TTM request.")

class StockFinancialAnalysisKeyMetricTTMResponse(StockFinancialAnalysisKeyMetricTTM):
    pass

# Batch request and response for financial ratios
class StockFinancialAnalysisRatioBatchRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StockFinancialPeriod = Field(..., description="The financial period for the request.")
    limit: int = Field(..., description="The limit for the number of results.")

class StockFinancialAnalysisRatioBatchResponse(BaseSchema):
    items: List[StockFinancialAnalysisRatio] = Field(..., description="List of financial ratios for the stock.")

class StockFinancialAnalysisRatioTTMRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the TTM request.")

class StockFinancialAnalysisRatioTTMResponse(StockFinancialAnalysisRatioTTM):
    pass