from .__init__ import *

__all__ = ["debug"]


def debug(logFn: Callable = logger.debug) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logFn(f"{func.__name__}#before: {globals(), locals()}")
            r = func(*args, **kwargs)
            logFn(f"{func.__name__}#after: {globals(), locals()}, result: {r}")
            return r

        return wrapper

    return decorator
