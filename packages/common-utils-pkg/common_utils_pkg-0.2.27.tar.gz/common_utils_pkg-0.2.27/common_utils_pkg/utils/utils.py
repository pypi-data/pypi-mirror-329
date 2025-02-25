from common_utils_pkg.types import PositionSideEnum, SideEnum
from pathlib import Path
from datetime import datetime, date, timezone
import time
import math
import tarfile
import os.path


def get_now_timestamp():
    return to_timestamp(time.time())


def to_timestamp(date: datetime | float):
    ts = date
    if isinstance(ts, datetime):
        ts = ts.timestamp()

    return int(ts * 1000)


def to_datetime_from_timestamp(ts: int, tz: timezone | None = timezone.utc) -> datetime:
    return datetime.fromtimestamp(ts / 1000, tz=tz)


def find_files_by_pattern(directory: str, pattern: str) -> list[Path]:
    """
    Ищет файлы в папке, подходящие под заданный паттерн.

    :param directory: Путь к папке.
    :param pattern: Паттерн для поиска (например, '*.log', 'file_*.txt').
    :return: Список подходящих файлов.
    """
    dir_path = Path(directory)

    # Проверяем, существует ли папка
    if not dir_path.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Ищем файлы по паттерну
    matching_files = list(dir_path.glob(pattern))

    return matching_files


def cast_nan_to_none(value):
    if isinstance(value, (float, int)) and (math.isnan(value) or math.isinf(value)):
        return None

    return value


def validate_data(data):
    if isinstance(data, (float, int)):
        return cast_nan_to_none(data)

    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = validate_data(value)  # Заменяем nan и inf на None

    if isinstance(data, list):
        return [validate_data(item) for item in data]

    return data


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def make_tarfile(output_filename: str, source_dir: str):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


async def get_postgres_database_connection_async(
    database_uri: str, attempts: int = 5, delay: int = 10
):
    import asyncpg

    for attempt in range(attempts):
        try:
            return await asyncpg.connect(database_uri)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            if attempt < attempts - 1:
                time.sleep(delay)

    raise ConnectionError("Can not connect to database")


def get_postgres_db_connection(database_uri: str, attempts: int = 5, delay: int = 10):
    import psycopg2

    for attempt in range(attempts):
        try:
            return psycopg2.connect(database_uri)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            if attempt < attempts - 1:
                time.sleep(delay)

    raise ConnectionError("Can not connect to database")


def is_reduce_order(position_side: PositionSideEnum, side: SideEnum):
    return (
        position_side == PositionSideEnum.LONG
        and side == SideEnum.SELL
        or position_side == PositionSideEnum.SHORT
        and side == SideEnum.BUY
    )


def is_open_order(position_side: PositionSideEnum, side: SideEnum):
    return (
        position_side == PositionSideEnum.LONG
        and side == SideEnum.BUY
        or position_side == PositionSideEnum.SHORT
        and side == SideEnum.SELL
    )
