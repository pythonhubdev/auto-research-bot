import logging
import sys
from typing import Any, Union

from loguru import logger
from opentelemetry.trace import INVALID_SPAN, INVALID_SPAN_CONTEXT, get_current_span

from auto_research_bot.config.settings import get_settings

settings = get_settings()


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            if frame.f_back:
                frame = frame.f_back
                depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


class CustomFormatter:
    def __call__(self, record: dict[str, Any]) -> str:
        span = get_current_span()
        record["extra"]["span_id"] = 0
        record["extra"]["trace_id"] = 0
        if span != INVALID_SPAN:
            span_context = span.get_span_context()
            if span_context != INVALID_SPAN_CONTEXT:
                record["extra"]["span_id"] = format(span_context.span_id, "016x")
                record["extra"]["trace_id"] = format(span_context.trace_id, "032x")

        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
            "| <level> {level: <4} </level> "
            "| <magenta>trace_id={extra[trace_id]}</magenta> "
            "| <blue>span_id={extra[span_id]}</blue> "
        )
        if record["function"]:
            log_format += "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
        log_format += "- <level>{message}</level>\n"

        if record["exception"]:
            log_format += "{exception}\n"
        return log_format


def configure_logging() -> None:
    intercept_handler = InterceptHandler()
    intercept_handler.setFormatter(CustomFormatter())  # type: ignore
    logging.basicConfig(
        handlers=[intercept_handler],
        level=logging.NOTSET,
    )

    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": settings.LOG_LEVEL,
                "format": CustomFormatter(),
            },
        ],
    )
