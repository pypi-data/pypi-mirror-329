import warnings
from functools import wraps
from typing import Callable


def experimental(f: Callable) -> Callable:
    """Mark a function as experimental."""

    @wraps(f)
    def new_func(*args, **kwargs):
        warnings.warn(
            f"{f.__name__} is an experimental feature and may change or be removed without notice.",
            category=FutureWarning,
            stacklevel=2,
        )
        return f(*args, **kwargs)

    return new_func
