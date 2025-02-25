from pydantic import BaseModel
from typing import Literal
from enum import Enum


class PositionSideEnum(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    BOTH = "BOTH"


class SideEnum(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderTypeEnum(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_MARKET = "STOP_MARKET"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"
    TRAILING_STOP_MARKET = "TRAILING_STOP_MARKET"


class OrderStatusEnum(str, Enum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    EXPIRED_IN_MATCH = "EXPIRED_IN_MATCH"  # для STP - Self Trade Prevention (or STP) prevents orders of users, or the user's tradeGroupId to match against their own.


class TimeInForceEnum(str, Enum):
    GTC = "GTC"  # Good Till Cancel(GTC order valitidy is 1 year from placement)
    IOC = "IOC"  # Immediate or Cancel
    FOK = "FOK"  # Fill or Kill
    GTX = "GTX"  # Good Till Crossing (Post Only)
    GTD = "GTD"  # Good Till Date


class WorkingTypeEnum(str, Enum):
    MARK_PRICE = "MARK_PRICE"
    CONTRACT_PRICE = "CONTRACT_PRICE"


class IncomeTypeEnum(str, Enum):
    REALIZED_PNL = "REALIZED_PNL"
    FUNDING_FEE = "FUNDING_FEE"
    COMMISSION = "COMMISSION"
    TRANSFER = "TRANSFER"
    # Unused
    WELCOME_BONUS = "WELCOME_BONUS"
    INSURANCE_CLEAR = "INSURANCE_CLEAR"
    REFERRAL_KICKBACK = "REFERRAL_KICKBACK"
    COMMISSION_REBATE = "COMMISSION_REBATE"
    API_REBATE = "API_REBATE"
    CONTEST_REWARD = "CONTEST_REWARD"
    CROSS_COLLATERAL_TRANSFER = "CROSS_COLLATERAL_TRANSFER"
    OPTIONS_PREMIUM_FEE = "OPTIONS_PREMIUM_FEE"
    OPTIONS_SETTLE_PROFIT = "OPTIONS_SETTLE_PROFIT"
    INTERNAL_TRANSFER = "INTERNAL_TRANSFER"
    AUTO_EXCHANGE = "AUTO_EXCHANGE"
    DELIVERED_SETTELMENT = "DELIVERED_SETTELMENT"
    COIN_SWAP_DEPOSIT = "COIN_SWAP_DEPOSIT"
    COIN_SWAP_WITHDRAW = "COIN_SWAP_WITHDRAW"
    POSITION_LIMIT_INCREASE_FEE = "POSITION_LIMIT_INCREASE_FEE"


class OrderRespEnum(str, Enum):
    ACK = "ACK"  # default
    RESULT = "RESULT"


class AccountUpdateReasonEnum(str, Enum):
    ORDER = "ORDER"
    FUNDING_FEE = "FUNDING_FEE"
    #
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    WITHDRAW_REJECT = "WITHDRAW_REJECT"
    ADJUSTMENT = "ADJUSTMENT"
    INSURANCE_CLEAR = "INSURANCE_CLEAR"
    ADMIN_DEPOSIT = "ADMIN_DEPOSIT"
    ADMIN_WITHDRAW = "ADMIN_WITHDRAW"
    MARGIN_TRANSFER = "MARGIN_TRANSFER"
    MARGIN_TYPE_CHANGE = "MARGIN_TYPE_CHANGE"
    ASSET_TRANSFER = "ASSET_TRANSFER"
    OPTIONS_PREMIUM_FEE = "OPTIONS_PREMIUM_FEE"
    OPTIONS_SETTLE_PROFIT = "OPTIONS_SETTLE_PROFIT"
    AUTO_EXCHANGE = "AUTO_EXCHANGE"
    COIN_SWAP_DEPOSIT = "COIN_SWAP_DEPOSIT"
    COIN_SWAP_WITHDRAW = "COIN_SWAP_WITHDRAW"


# ------------------------------------------------------
# ------------------ Filters / Limits ------------------
# ------------------------------------------------------
class IntervalEnum(str, Enum):
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"


class RateLimitTypeEnum(str, Enum):
    ORDERS = "ORDERS"
    REQUEST_WEIGHT = "REQUEST_WEIGHT"


class SymbolFilterTypeEnum(str, Enum):
    PRICE_FILTER = "PRICE_FILTER"
    LOT_SIZE = "LOT_SIZE"
    MARKET_LOT_SIZE = "MARKET_LOT_SIZE"
    MAX_NUM_ORDERS = "MAX_NUM_ORDERS"
    MAX_NUM_ALGO_ORDERS = "MAX_NUM_ALGO_ORDERS"
    MIN_NOTIONAL = "MIN_NOTIONAL"
    PERCENT_PRICE = "PERCENT_PRICE"


class RateLimitType(BaseModel):
    interval: IntervalEnum
    intervalNum: int
    limit: int
    rateLimitType: RateLimitTypeEnum


class SymbolPriceFilterType(BaseModel):
    filterType: Literal[SymbolFilterTypeEnum.PRICE_FILTER]
    maxPrice: float
    minPrice: float
    tickSize: float


class SymbolLotSizeFilterType(BaseModel):
    filterType: Literal[SymbolFilterTypeEnum.LOT_SIZE]
    maxQty: float
    minQty: float
    stepSize: float


class SymbolMarketLotSizeFilterType(SymbolLotSizeFilterType):
    filterType: Literal[SymbolFilterTypeEnum.MARKET_LOT_SIZE]


class SymbolMaxOrdersFilterType(BaseModel):
    filterType: Literal[SymbolFilterTypeEnum.MAX_NUM_ORDERS]
    limit: int


class SymbolMaxAlgoOrdersFilterType(SymbolMaxOrdersFilterType):
    filterType: Literal[SymbolFilterTypeEnum.MAX_NUM_ALGO_ORDERS]
    limit: int


class SymbolMinNotionalFilterType(BaseModel):
    filterType: Literal[SymbolFilterTypeEnum.MIN_NOTIONAL]
    notional: float


class SymbolPercentPriceFilterType(BaseModel):
    filterType: Literal[SymbolFilterTypeEnum.PERCENT_PRICE]
    multiplierUp: float
    multiplierDown: float
    multiplierDecimal: int


class SymbolInfoType(BaseModel):
    symbol: str
    filters: list[
        SymbolPriceFilterType
        | SymbolLotSizeFilterType
        | SymbolMarketLotSizeFilterType
        | SymbolMaxOrdersFilterType
        | SymbolMaxAlgoOrdersFilterType
        | SymbolMinNotionalFilterType
        | SymbolPercentPriceFilterType
    ]
    # "pair": "BLZUSDT",
    # "contractType": "PERPETUAL",
    # "deliveryDate": 4133404800000,
    # "onboardDate": 1598252400000,
    # "status": "TRADING",
    # "maintMarginPercent": "2.5000",   # ignore
    # "requiredMarginPercent": "5.0000",  # ignore
    # "baseAsset": "BLZ",
    # "quoteAsset": "USDT",
    # "marginAsset": "USDT",
    # "pricePrecision": 5,    # please do not use it as tickSize
    # "quantityPrecision": 0, # please do not use it as stepSize
    # "baseAssetPrecision": 8,
    # "quotePrecision": 8,
    # "underlyingType": "COIN",
    # "underlyingSubType": ["STORAGE"],
    # "settlePlan": 0,
    # "triggerProtect": "0.15", # threshold for algo order with "priceProtect"
    # "liquidationFee": "0.010000",   # liquidation fee rate
    # "marketTakeBound": "0.30",  # the max price difference rate( from mark price) a market order can make
    # "OrderType": [
    #     "LIMIT",
    #     "MARKET",
    #     "STOP",
    #     "STOP_MARKET",
    #     "TAKE_PROFIT",
    #     "TAKE_PROFIT_MARKET",
    #     "TRAILING_STOP_MARKET"
    # ],
    # "timeInForce": [
    #     "GTC",
    #     "IOC",
    #     "FOK",
    #     "GTX"
    # ],
