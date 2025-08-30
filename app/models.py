from pydantic import BaseModel
from typing import List

class OptionParams(BaseModel):
    spot: float
    strike: float
    maturity: float
    interest_rate: float
    volatility: float

class PricesResponse(BaseModel):
    prices: List[float]
