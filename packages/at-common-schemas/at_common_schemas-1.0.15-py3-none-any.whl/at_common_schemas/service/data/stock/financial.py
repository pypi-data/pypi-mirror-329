from typing import List
from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.common.stock import (
    StockFinancialPeriod, StockFinancialAnalysisKeyMetric, 
    StockFinancialStatementCashFlow, StockFinancialStatementBalanceSheet, StockFinancialStatementIncome,
    StockFinancialAnalysisKeyMetricTTM, StockFinancialAnalysisRatio, StockFinancialAnalysisRatioTTM
)

# Batch request and response for financial cash flows statements
class StockFinancialStatementCashFlowBatchRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StockFinancialPeriod = Field(..., description="The financial period for the request.")
    limit: int = Field(..., description="The limit on the number of results returned.")

class StockFinancialStatementCashFlowBatchResponse(BaseSchema):
    items: List[StockFinancialStatementCashFlow] = Field(..., description="List of financial cash flows statements.")

# Batch request and response for financial balance sheets statements
class StockFinancialStatementBalanceSheetBatchRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StockFinancialPeriod = Field(..., description="The financial period for the request.")
    limit: int = Field(..., description="The limit on the number of results returned.")

class StockFinancialStatementBalanceSheetBatchResponse(BaseSchema):
    items: List[StockFinancialStatementBalanceSheet] = Field(..., description="List of financial balance sheets statements.")

# Batch request and response for financial income statements
class StockFinancialStatementIncomeBatchRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StockFinancialPeriod = Field(..., description="The financial period for the request.")
    limit: int = Field(..., description="The limit on the number of results returned.")

class StockFinancialStatementIncomeBatchResponse(BaseSchema):
    items: List[StockFinancialStatementIncome] = Field(..., description="List of financial income statements.")

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