from typing import List
from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.common.stock import StockFinancialPeriod, StockFinancialStatement, StockFinancialAnalysisKeyMetrics, StockFinancialAnalysisKeyMetricsTTM, StockFinancialAnalysisRatios, StockFinancialAnalysisRatiosTTM

# Batch request and response for financial statements
class StockFinancialStatementBatchRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StockFinancialPeriod = Field(..., description="The financial period for the request.")
    limit: int = Field(..., description="The limit on the number of results returned.")

class StockFinancialStatementBatchResponse(BaseSchema):
    items: List[StockFinancialStatement] = Field(..., description="List of financial statements.")

# Batch request and response for financial key metrics
class StockFinancialAnalysisKeyMetricsBatchRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StockFinancialPeriod = Field(..., description="The financial period for the request.")
    limit: int = Field(..., description="The limit for the number of results.")

class StockFinancialAnalysisKeyMetricsBatchResponse(BaseSchema):
    items: List[StockFinancialAnalysisKeyMetrics] = Field(..., description="List of key metrics for the stock.")

class StockFinancialAnalysisKeyMetricsTTMRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the TTM request.")

class StockFinancialAnalysisKeyMetricsTTMResponse(StockFinancialAnalysisKeyMetricsTTM):
    pass

# Batch request and response for financial ratios
class StockFinancialAnalysisRatiosBatchRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StockFinancialPeriod = Field(..., description="The financial period for the request.")
    limit: int = Field(..., description="The limit for the number of results.")

class StockFinancialAnalysisRatiosBatchResponse(BaseSchema):
    items: List[StockFinancialAnalysisRatios] = Field(..., description="List of financial ratios for the stock.")

class StockFinancialAnalysisRatiosTTMRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the TTM request.")

class StockFinancialAnalysisRatiosTTMResponse(StockFinancialAnalysisRatiosTTM):
    pass