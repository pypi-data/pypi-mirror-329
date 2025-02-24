from .types import (
    SymbolDataRange,
    TickTrade,
    Kline,
    Funding,
    PremiumIndexKline,
    ExchangeMetrics,
    Liquidations,
    SymbolVolatility,
    SymbolCurrentMetrics,
)
from typing import overload, Literal


@overload
def format_trades(raw_trades: list, raw: Literal[True]) -> list[dict]:
    ...


@overload
def format_trades(raw_trades: list, raw: Literal[False]) -> list[TickTrade]:
    ...


@overload
def format_trades(raw_trades: list, raw: bool) -> list[dict] | list[TickTrade]:
    ...


def format_trades(raw_trades, raw=False) -> list[dict] | list[TickTrade]:
    if not raw_trades:
        return []

    trades = [
        {
            "time": t[0],
            "symbol": t[1],
            "price": t[2],
            "quantity": t[3],
        }
        for t in raw_trades
    ]

    if raw:
        return trades

    return [TickTrade.model_validate(trade) for trade in trades]


@overload
def format_symbols_data_range(raw_symbols_data_range: list, raw: Literal[True]) -> list[dict]:
    ...


@overload
def format_symbols_data_range(
    raw_symbols_data_range: list, raw: Literal[False]
) -> list[SymbolDataRange]:
    ...


@overload
def format_symbols_data_range(
    raw_symbols_data_range: list, raw: bool
) -> list[dict] | list[SymbolDataRange]:
    ...


def format_symbols_data_range(
    raw_symbols_data_range, raw=False
) -> list[dict] | list[SymbolDataRange]:
    if not raw_symbols_data_range:
        return []

    symbols_data = [
        {
            "data_type": t[0],
            "symbol": t[1],
            "start_date": t[2],
            "last_date": t[3],
            "last_loaded_date": t[4],
        }
        for t in raw_symbols_data_range
    ]

    if raw:
        return symbols_data

    return [SymbolDataRange.model_validate(symbol) for symbol in symbols_data]


@overload
def format_funding(raw_funding: list, raw: Literal[True]) -> list[dict]:
    ...


@overload
def format_funding(raw_funding: list, raw: Literal[False]) -> list[Funding]:
    ...


@overload
def format_funding(raw_funding: list, raw: bool) -> list[dict] | list[Funding]:
    ...


def format_funding(raw_funding, raw=False) -> list[dict] | list[Funding]:
    if not raw_funding:
        return []

    fundings = [
        {
            "time": t[0],
            "symbol": t[1],
            "funding": t[2],
            "mark_price": t[3],
        }
        for t in raw_funding
    ]

    if raw:
        return fundings

    return [Funding.model_validate(funding) for funding in fundings]


@overload
def format_premium_index(raw_premium_index: list, raw: Literal[True]) -> list[dict]:
    ...


@overload
def format_premium_index(raw_premium_index: list, raw: Literal[False]) -> list[PremiumIndexKline]:
    ...


@overload
def format_premium_index(
    raw_premium_index: list, raw: bool
) -> list[dict] | list[PremiumIndexKline]:
    ...


def format_premium_index(raw_premium_index, raw=False) -> list[dict] | list[PremiumIndexKline]:
    if not raw_premium_index:
        return []

    premium_indexes = [
        {
            "time": t[0],
            "symbol": t[1],
            "open": t[2],
            "high": t[3],
            "low": t[4],
            "close": t[5],
        }
        for t in raw_premium_index
    ]

    if raw:
        return premium_indexes

    return [PremiumIndexKline.model_validate(premium_index) for premium_index in premium_indexes]


@overload
def format_ohlc_prices(raw_ohlc: list, raw: Literal[True]) -> list[dict]:
    ...


@overload
def format_ohlc_prices(raw_ohlc: list, raw: Literal[False]) -> list[Kline]:
    ...


@overload
def format_ohlc_prices(raw_ohlc: list, raw: bool) -> list[dict] | list[Kline]:
    ...


def format_ohlc_prices(raw_ohlc, raw=False) -> list[dict] | list[Kline]:
    if not raw_ohlc:
        return []

    ohlc = [
        {
            "open_time": t[0],
            "symbol": t[1],
            "open": t[2],
            "high": t[3],
            "low": t[4],
            "close": t[5],
            "volume": t[6],
        }
        for t in raw_ohlc
    ]

    if raw:
        return ohlc

    return [Kline.model_validate(o) for o in ohlc]


@overload
def format_exchange_metrics(raw_metrics: list, raw: Literal[True]) -> list[dict]:
    ...


@overload
def format_exchange_metrics(raw_metrics: list, raw: Literal[False]) -> list[ExchangeMetrics]:
    ...


@overload
def format_exchange_metrics(raw_metrics: list, raw: bool) -> list[dict] | list[ExchangeMetrics]:
    ...


def format_exchange_metrics(raw_metrics, raw=False) -> list[dict] | list[ExchangeMetrics]:
    if not raw_metrics:
        return []

    metrics = [
        {
            "time": t[0],
            "symbol": t[1],
            "sum_open_interest": t[2],
            "sum_open_interest_value": t[3],
            "count_toptrader_long_short_ratio": t[4],
            "sum_toptrader_long_short_ratio": t[5],
            "count_long_short_ratio": t[6],
            "sum_taker_long_short_vol_ratio": t[7],
        }
        for t in raw_metrics
    ]

    if raw:
        return metrics

    return [ExchangeMetrics.model_validate(metric) for metric in metrics]


@overload
def format_liquidations(raw_liquidation: list, raw: Literal[True]) -> list[dict]:
    ...


@overload
def format_liquidations(raw_liquidation: list, raw: Literal[False]) -> list[Liquidations]:
    ...


@overload
def format_liquidations(raw_liquidation: list, raw: bool) -> list[dict] | list[Liquidations]:
    ...


def format_liquidations(raw_liquidation, raw=False) -> list[dict] | list[Liquidations]:
    if not raw_liquidation:
        return []

    liquidations = [
        {
            "time": t[0],
            "symbol": t[1],
            "side": "BUY" if t[2] else "SELL",
            "price": t[3],
            "orig_qty": t[4],
            "avg_price": t[5],
            "last_fill_qty": t[6],
            "accumulated_fill_qty": t[7],
        }
        for t in raw_liquidation
    ]

    if raw:
        return liquidations

    return [Liquidations.model_validate(liq) for liq in liquidations]


@overload
def format_symbol_volatility(raw_volatility: list, raw: Literal[True]) -> list[dict]:
    ...


@overload
def format_symbol_volatility(raw_volatility: list, raw: Literal[False]) -> list[SymbolVolatility]:
    ...


@overload
def format_symbol_volatility(
    raw_volatility: list, raw: bool
) -> list[dict] | list[SymbolVolatility]:
    ...


def format_symbol_volatility(raw_volatility, raw=False) -> list[dict] | list[SymbolVolatility]:
    if not raw_volatility:
        return []

    volatility = [
        {
            "date": t[0],
            "symbol": t[1],
            "long_trades": t[2],
            "short_trades": t[3],
            "last_level_price": t[4],
        }
        for t in raw_volatility
    ]

    if raw:
        return volatility

    return [SymbolVolatility.model_validate(vol) for vol in volatility]


@overload
def format_current_metrics(raw_current_metrics: list, raw: Literal[True]) -> list[dict]:
    ...


@overload
def format_current_metrics(
    raw_current_metrics: list, raw: Literal[False]
) -> list[SymbolCurrentMetrics]:
    ...


@overload
def format_current_metrics(
    raw_current_metrics: list, raw: bool
) -> list[dict] | list[SymbolCurrentMetrics]:
    ...


def format_current_metrics(
    raw_current_metrics: list, raw=False
) -> list[dict] | list[SymbolCurrentMetrics]:
    if not raw_current_metrics:
        return []

    current_metrics = [
        {
            "time": item[0],
            "symbol": item[1],
            "index_price": item[2],
            "mark_price": item[3],
            "expected_funding": item[4],
        }
        for item in raw_current_metrics
    ]

    if raw:
        return current_metrics

    return [SymbolCurrentMetrics.model_validate(metrics) for metrics in current_metrics]
