import warnings
from functools import wraps
from typing import Callable


def deprecated(reason: str, version: str) -> Callable[[Callable], Callable]:
    """
    Mark a function as deprecated.

    Parameters
    ----------
    reason : str
        The reason for deprecation.
    version : str
        The version in which the function was deprecated.
    """

    def decorator(f: Callable) -> Callable:

        @wraps(f)
        def new_func(*args, **kwargs):
            warnings.warn(
                f"{f.__name__} is deprecated since version {version}: {reason}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return f(*args, **kwargs)

        return new_func

    return decorator
