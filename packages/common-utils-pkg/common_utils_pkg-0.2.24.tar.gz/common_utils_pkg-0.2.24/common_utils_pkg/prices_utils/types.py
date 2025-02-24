from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from common_utils_pkg.types.binance_types import SideEnum


class MarketTypeEnum(str, Enum):
    SPOT = "spot"
    FUTURES = "futures"


str


class SymbolDataRange(BaseModel):
    symbol: str
    data_type: str
    start_date: datetime
    last_date: datetime
    last_loaded_date: datetime | None


class TickTrade(BaseModel):
    time: datetime
    symbol: str
    price: float
    quantity: float


class Kline(BaseModel):
    symbol: str
    open_time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class Funding(BaseModel):
    symbol: str
    time: datetime
    funding: float
    mark_price: float


class PremiumIndexKline(BaseModel):
    symbol: str
    time: datetime
    open: float
    high: float
    low: float
    close: float


class ExchangeMetrics(BaseModel):
    symbol: str
    time: datetime
    sum_open_interest: float | None
    sum_open_interest_value: float | None
    count_toptrader_long_short_ratio: float | None
    sum_toptrader_long_short_ratio: float | None
    count_long_short_ratio: float | None
    sum_taker_long_short_vol_ratio: float | None


class Liquidations(BaseModel):
    symbol: str
    time: datetime
    side: SideEnum
    price: float
    orig_qty: float
    avg_price: float
    last_fill_qty: float
    accumulated_fill_qty: float


class SymbolVolatility(BaseModel):
    symbol: str
    date: datetime
    long_trades: int
    short_trades: int
    last_level_price: float | None


class SymbolCurrentMetrics(BaseModel):
    symbol: str
    time: datetime
    index_price: float
    mark_price: float
    expected_funding: float
