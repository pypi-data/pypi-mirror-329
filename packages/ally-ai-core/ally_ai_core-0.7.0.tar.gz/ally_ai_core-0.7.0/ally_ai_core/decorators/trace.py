import logging
import inspect
from functools import wraps
from typing import Callable, Optional, TypeVar, Any, cast
from random import randrange
from dataclasses import dataclass

default_logger = logging.getLogger()
default_logger.setLevel(logging.INFO)

F = TypeVar("F", bound=Callable[..., Any])


@dataclass(frozen=True)
class Tracer:
    """
    Args:
            message (str): Custom message to include in logs.
            show_in (bool): Whether to log the start of the function.
            show_out (bool): Whether to log the finish of the function.
            show_data (bool): Whether to log the args and kwargs of the function.
    """

    show_in: bool = (True,)
    show_out: bool = (True,)
    show_data: bool = (True,)
    logger: logging.Logger = (default_logger,)

    def trace(
        self,
        message: str,
        show_in: Optional[bool] = None,
        show_out: Optional[bool] = None,
        show_data: Optional[bool] = None,
        logger: Optional[logging.Logger] = None,
    ) -> Callable[[F], F]:
        """
        Decorator to log the start and finish of a function execution.

        Args:
            message (str): Custom message to include in logs.
            show_in (bool): Overrides whether to log the start of the function.
            show_out (bool): Overrides whether to log the finish of the function.
            show_data (bool): Overrides whether to log the args and kwargs of the function.
            logger: (Logger):
        Returns:
            Callable: The decorated function with logging.
        """

        show_in = show_in if show_in else self.show_in
        show_out = show_out if show_out else self.show_out
        show_data = show_data if show_data else self.show_data
        logger = logger if logger else self.logger

        def decorator(func: F) -> F:
            if inspect.iscoroutinefunction(func):

                @wraps(func)
                async def awrapper(*args, **kwargs) -> Any:
                    id = randrange(1, 100_000_000_000)
                    try:
                        if show_in:
                            logger.log(
                                level=logger.level,
                                msg=f"{message} - IN({id}) *{func.__name__}* with args: {args if show_data else ''} , kwargs: {kwargs if show_data else ''}",
                            )

                        result = await func(*args, **kwargs)

                        if show_out:
                            logger.log(
                                level=logger.level,
                                msg=f"{message} - OUT({id}) *{func.__name__}* with result: {result if show_data else ''}",
                            )
                        return result
                    except Exception as e:
                        logger.exception(
                            f"{message} - Exception({id}) *{func.__name__}* raised an exception: {e}"
                        )
                        raise  # Re-raise the exception after logger

                return cast(F, awrapper)
            else:

                @wraps(func)
                def wrapper(*args, **kwargs) -> Any:
                    id = randrange(1, 100_000_000_000)
                    try:
                        if show_in:
                            logger.log(
                                level=logger.level,
                                msg=f"{message} - IN({id}) *{func.__name__}* with args: {args if show_data else ''} , kwargs: {kwargs if show_data else ''}",
                            )

                        result = func(*args, **kwargs)

                        if show_out:
                            logger.log(
                                level=logger.level,
                                msg=f"{message} - OUT({id}) *{func.__name__}* with result: {result if show_data else ''}",
                            )
                        return result
                    except Exception as e:
                        logger.exception(
                            f"{message} - Exception({id}) *{func.__name__}* raised an exception: {e}"
                        )
                        raise

                return cast(F, wrapper)

        return decorator


default_tracer = Tracer(
    show_in=True, show_out=True, show_data=True, logger=default_logger
)


def trace(
    message: str,
    show_in: Optional[bool] = None,
    show_out: Optional[bool] = None,
    show_data: Optional[bool] = None,
    logger: Optional[bool] = None,
) -> Callable[[F], F]:
    return default_tracer.trace(message, show_in, show_out, show_data, logger)
