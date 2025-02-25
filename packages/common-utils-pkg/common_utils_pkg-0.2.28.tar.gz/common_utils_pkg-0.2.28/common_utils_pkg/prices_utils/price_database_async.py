from .types import SymbolDataRange, Kline, TickTrade, Funding, MarketTypeEnum
from common_utils_pkg.types import KlineIntervalEnum
from common_utils_pkg.utils import to_datetime_from_timestamp
from .formatters import (
    format_funding,
    format_ohlc_prices,
    format_premium_index,
    format_symbols_data_range,
    format_trades,
    format_exchange_metrics,
    format_liquidations,
    format_current_metrics,
    format_symbol_volatility,
)
import clickhouse_connect
import asyncio

# pip install clickhouse-connect


class PriceDatabaseAsync:
    def __init__(self, max_workers: int = 10):
        self.client = None
        self.semaphore = asyncio.Semaphore(max_workers)

    async def connect(
        self,
        database_name: str,
        host: str,
        port: int,
        username: str,
        password: str,
        secure=False,
    ):
        self.db_name = database_name
        self.client = await clickhouse_connect.get_async_client(
            host=host,
            port=port,
            username=username,
            password=password,
            database=self.db_name,
            secure=secure,
        )

    async def get_symbols_data_ranges(self, data_type: str) -> list[SymbolDataRange]:
        rows = await self.client.query(
            """SELECT data_type, symbol, start_date, last_date, last_loaded_date FROM symbols_data_range
                WHERE data_type = %(data_type)s""",
            parameters={"data_type": data_type},
        )
        return format_symbols_data_range(list(rows.result_rows), raw=False)

    async def get_symbol_data_range(self, symbol: str, data_type: str) -> SymbolDataRange | None:
        rows = await self.client.query(
            """SELECT data_type, symbol, start_date, last_date, last_loaded_date FROM symbols_data_range
                WHERE data_type = %(data_type)s AND symbol = %(symbol)s LIMIT 1""",
            parameters={"data_type": data_type, "symbol": symbol},
        )
        return (
            format_symbols_data_range(list(rows.result_rows), raw=False)[0]
            if rows.row_count
            else None
        )

    async def get_spot_tick_prices(
        self, tickers: tuple[str, ...], from_ts: int, to_ts: int, raw=False
    ):
        return await self._get_tick_prices(
            tickers, from_ts, to_ts, type=MarketTypeEnum.SPOT, raw=raw
        )

    async def get_futures_tick_prices(
        self, tickers: tuple[str, ...], from_ts: int, to_ts: int, raw=False
    ):
        return await self._get_tick_prices(
            tickers, from_ts, to_ts, type=MarketTypeEnum.FUTURES, raw=raw
        )

    async def get_spot_klines(
        self,
        tickers: tuple[str, ...],
        from_ts: int,
        to_ts: int,
        period: KlineIntervalEnum,
        raw=False,
    ):
        return await self._get_klines(
            tickers, from_ts, to_ts, period, type=MarketTypeEnum.SPOT, raw=raw
        )

    async def get_futures_klines(
        self,
        tickers: tuple[str, ...],
        from_ts: int,
        to_ts: int,
        period: KlineIntervalEnum,
        raw=False,
    ):
        return await self._get_klines(
            tickers, from_ts, to_ts, period, type=MarketTypeEnum.FUTURES, raw=raw
        )

    async def get_funding(
        self, tickers: tuple[str, ...], from_ts: int, to_ts: int, raw=False
    ) -> list[dict] | list[Funding]:
        rows = await self.client.query(
            """SELECT time, symbol, funding, mark_price,
                FROM funding 
                WHERE symbol IN %(tickers)s AND time >= %(from_ts)s AND time < %(to_ts)s
                ORDER BY time ASC""",
            parameters={
                "tickers": tickers,
                "from_ts": to_datetime_from_timestamp(from_ts),
                "to_ts": to_datetime_from_timestamp(to_ts),
            },
        )
        return format_funding(list(rows.result_rows), raw)

    async def get_premium_index(
        self, tickers: tuple[str, ...], from_ts: int, to_ts: int, raw=False
    ):
        rows = await self.client.query(
            """SELECT time, symbol, open, high, low, close
                FROM premium_index_1m 
                WHERE symbol IN %(tickers)s AND time >= %(from_ts)s AND time < %(to_ts)s
                ORDER BY time ASC""",
            parameters={
                "tickers": tickers,
                "from_ts": to_datetime_from_timestamp(from_ts),
                "to_ts": to_datetime_from_timestamp(to_ts),
            },
        )
        return format_premium_index(list(rows.result_rows), raw)

    async def get_exchange_metrics(
        self, tickers: tuple[str, ...], from_ts: int, to_ts: int, raw=False
    ):
        rows = await self.client.query(
            """SELECT
                    time,
                    symbol,
                    sum_open_interest,
                    sum_open_interest_value,
                    count_toptrader_long_short_ratio,
                    sum_toptrader_long_short_ratio,
                    count_long_short_ratio,
                    sum_taker_long_short_vol_ratio
                FROM exchange_metrics 
                WHERE symbol IN %(tickers)s AND time >= %(from_ts)s AND time < %(to_ts)s
                ORDER BY time ASC""",
            parameters={
                "tickers": tickers,
                "from_ts": to_datetime_from_timestamp(from_ts),
                "to_ts": to_datetime_from_timestamp(to_ts),
            },
        )
        return format_exchange_metrics(list(rows.result_rows), raw)

    async def get_liquidations(self, tickers: tuple[str, ...], from_ts: int, to_ts: int, raw=False):
        rows = await self.client.query(
            """SELECT
                    time,
                    symbol,
                    is_buy_side,
                    price,
                    orig_qty,
                    avg_price,
                    last_fill_qty,
                    accumulated_fill_qty
                FROM liquidations
                WHERE symbol IN %(tickers)s AND time >= %(from_ts)s AND time < %(to_ts)s
                ORDER BY time ASC""",
            parameters={
                "tickers": tickers,
                "from_ts": to_datetime_from_timestamp(from_ts),
                "to_ts": to_datetime_from_timestamp(to_ts),
            },
        )
        return format_liquidations(list(rows.result_rows), raw)

    async def get_symbol_current_metrics(
        self, tickers: tuple[str, ...], from_ts: int, to_ts: int, raw=False
    ):
        rows = await self.client.query(
            """SELECT
                    time,
                    symbol,
                    index_price,
                    mark_price,
                    expected_funding_rate
                FROM symbol_current_metrics
                WHERE symbol IN %(tickers)s AND time >= %(from_ts)s AND time < %(to_ts)s
                ORDER BY time ASC""",
            parameters={
                "tickers": tickers,
                "from_ts": to_datetime_from_timestamp(from_ts),
                "to_ts": to_datetime_from_timestamp(to_ts),
            },
        )
        return format_current_metrics(list(rows.result_rows), raw)

    async def _get_tick_prices(
        self, symbols: tuple[str, ...], from_ts: int, to_ts: int, type: MarketTypeEnum, raw=False
    ) -> list[dict] | list[TickTrade]:
        tick_table_name = (
            "tick_spot_trades" if type is MarketTypeEnum.SPOT else "tick_futures_trades"
        )
        rows = await self.client.query(
            f"""SELECT time, symbol, price, quantity
                FROM {tick_table_name} 
                WHERE symbol IN %(tickers)s AND time >= %(from_ts)s AND time < %(to_ts)s
                ORDER BY time ASC""",
            parameters={
                "tickers": symbols,
                "from_ts": to_datetime_from_timestamp(from_ts),
                "to_ts": to_datetime_from_timestamp(to_ts),
            },
        )
        return format_trades(list(rows.result_rows), raw)

    async def _get_klines(
        self,
        symbols: tuple[str, ...],
        from_ts: int,
        to_ts: int,
        period: KlineIntervalEnum,
        type: MarketTypeEnum,
        raw=False,
    ) -> list[dict] | list[Kline]:
        klines_table_name = "spot_kline_1m" if type is MarketTypeEnum.SPOT else "futures_kline_1m"

        rows = []
        if period == KlineIntervalEnum.ONE_MIN:
            rows = await self.client.query(
                f"""SELECT
                        open_ts, symbol, open, high, low, close, volume
                    FROM {klines_table_name} 
                    WHERE symbol IN %(tickers)s AND open_ts >= %(from_ts)s AND open_ts < %(to_ts)s
                    ORDER BY open_ts ASC""",
                parameters={
                    "tickers": symbols,
                    "from_ts": to_datetime_from_timestamp(from_ts),
                    "to_ts": to_datetime_from_timestamp(to_ts),
                },
            )
        else:
            period_to_interval_map = {
                KlineIntervalEnum.ONE_MIN: "1 minute",
                KlineIntervalEnum.FIVE_MINS: "5 minute",
                KlineIntervalEnum.FIFTEEN_MINS: "15 minute",
                KlineIntervalEnum.ONE_HOUR: "1 hour",
                KlineIntervalEnum.FOUR_HOURS: "4 hour",
                KlineIntervalEnum.SIX_HOURS: "6 hour",
                KlineIntervalEnum.EIGHT_HOURS: "8 hour",
                KlineIntervalEnum.TWELVE_HOURS: "12 hour",
                KlineIntervalEnum.ONE_DAY: "1 day",
                KlineIntervalEnum.THREE_DAYS: "3 day",
            }

            if period == KlineIntervalEnum.ONE_WEEK:
                agg_function = "toStartOfWeek(open_ts)"
            elif period == KlineIntervalEnum.ONE_MONTH:
                agg_function = "toStartOfMonth(open_ts)"
            else:
                interval = period_to_interval_map[period]
                agg_function = f"toStartOfInterval(open_ts, INTERVAL {interval})"

            rows = await self.client.query(
                f"""SELECT
                        {agg_function} AS interval_ts,
                        symbol,
                        argMin(open, open_ts) AS open,  
                        max(high) AS high,              
                        min(low) AS low,                
                        argMax(close, open_ts) AS close, 
                        sum(volume) AS volume            
                    FROM {klines_table_name} 
                    WHERE symbol IN %(tickers)s AND interval_ts >= %(from_ts)s AND interval_ts < %(to_ts)s
                    GROUP BY interval_ts, symbol
                    ORDER BY interval_ts ASC;""",
                parameters={
                    "tickers": symbols,
                    "from_ts": to_datetime_from_timestamp(from_ts),
                    "to_ts": to_datetime_from_timestamp(to_ts),
                },
            )
        return format_ohlc_prices(list(rows.result_rows), raw)

    # ----- Indicators -----
    async def get_symbol_volatility(
        self, tickers: tuple[str, ...], from_ts: int, to_ts: int, raw=False
    ):
        rows = await self.client.query(
            """SELECT 
                    date,
                    symbol,
                    long_trades,
                    short_trades,
                    last_level_price
                FROM symbol_futures_volatility 
                WHERE symbol IN %(tickers)s AND date >= %(from_ts)s AND date < %(to_ts)s
                ORDER BY date ASC""",
            parameters={
                "tickers": tickers,
                "from_ts": to_datetime_from_timestamp(from_ts),
                "to_ts": to_datetime_from_timestamp(to_ts),
            },
        )
        return format_symbol_volatility(list(rows.result_rows), raw)
