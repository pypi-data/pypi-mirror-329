import logging
from functools import wraps


def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        # pylint: disable=broad-except
        except Exception as e:
            logging.error("Error in %s: %s", func.__name__, str(e))
        return None  # Add this line to ensure consistent return

    return wrapper
