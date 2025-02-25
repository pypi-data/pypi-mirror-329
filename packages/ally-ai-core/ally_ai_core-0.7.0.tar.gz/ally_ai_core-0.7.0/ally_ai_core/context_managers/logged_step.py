from contextlib import contextmanager, asynccontextmanager
import logging
from typing import Optional, Generator, AsyncGenerator


@contextmanager
def logged_step(
    name: str, level: int = logging.INFO, raise_exception: bool = True
) -> Generator[None, None, None]:
    """
    Context manager to log the start and finish of a step, and handle exceptions.

    Args:
        name (str): Name of the step to log.
        level (int, optional): Logging level. Defaults to logging.INFO.
        raise_exception (bool, optional): Whether to re-raise exceptions after logging. Defaults to True.

    Yields:
        None
    """
    try:
        logging.log(level, f"Step({name}): Executing...")
        yield
        logging.log(level, f"Step({name}): Executed.")
    except Exception as ex:
        # Log the exception at ERROR level regardless of the specified level
        logging.error(f"Step({name}): Failed! Reason: {ex}")
        if raise_exception:
            raise


@asynccontextmanager
async def alogged_step(
    name: str, level: int = logging.INFO, raise_exception: bool = True
) -> AsyncGenerator[None, None]:
    """
    Asynchronous context manager to log the start and finish of a step, and handle exceptions.

    Args:
        name (str): Name of the step to log.
        level (int, optional): Logging level. Defaults to logging.INFO.
        raise_exception (bool, optional): Whether to re-raise exceptions after logging. Defaults to True.

    Yields:
        None
    """
    try:
        logging.log(level, f"Step({name}): Executing...")
        yield
        logging.log(level, f"Step({name}): Executed.")
    except Exception as ex:
        # Log the exception at ERROR level regardless of the specified level
        logging.error(f"Step({name}): Failed! Reason: {ex}")
        if raise_exception:
            raise
