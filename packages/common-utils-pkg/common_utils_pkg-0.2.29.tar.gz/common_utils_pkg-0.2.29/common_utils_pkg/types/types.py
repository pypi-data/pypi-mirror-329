from pydantic import BaseModel
from enum import Enum


class KlineIntervalEnum(str, Enum):
    ONE_MIN = "1m"
    FIVE_MINS = "5m"
    FIFTEEN_MINS = "15m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    SIX_HOURS = "6h"
    EIGHT_HOURS = "8h"
    TWELVE_HOURS = "12h"
    ONE_DAY = "1d"
    THREE_DAYS = "3d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1M"


KlineIntervalDurationSeconds = {
    KlineIntervalEnum.ONE_MIN: 60,
    KlineIntervalEnum.FIVE_MINS: 300,
    KlineIntervalEnum.FIFTEEN_MINS: 900,
    KlineIntervalEnum.ONE_HOUR: 3600,
    KlineIntervalEnum.FOUR_HOURS: 3600 * 4,
    KlineIntervalEnum.SIX_HOURS: 3600 * 6,
    KlineIntervalEnum.EIGHT_HOURS: 3600 * 8,
    KlineIntervalEnum.TWELVE_HOURS: 3600 * 12,
    KlineIntervalEnum.ONE_DAY: 3600 * 24,
    KlineIntervalEnum.THREE_DAYS: 3600 * 24 * 3,
    KlineIntervalEnum.ONE_WEEK: 3600 * 24 * 7,
    KlineIntervalEnum.ONE_MONTH: 3600 * 24 * 30,
}


class CommonRolesEnum(str, Enum):
    PRICES_READ = "prices/read"
    INDICATORS_READ = "indicators/read"
    BACKTEST_READ = "backtest/read"
    BACKTEST_WRITE = "backtest/write"
    TRADE_BOT_READ = "trade_bot/read"
    TRADE_BOT_WRITE = "trade_bot/write"


class BasicJWTToken(BaseModel):
    iss: str  # issuer
    sub: str  # login
    iat: int
    exp: int


class AccessToken(BasicJWTToken):
    roles: list[str]


class RefreshToken(BasicJWTToken):
    pass
