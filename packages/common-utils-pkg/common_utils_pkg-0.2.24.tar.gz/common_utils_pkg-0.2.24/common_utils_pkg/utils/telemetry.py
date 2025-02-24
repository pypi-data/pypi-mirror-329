from common_utils_pkg import Logger
import time


def wait_for_collector_grpc(
    trace, span_processor, logger: Logger, endpoint: str, max_retries=5, delay=2
):
    # Создаём локальный TracerProvider (временный)
    # tracer_provider = TracerProvider()
    # trace.set_tracer_provider(tracer_provider)

    # # Настраиваем OTLP Exporter на gRPC
    # exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)

    # # SimpleSpanProcessor (чтобы при завершении сразу отправлялись спаны)
    # span_processor = SimpleSpanProcessor(exporter)
    # tracer_provider.add_span_processor(span_processor)

    tracer = trace.get_tracer("collector-check")

    for attempt in range(1, max_retries + 1):
        try:
            with tracer.start_as_current_span("check_collector_span"):
                pass  # Ничего не делаем, просто хотим отправить

            # или shutdown(), но тогда процессор более не работает
            if not span_processor.force_flush():
                raise Exception("Timeout exceeded")

            logger.info(f"Collector on '{endpoint}' is available.")
            return True
        except Exception as ex:
            logger.warning(f"[Attempt {attempt}/{max_retries}] Collector not available: {ex}.")
            time.sleep(delay)

    logger.error(f"Can not connect to Collector on '{endpoint}' after {max_retries} attempts.")
    return False
