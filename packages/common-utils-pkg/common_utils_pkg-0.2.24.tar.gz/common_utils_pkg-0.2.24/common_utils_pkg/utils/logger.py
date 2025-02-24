from .notifications import NotificationHandler
from loguru import logger as loguru_logger
import sys


DEFAULT_CONSOLE_FORMATTER = "<g><n>{time:YYYY-MM-DD HH:mm:ss.SSSSSS!UTC}</></> <lvl>[{level:7}] {extra[service]}[{extra[prefix]}] <i>{thread.name}</> <d><lc>{file}</>:<blue>{line}</></>: <n>{message}</></>"
DEFAULT_FILE_FORMATTER = "{time:YYYY-MM-DD HH:mm:ss.SSSSSS!UTC} [{level:7}] {extra[service]}[{extra[prefix]}] {thread.name} {file}:{line}: {message}"
DEFAULT_NOTIFICATION_FORMATTER = "{level.icon} {extra[service]} <i>{extra[prefix]}</i>: {message}"
DEFAULT_DEPTH = 1

global_logger = None


def common_filter(record):
    should_pass = "special" not in record["extra"] or not record["extra"]["special"]
    return should_pass


def get_custom_filter(service_name):
    def _filter(record):
        should_pass = "special" in record["extra"] and record["extra"]["special"] == service_name
        return should_pass

    return _filter


def notification_filter(record):
    if "notify" in record["extra"] and record["extra"]["notify"]:
        return True
    return False


class CustomLoggerWrapper:
    def __init__(self, base_logger, sink_id: int | None = None, depth=DEFAULT_DEPTH, **kwargs):
        """
        Создает обертку вокруг логгера Loguru с кастомными методами.
        :param base_logger: Экземпляр базового логгера Loguru.
        """
        self.depth = depth
        self.logger = base_logger

        self.extras = kwargs
        self.sink_id = sink_id

    def info(self, message, notify=False, *args, **kwargs):
        """
        Переопределенный метод info с дополнительным параметром notify.
        :param message: Сообщение для логгирования.
        :param notify: Если True, добавляет уведомление в extra.
        :param args: Дополнительные аргументы для логгера.
        :param kwargs: Дополнительные параметры для логгера.
        """
        self.logger.opt(depth=self.depth).bind(notify=notify, **self.extras).info(
            message, *args, **kwargs
        )

    def warning(self, message, notify=False, *args, **kwargs):
        """
        Пример переопределения warning.
        """
        self.logger.opt(depth=self.depth).bind(notify=notify, **self.extras).warning(
            message, *args, **kwargs
        )

    def error(self, message, notify=False, *args, **kwargs):
        self.logger.opt(depth=self.depth).bind(notify=notify, **self.extras).error(message)

    def debug(self, message, notify=False, *args, **kwargs):
        self.logger.opt(depth=self.depth).bind(notify=notify, **self.extras).debug(message)

    def trace(self, message, notify=False, *args, **kwargs):
        self.logger.opt(depth=self.depth).bind(notify=notify, **self.extras).trace(message)

    def success(self, message, notify=False, *args, **kwargs):
        self.logger.opt(depth=self.depth).bind(notify=notify, **self.extras).success(message)

    def critical(self, message, notify=True, *args, **kwargs):
        self.logger.opt(depth=self.depth).bind(notify=notify, **self.extras).critical(message)

    def create_prefix(self, prefix):
        new_logger = self.logger.bind(prefix=f"{prefix}")
        return CustomLoggerWrapper(new_logger, depth=self.depth, **self.extras)

    def __getattr__(self, name):
        """
        Делегирует все остальные вызовы методам базового логгера.
        """
        return getattr(self.logger, name)

    def __del__(self):
        if self.sink_id:
            self.logger.remove(self.sink_id)


class Logger:
    def __init__(
        self,
        logging_service: str,
        diagnose=False,
        compression=None,
        rotation="50 Mb",
        retention=None,
        enable_file_log=True,
        enable_console_log=True,
        enable_notifications=False,
        telegram_api_key=None,
        telegram_chat_ids=None,
        file_log_level="TRACE",
        console_log_level="INFO",
        notification_log_level="INFO",
        file_formatter=DEFAULT_FILE_FORMATTER,
        console_formatter=DEFAULT_CONSOLE_FORMATTER,
        notification_formatter=DEFAULT_NOTIFICATION_FORMATTER,
    ):
        if not logging_service:
            raise Exception("logging_service parameter is not specified")

        self.service_name = logging_service

        global global_logger
        if global_logger:
            raise Exception("Only one Logger should be created")
        else:
            global_logger = loguru_logger

        self.logger = global_logger.bind(service=self.service_name, prefix="main")
        self.logger.configure(handlers=[])

        self.file_log_level = file_log_level
        self.file_formatter = file_formatter
        self.diagnose = diagnose
        self.rotation = rotation
        self.retention = retention
        self.compression = compression

        if enable_file_log:
            file_sink_id = self.logger.add(
                sink="logs/" + self.service_name + "_{time}.log",
                level=self.file_log_level,
                format=self.file_formatter,
                diagnose=self.diagnose,
                backtrace=True,
                catch=True,
                enqueue=True,
                rotation=self.rotation,
                retention=self.retention,
                compression=self.compression,
                filter=common_filter,
            )

        # logging to console
        if enable_console_log:
            console_sink_id = self.logger.add(
                sink=sys.stdout,
                level=console_log_level,
                format=console_formatter,
                colorize=True,
                backtrace=True,
                diagnose=self.diagnose,
                catch=True,
                enqueue=True,
                # filter=common_filter,
            )

        self.notifier = None
        if enable_notifications:
            if telegram_chat_ids and telegram_api_key:
                self.notifier = NotificationHandler(
                    telegram_chat_ids=telegram_chat_ids,
                    telegram_api_key=telegram_api_key,
                    enabled=True,
                )
                self.logger.add(
                    sink=self.notifier.send_notification,
                    format=notification_formatter,
                    level=notification_log_level,
                    filter=notification_filter,
                )
            else:
                self.logger.warning(f"API keys not set for notificator")

        self.logger = CustomLoggerWrapper(self.logger)
        self.logger.info(f"----------------- Starting logger: {logging_service} -----------------")

    def create_extra_logger(
        self,
        service_name,
        file_log_level: str | None = None,
        file_formatter: str | None = None,
        rotation: str | None = None,
        retention: str | None = None,
        compression: str | None = None,
        backtrace=True,
        diagnose=False,
        catch=False,
        enqueue=True,
    ) -> CustomLoggerWrapper:
        new_logger = self.logger.bind(service=service_name)
        file_sink_id = new_logger.add(
            sink="logs/" + service_name + "_{time}.log",
            level=file_log_level or self.file_log_level,
            format=file_formatter or self.file_formatter,
            backtrace=backtrace or self.ba,
            diagnose=diagnose,
            catch=catch,
            enqueue=enqueue,
            rotation=rotation or self.rotation,
            retention=retention or self.retention,
            compression=compression or self.compression,
            filter=get_custom_filter(service_name),
        )

        new_logger = CustomLoggerWrapper(new_logger, special=service_name, sink_id=file_sink_id)
        new_logger.info(f"-------------- Starting extra logger: {service_name} --------------")
        return new_logger

    def shutdown(self):
        if self.notifier:
            self.notifier.shutdown()

    def __getattr__(self, name):
        return getattr(self.logger, name)

    def __del__(self):
        self.shutdown()


def get_logger():
    global global_logger
    if not global_logger:
        return loguru_logger
    return global_logger
