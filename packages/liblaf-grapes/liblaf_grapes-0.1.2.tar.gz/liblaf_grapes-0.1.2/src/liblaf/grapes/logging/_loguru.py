import contextlib
import inspect
import itertools
import logging
from collections.abc import Iterable, Sequence

import loguru
from environs import Env
from loguru import logger
from rich.console import Console

from liblaf import grapes

type Filter = "str | loguru.FilterDict | loguru.FilterFunction"


DEFAULT_FILTER: Filter = {
    "": "INFO",
    "__main__": "TRACE",
    "liblaf": "DEBUG",
}


DEFAULT_LEVELS: Sequence["loguru.LevelConfig"] = [
    {"name": "ICECREAM", "no": 15, "color": "<magenta><bold>", "icon": "🍦"}
]


class InterceptHandler(logging.Handler):
    """A logging handler that intercepts log messages and redirects them to Loguru.

    This handler is designed to be compatible with the standard logging framework and allows the use of Loguru for logging while maintaining compatibility with existing logging configurations.
    """

    # [Overview — loguru documentation](https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging)

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record.

        This function is called by the logging framework to handle a log record.
        It maps the standard logging levels to Loguru levels and finds the caller
        frame from where the log message originated. Finally, it logs the message
        using Loguru.

        Args:
            record: The log record to be emitted.
        """
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def add_level(
    name: str, no: int, color: str | None = None, icon: str | None = None
) -> None:
    """Add a new logging level to the logger.

    Args:
        name: The name of the new logging level.
        no: The numeric value of the new logging level.
        color: The color associated with the new logging level.
        icon: The icon associated with the new logging level.
    """
    with contextlib.suppress(ValueError):
        logger.level(name, no, color=color, icon=icon)


def setup_loguru_logging_intercept(
    level: int | str = logging.NOTSET, modules: Iterable[str] = ()
) -> None:
    """Sets up logging interception using Loguru.

    This function configures the logging module to use Loguru for handling log messages. It sets the logging level and replaces the handlers for the specified modules with an InterceptHandler that redirects log messages to Loguru.

    Args:
        level: The logging level to set.
        modules: A list of module names whose loggers should be intercepted.
    """
    # [loguru-logging-intercept/loguru_logging_intercept.py at f358b75ef4162ea903bf7a3298c22b1be83110da · MatthewScholefield/loguru-logging-intercept](https://github.com/MatthewScholefield/loguru-logging-intercept/blob/f358b75ef4162ea903bf7a3298c22b1be83110da/loguru_logging_intercept.py#L35C5-L42)
    logging.basicConfig(level=level, handlers=[InterceptHandler()])
    for logger_name in itertools.chain(("",), modules):
        mod_logger: logging.Logger = logging.getLogger(logger_name)
        mod_logger.handlers = [InterceptHandler(level=level)]
        mod_logger.propagate = False


def init_loguru(
    level: int | str = logging.NOTSET,
    filter: Filter | None = None,  # noqa: A002
    handlers: Sequence["loguru.HandlerConfig"] | None = None,
    levels: Sequence["loguru.LevelConfig"] | None = None,
) -> None:
    """Initialize the Loguru logger with specified configurations.

    Args:
        level: The logging level.
        filter: A filter to apply to the logger.
        handlers: A sequence of handler configurations.
        levels: A sequence of level configurations.
    """
    filter = filter or DEFAULT_FILTER  # noqa: A001
    if handlers is None:
        console: Console = grapes.logging_console()
        handlers: list[loguru.HandlerConfig] = [
            {
                "sink": lambda s: console.print(
                    s, end="", no_wrap=True, crop=False, overflow="ignore"
                ),
                "format": "[green]{time:YYYY-MM-DD HH:mm:ss.SSS}[/green] | [logging.level.{level}]{level: <8}[/logging.level.{level}] | [cyan]{name}[/cyan]:[cyan]{function}[/cyan]:[cyan]{line}[/cyan] - {message}",
                "filter": filter,
            }
        ]
        env: Env = grapes.environ.init_env()
        if fpath := env.path("LOGGING_FILE", None):
            handlers.append({"sink": fpath, "filter": filter, "mode": "w"})
        if fpath := env.path("LOGGING_JSONL", None):
            handlers.append(
                {"sink": fpath, "filter": filter, "serialize": True, "mode": "w"}
            )
    logger.configure(handlers=handlers)
    for lvl in levels or DEFAULT_LEVELS:
        add_level(**lvl)
    setup_loguru_logging_intercept(level=level)
