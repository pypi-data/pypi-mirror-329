# from .prices_utils.price_database_async import PriceDatabaseAsync
# import asyncio
# import pprint
# from .types.types import KlineIntervalEnum


# async def main():
#     uri = "postgresql://postgres:jnasijdK14AD@127.0.0.1:5432/prices_db"
#     price_db = PriceDatabaseAsync()

#     print("connecting")
#     price_db = await price_db.connect(uri, attempts=2, delay=5)
#     print("connected")

#     symbols = await price_db.get_futures_klines(
#         tickers=("OPUST",),
#         from_ts=0,
#         to_ts=1737538903000,
#         period=KlineIntervalEnum.ONE_MIN,
#         raw=False,
#     )

#     pprint.pprint(symbols)


# asyncio.run(main())
