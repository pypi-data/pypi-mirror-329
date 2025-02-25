from .logger import Logger
import traceback


def apply_migration(migration_name, migration_query, db_connection, logger: Logger):
    logger.debug(f"Start migration '{migration_name}'")

    # Подключение к базе данных
    conn = db_connection

    # Создание курсора для выполнения операций с базой данных
    cur = conn.cursor()

    # Создаем базу миграций, если ее нет
    cur.execute(
        """CREATE TABLE IF NOT EXISTS migrations (
            id SERIAL PRIMARY KEY,
            migration_name VARCHAR(255) NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
    )
    conn.commit()

    # Проверка, была ли уже применена эта миграция
    cur.execute("SELECT 1 FROM migrations WHERE migration_name = %s;", (migration_name,))
    if cur.fetchone():
        logger.info(f"Migration '{migration_name}' has already been applied.")
        cur.close()
        return

    try:
        # Выполнение SQL-запроса миграции
        cur.execute(migration_query)

        # Запись информации о выполненной миграции в таблицу migrations
        cur.execute("INSERT INTO migrations (migration_name) VALUES (%s);", (migration_name,))

        # Сохранение изменений
        conn.commit()
        logger.info(f"Migration '{migration_name}' applied successfully.")

    except Exception as e:
        # В случае ошибки откатить изменения
        conn.rollback()
        logger.error(f"Migration error occurred: {e}", notify=True)
        logger.warning(traceback.format_exc())

    finally:
        # Закрытие курсора и соединения
        cur.close()
