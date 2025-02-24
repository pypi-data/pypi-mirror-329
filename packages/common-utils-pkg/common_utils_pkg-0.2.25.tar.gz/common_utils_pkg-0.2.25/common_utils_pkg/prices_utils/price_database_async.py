from .types import SymbolInfo, SymbolDataRange, Kline, TickTrade, Funding, MarketTypeEnum
from common_utils_pkg.types import KlineIntervalEnum
from common_utils_pkg.utils import (
    to_datetime_from_timestamp,
    get_postgres_database_connection_async,
)
from .formatters import (
    format_funding,
    format_ohlc_prices,
    format_premium_index,
    format_symbols,
    format_symbols_data_range,
    format_trades,
    format_exchange_metrics,
    format_liquidations,
    format_current_metrics,
    format_symbol_volatility,
)


class PriceDatabaseAsync:
    def __init__(self):
        self.prices_connection = None

    @classmethod
    async def connect(cls, database_uri: str, attempts: int, delay=10):
        """
        Асинхронный фабричный метод для создания экземпляра класса.
        """
        instance = cls()
        instance.prices_connection = await get_postgres_database_connection_async(
            database_uri=database_uri, attempts=attempts, delay=delay
        )
        return instance

    async def get_all_symbols(self) -> list[SymbolInfo]:
        rows = await self.prices_connection.fetch("SELECT * FROM symbols")
        return format_symbols(rows, raw=False)

    async def get_symbol(self, symbol: str) -> SymbolInfo | None:
        row = await self.prices_connection.fetchrow(
            "SELECT * FROM symbols WHERE symbol = $1 LIMIT 1",
            symbol,
        )
        return format_symbols([row], raw=False)[0] if row else None

    async def get_symbols_data_range(self, data_type: str) -> list[SymbolDataRange]:
        rows = await self.prices_connection.fetch(
            """SELECT
                s.symbol,
                d.data_type,
                d.start_date,
                d.last_date,
                d.last_loaded_date
            FROM symbols_data_range d JOIN symbols s ON d.symbol_id = s.id
            WHERE d.data_type = $1""",
            data_type,
        )
        return format_symbols_data_range(rows, raw=False)

    async def get_symbol_data_range(self, symbol: str, data_type: str) -> SymbolDataRange | None:
        row = await self.prices_connection.fetchrow(
            """SELECT
                s.symbol,
                d.data_type,
                d.start_date,
                d.last_date,
                d.last_loaded_date
            FROM symbols_data_range d JOIN symbols s ON d.symbol_id = s.id
            WHERE d.data_type = $1 AND s.symbol = $2""",
            data_type,
            symbol,
        )
        return format_symbols_data_range([row], raw=False)[0] if row else None

    async def get_spot_tick_prices(self, tickers: tuple[str], from_ts: int, to_ts: int, raw=False):
        return await self._get_tick_prices(
            tickers, from_ts, to_ts, type=MarketTypeEnum.SPOT, raw=raw
        )

    async def get_futures_tick_prices(
        self, tickers: tuple[str], from_ts: int, to_ts: int, raw=False
    ):
        return await self._get_tick_prices(
            tickers, from_ts, to_ts, type=MarketTypeEnum.FUTURES, raw=raw
        )

    async def get_spot_klines(
        self, tickers: tuple[str], from_ts: int, to_ts: int, period: KlineIntervalEnum, raw=False
    ):
        return await self._get_klines(
            tickers, from_ts, to_ts, period, type=MarketTypeEnum.SPOT, raw=raw
        )

    async def get_futures_klines(
        self, tickers: tuple[str], from_ts: int, to_ts: int, period: KlineIntervalEnum, raw=False
    ):
        return await self._get_klines(
            tickers, from_ts, to_ts, period, type=MarketTypeEnum.FUTURES, raw=raw
        )

    async def get_funding(
        self, tickers: tuple[str], from_ts: int, to_ts: int, raw=False
    ) -> list[dict] | list[Funding]:
        rows = await self.prices_connection.fetch(
            """SELECT
                s.symbol,
                f.time,
                f.funding,
                f.mark_price
            FROM funding f JOIN symbols s ON f.symbol_id = s.id
            WHERE s.symbol = ANY($1) AND f.time >= $2 AND f.time < $3
            ORDER BY f.time ASC""",
            tickers,
            to_datetime_from_timestamp(from_ts),
            to_datetime_from_timestamp(to_ts),
        )
        return format_funding(rows, raw)

    async def get_premium_index(self, tickers: tuple[str], from_ts: int, to_ts: int, raw=False):
        rows = await self.prices_connection.fetch(
            """SELECT
                s.symbol,
                p.time,
                p.open,
                p.high,
                p.low,
                p.close
            FROM premium_index_1m p JOIN symbols s ON p.symbol_id = s.id
            WHERE s.symbol = ANY($1) AND p.time >= $2 AND p.time < $3
            ORDER BY p.time ASC""",
            tickers,
            to_datetime_from_timestamp(from_ts),
            to_datetime_from_timestamp(to_ts),
        )

        return format_premium_index(rows, raw)

    async def get_exchange_metrics(self, tickers: tuple[str], from_ts: int, to_ts: int, raw=False):
        rows = await self.prices_connection.fetch(
            """SELECT
                s.symbol,
                e.time,
                e.sum_open_interest,
                e.sum_open_interest_value,
                e.count_toptrader_long_short_ratio,
                e.sum_toptrader_long_short_ratio,
                e.count_long_short_ratio,
                e.sum_taker_long_short_vol_ratio
            FROM exchange_metrics e JOIN symbols s ON e.symbol_id = s.id
            WHERE s.symbol = ANY($1) AND e.time >= $2 AND e.time < $3
            ORDER BY e.time ASC""",
            tickers,
            to_datetime_from_timestamp(from_ts),
            to_datetime_from_timestamp(to_ts),
        )

        return format_exchange_metrics(rows, raw)

    async def get_liquidations(self, tickers: tuple[str], from_ts: int, to_ts: int, raw=False):
        rows = await self.prices_connection.fetch(
            """SELECT
                s.symbol,
                l.time,
                l.is_buy_side,
                l.price,
                l.orig_qty,
                l.avg_price,
                l.last_fill_qty,
                l.accumulated_fill_qty
            FROM liquidations l JOIN symbols s ON l.symbol_id = s.id
            WHERE s.symbol = ANY($1) AND l.time >= $2 AND l.time < $3
            ORDER BY l.time ASC""",
            tickers,
            to_datetime_from_timestamp(from_ts),
            to_datetime_from_timestamp(to_ts),
        )

        return format_liquidations(rows, raw)

    async def get_symbol_current_metrics(
        self, tickers: tuple[str], from_ts: int, to_ts: int, raw=False
    ):
        rows = await self.prices_connection.fetch(
            """SELECT
                s.symbol,
                cm.time,
                cm.index_price,
                cm.mark_price,
                cm.expected_funding
            FROM symbol_current_metrics cm JOIN symbols s ON cm.symbol_id = s.id
            WHERE s.symbol = ANY($1) AND cm.time >= $2 AND cm.time < $3
            ORDER BY cm.time ASC""",
            tickers,
            to_datetime_from_timestamp(from_ts),
            to_datetime_from_timestamp(to_ts),
        )

        return format_current_metrics(rows, raw)

    async def _get_tick_prices(
        self, symbols: tuple[str], from_ts: int, to_ts: int, type: MarketTypeEnum, raw=False
    ) -> list[dict] | list[TickTrade]:
        tick_table_name = (
            "tick_spot_trades" if type is MarketTypeEnum.SPOT else "tick_futures_trades"
        )
        rows = await self.prices_connection.fetch(
            f"""SELECT
                t.time,
                s.symbol,
                t.price,
                t.quantity
            FROM {tick_table_name} t JOIN symbols s ON t.symbol_id = s.id
            WHERE s.symbol = ANY($1) AND t.time >= $2 AND t.time < $3
            ORDER BY t.time ASC""",
            tuple(symbols),
            to_datetime_from_timestamp(from_ts),
            to_datetime_from_timestamp(to_ts),
        )

        return format_trades(rows, raw)

    async def _get_klines(
        self,
        symbols: tuple[str],
        from_ts: int,
        to_ts: int,
        period: KlineIntervalEnum,
        type: MarketTypeEnum,
        raw=False,
    ) -> list[dict] | list[Kline]:
        period_type = period.value[-1]
        period_range = int(period.value[0:-1])

        if period_type == "m":
            klines_table_name = (
                "ohlc_spot_data_minute"
                if type is MarketTypeEnum.SPOT
                else "ohlc_futures_data_minute"
            )
        else:
            klines_table_name = (
                "ohlc_spot_data_hour" if type is MarketTypeEnum.SPOT else "ohlc_futures_data_hour"
            )

        need_to_aggregate = period not in [KlineIntervalEnum.ONE_MIN, KlineIntervalEnum.ONE_HOUR]

        rows = []
        if not need_to_aggregate:
            rows = await self.prices_connection.fetch(
                f"""SELECT
                        s.symbol,
                        k.date,
                        k.open,
                        k.high,
                        k.low,
                        k.close,
                        k.volume
                    FROM {klines_table_name} k JOIN symbols s ON k.symbol_id = s.id
                    WHERE s.symbol = ANY($1) AND k.date >= $2 AND k.date < $3
                    ORDER BY k.date ASC""",
                tuple(symbols),
                to_datetime_from_timestamp(from_ts),
                to_datetime_from_timestamp(to_ts),
            )
        else:
            bucket_period = str(period_range)
            if period_type == "m":
                bucket_period += " minute"
            elif period_type == "h":
                bucket_period += " hour"
            elif period_type == "d":
                bucket_period += " day"
            elif period_type == "w":
                bucket_period += " week"
            elif period_type == "M":
                bucket_period += " month"

            rows = await self.prices_connection.fetch(
                f"""SELECT s.symbol,
                        time_bucket('{bucket_period}', k.date) AS date_bucket,
                        FIRST(k.open, k.date) AS open,
                        MAX(k.high) AS high,
                        MIN(k.low) AS low,
                        LAST(k.close, k.date) AS close,
                        SUM(k.volume) AS volume
                    FROM {klines_table_name} k
                    JOIN symbols s ON k.symbol_id = s.id
                    WHERE s.symbol = ANY($1) AND k.date >= $2 AND k.date < $3
                    GROUP BY date_bucket, s.symbol
                    ORDER BY date_bucket ASC""",
                tuple(symbols),
                to_datetime_from_timestamp(from_ts),
                to_datetime_from_timestamp(to_ts),
            )

        return format_ohlc_prices(rows, raw)

    # ----- Indicators -----
    async def get_symbol_volatility(self, tickers: tuple[str], from_ts: int, to_ts: int, raw=False):
        rows = await self.prices_connection.fetch(
            """SELECT s.symbol,
                v.date,
                v.long_trades,
                v.short_trades,
                v.last_level_price
            FROM symbol_futures_volatility v
            JOIN symbols s ON v.symbol_id = s.id
            WHERE s.symbol = ANY($1) AND v.date >= $2 AND v.date < $3 ORDER BY date ASC""",
            tickers,
            to_datetime_from_timestamp(from_ts),
            to_datetime_from_timestamp(to_ts),
        )

        return format_symbol_volatility(rows, raw)
