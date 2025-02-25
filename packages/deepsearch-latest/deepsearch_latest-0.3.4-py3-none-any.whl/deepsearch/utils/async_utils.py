import asyncio
import logging
import functools

logger = logging.getLogger("deepsearch-mcp")


def log_cancellation(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except asyncio.CancelledError:
            logger.info(f"Function {func.__name__} was cancelled")
            raise
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper
