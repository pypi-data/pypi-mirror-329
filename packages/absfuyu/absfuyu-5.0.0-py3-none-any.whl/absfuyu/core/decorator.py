"""
Absfuyu: Core
-------------
Decorator

Version: 5.0.0
Date updated: 22/02/2025 (dd/mm/yyyy)
"""

# Module Package
# ---------------------------------------------------------------------------
__all__ = ["dummy_decorator", "dummy_decorator_with_args"]


# Library
# ---------------------------------------------------------------------------
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar, overload

# Type
# ---------------------------------------------------------------------------
P = ParamSpec("P")  # Parameter type
R = TypeVar("R")  # Return type - Can be anything
T = TypeVar("T", bound=type)  # Type type - Can be any subtype of `type`


# Decorator
# ---------------------------------------------------------------------------
@overload
def dummy_decorator(obj: T) -> T: ...
@overload
def dummy_decorator(obj: Callable[P, R]) -> Callable[P, R]: ...
def dummy_decorator(obj: Callable[P, R] | T) -> Callable[P, R] | T:
    """
    This is a decorator that does nothing. Normally used as a placeholder
    """
    if isinstance(obj, type):
        return obj

    @wraps(obj)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return obj(*args, **kwargs)

    return wrapper


def dummy_decorator_with_args(*args, **kwargs):
    """
    This is a decorator with args and kwargs that does nothing. Normally used as a placeholder
    """

    @overload
    def decorator(obj: T) -> T: ...
    @overload
    def decorator(obj: Callable[P, R]) -> Callable[P, R]: ...
    def decorator(obj: Callable[P, R] | T) -> Callable[P, R] | T:
        if isinstance(obj, type):
            return obj

        @wraps(obj)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return obj(*args, **kwargs)

        return wrapper

    return decorator
