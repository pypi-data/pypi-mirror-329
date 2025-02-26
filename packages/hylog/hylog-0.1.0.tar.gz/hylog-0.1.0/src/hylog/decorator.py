from __future__ import annotations

import functools
import logging
import sys
import time

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar


if TYPE_CHECKING:
    from collections.abc import Callable


def get_debug_decorator(
    logger: logging.Logger, log_level: str | None = None
) -> Callable[..., Any]:
    # Set the level to the log_level if it exists otherwise use the logger.getLevelName
    # to retrieve the corresponding int value for the log level
    level = getattr(logger, log_level.upper()) if log_level else logger.level

    def decorator(func: Callable[..., Any]) -> Any:
        """Print the function signature and return value"""

        @functools.wraps(func)
        def wrapper_debug(*args: Any, **kwargs: Any) -> Any:
            args_repr = [f"{a!r}" for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            logger.log(level, f"Calling {func.__name__}({signature})")

            value = func(*args, **kwargs)
            logger.log(level, f"{func.__name__}() returned {value!r}")

            return value

        return wrapper_debug

    return decorator


def get_perf_timer_decorator(
    logger: logging.Logger, log_level: str | None = None
) -> Callable[..., Any]:
    # Set the level to the log_level if it exists otherwise use the logger.getLevelName
    # to retrieve the corresponding int value for the log level
    level = logger.level
    if log_level:
        level = logging.getLevelName(log_level.upper())

    def decorator(func: Callable[..., Any]) -> Any:
        """Print the function signature and return value"""

        @functools.wraps(func)
        def wrapper_debug(*args: Any, **kwargs: Any) -> Any:
            args_repr = [f"{a!r}" for a in args]

            # kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]

            signature = ", ".join(args_repr + kwargs_repr)

            logger.log(level, f"Calling {func.__name__}({signature})")

            start_time = time.perf_counter()
            value = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            logger.log(level, f"{func.__name__}() returned {value!r}")
            logger.log(level, f"{total_time:.4f} seconds for Function {func.__name__}")

            return value

        return wrapper_debug

    return decorator
