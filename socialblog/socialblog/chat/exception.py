from functools import wraps
from inspect import iscoroutinefunction
from logging import getLogger

from channels.exceptions import AcceptConnection, DenyConnection, StopConsumer

logger = getLogger()

def apply_wrappers(consumer_class):
    for method_name, method in list(consumer_class.__dict__.items()):
        if iscoroutinefunction(method):
            setattr(consumer_class, method_name, propagate_exceptions(method))


def propagate_exceptions(func):
    async def wrapper(*args, **kwargs):  # we're wrapping an async function
        try:
            return await func(*args, **kwargs)
        except (AcceptConnection, DenyConnection, StopConsumer):  # these are handled by channels
            raise
        except Exception as exception:  # any other exception
            # avoid logging the same exception multiple times
            if not getattr(exception, "caught", False):
                setattr(exception, "caught", True)
                logger.error(
                    """Exception occurred in %s :""" % func.__qualname,
                    exc_info=exception,
                )
            raise  # propagate the exception
    return wraps(func)(wrapper)
