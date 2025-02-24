from .types import Kline, TickTrade
from datetime import timedelta


def flat_ohlc_to_tick_prices(ohlc_prices: list[Kline]) -> list[TickTrade]:
    tick_prices: list[TickTrade] = []

    for ohlc in ohlc_prices:
        is_green = ohlc.open < ohlc.close
        tick_quantity = ohlc.volume / 4

        tick_prices.append(
            TickTrade(
                time=ohlc.open_time, symbol=ohlc.symbol, price=ohlc.open, quantity=tick_quantity
            )
        )
        tick_prices.append(
            TickTrade(
                time=ohlc.open_time + timedelta(seconds=15),
                symbol=ohlc.symbol,
                price=ohlc.low if is_green else ohlc.high,
                quantity=tick_quantity,
            )
        )
        tick_prices.append(
            TickTrade(
                time=ohlc.open_time + timedelta(seconds=30),
                symbol=ohlc.symbol,
                price=ohlc.high if is_green else ohlc.low,
                quantity=tick_quantity,
            )
        )
        tick_prices.append(
            TickTrade(
                time=ohlc.open_time + timedelta(seconds=45),
                symbol=ohlc.symbol,
                price=ohlc.close,
                quantity=tick_quantity,
            )
        )

    return tick_prices
