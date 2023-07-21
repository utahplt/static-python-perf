from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
    pass

def timeout(seconds=5):
    """
    Decorator which waits for a function to execute and
    calls time_out_handler if the function does not
    return a value in time
    """
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError()

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
                return result

            finally:
                signal.alarm(0)

        return wraps(func)(wrapper)

    return decorator


