import logging
import typing as t

import structlog
from structlog.typing import EventDict, Processor


def get_logger(name=None) -> t.Any:
    """
    Returns a structlog-based logger.

    You can pass in a name if you want the logger to be named, e.g. '__name__'.

    Args:
        name (str): Module name to pass to the logger.

    Returns:
        A configured structlog logger.
    """
    return structlog.get_logger(name)


def avoid_color_message_logs(_, __, event_dict: EventDict) -> EventDict:
    """
    Uvicorn logs the message a second time in the extra `color_message`, but we don't
    need it. This processor drops the key from the event dict if it exists.

    Args:
        _: the logger.
        __: method name, such as INFO.
        event_dict (EventDict): Copy of the configured Context.

    Returns:
        The event_dict
    """
    event_dict.pop("color_message", None)
    return event_dict


def setup_logging(json_format_logs: bool = False, log_level: str = "INFO") -> None:
    """
    This function is used to set up the structlog configuration and integrate unicorn logs in structlog.

    Call it once at the start of the application.

    Args:
        json_format_logs (bool): It allows the user to display logs in JSON format.
        log_level (str): It allows the user to set the desired log level.
    """
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    common_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ExtraAdder(),
        avoid_color_message_logs,
        timestamper,
        structlog.processors.StackInfoRenderer(),
    ]

    if json_format_logs:
        common_processors.append(structlog.processors.format_exc_info)

    structlog.configure(
        processors=common_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    log_format_renderer: structlog.types.Processor

    if json_format_logs:
        log_format_renderer = structlog.processors.JSONRenderer()
    else:
        log_format_renderer = structlog.dev.ConsoleRenderer()

    other_logs_formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=common_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            log_format_renderer,
        ],
    )

    handler = logging.StreamHandler()
    handler.setFormatter(other_logs_formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level.upper())

    for _log in ["uvicorn", "uvicorn.error"]:
        logging.getLogger(_log).handlers.clear()
        logging.getLogger(_log).propagate = True

    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.access").propagate = False
