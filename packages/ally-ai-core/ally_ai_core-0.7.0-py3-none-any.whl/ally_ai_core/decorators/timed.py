import logging
import inspect
from functools import wraps
from typing import Optional
from time import perf_counter
from typing import Optional, Callable, TypeVar, Any

F = TypeVar("F", bound=Callable[..., Any])


def timed(
    _func: Optional[F] = None,
    *,
    message: Optional[str] = None,
    level: int = logging.INFO,
    logger: logging.Logger = logging.getLogger(),
) -> Callable[..., F]:
    """
    A decorator that logs the time taken by a function to execute.
    Can be used with or without arguments.

    Usage:
        @timed
        def func(...):
            ...

        @timed(message="Custom message", level=logging.DEBUG)
        def func(...):
            ...
    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                start = perf_counter()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    elapsed = perf_counter() - start
                    log_message = (
                        f"{func.__name__} took {elapsed:.6f} seconds to finish"
                    )
                    if message:
                        log_message = f"{message} - {log_message}"
                    logger.log(level, f"Timed: {log_message}")

            return async_wrapper  # type: ignore
        else:

            @wraps(func)
            def sync_wrapper(*args, **kwargs) -> Any:
                start = perf_counter()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    elapsed = perf_counter() - start
                    log_message = (
                        f"{func.__name__} took {elapsed:.6f} seconds to finish"
                    )
                    if message:
                        log_message = f"{message} - {log_message}"
                    logger.log(level, f"Timed: {log_message}")

            return sync_wrapper  # type: ignore

    if _func is None:
        # Decorator is called with arguments
        return decorator
    else:
        # Decorator is used without arguments
        return decorator(_func)
