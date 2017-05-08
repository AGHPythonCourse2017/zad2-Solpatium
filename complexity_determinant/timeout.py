"""Decorator for setting a time constraint on a function"""
from functools import wraps
import signal


class TimeoutExceeded(Exception):
    """Exception thrown when the execution exceeds timeout"""
    pass


# Thanks to David Narayan
# http://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish
def timeout(seconds):
    """Decorator used for adding time constraints"""
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutExceeded()

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
