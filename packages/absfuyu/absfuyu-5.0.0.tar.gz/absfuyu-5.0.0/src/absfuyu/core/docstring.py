"""
Absfuyu: Core
-------------
Sphinx docstring decorator

Version: 5.0.0
Date updated: 13/02/2025 (dd/mm/yyyy)
"""

# Module Package
# ---------------------------------------------------------------------------
__all__ = [
    "SphinxDocstring",
    "SphinxDocstringMode",
    "versionadded",
    "versionchanged",
    "deprecated",
]


# Library
# ---------------------------------------------------------------------------
from collections.abc import Callable
from enum import Enum
from functools import partial, wraps
from string import Template
from typing import ClassVar, ParamSpec, TypeVar, overload

# Type
# ---------------------------------------------------------------------------
P = ParamSpec("P")  # Parameter type
R = TypeVar("R")  # Return type - Can be anything
T = TypeVar("T", bound=type)  # Type type - Can be any subtype of `type`

_SPHINX_DOCS_TEMPLATE = Template("$line_break*$mode in version $version$reason*")


# Class
# ---------------------------------------------------------------------------
class SphinxDocstringMode(Enum):
    """
    Enum representing the mode of the version change
    (added, changed, or deprecated)
    """

    ADDED = "Added"
    CHANGED = "Changed"
    DEPRECATED = "Deprecated"


class SphinxDocstring:
    """
    A class-based decorator to add a 'Version added',
    'Version changed', or 'Deprecated' note to a function's docstring,
    formatted for Sphinx documentation.
    """

    _LINEBREAK: ClassVar[str] = "\n\n"  # Use ClassVar for constant

    def __init__(
        self,
        version: str,
        reason: str | None = None,
        mode: SphinxDocstringMode = SphinxDocstringMode.ADDED,
    ) -> None:
        """
        Initializes the SphinxDocstring decorator.

        Parameters
        ----------
        version : str
            The version in which the function was added, changed, or deprecated.

        reason : str | None, optional
            An optional reason or description for the change
            or deprecation, by default ``None``

        mode : SphinxDocstringMode | int, optional
            Specifies whether the function was 'added', 'changed', or 'deprecated',
            by default SphinxDocstringMode.ADDED

        Usage
        -----
        Use this as a decorator (``@SphinxDocstring(<parameters>)``)
        """
        self.version = version
        self.reason = reason
        self.mode = mode

    @overload
    def __call__(self, obj: T) -> T: ...  # Class overload
    @overload
    def __call__(self, obj: Callable[P, R]) -> Callable[P, R]: ...  # Function overload
    def __call__(self, obj: T | Callable[P, R]) -> T | Callable[P, R]:
        # Class wrapper
        if isinstance(obj, type):  # if inspect.isclass(obj):
            obj.__doc__ = (obj.__doc__ or "") + self._generate_version_note(
                num_of_white_spaces=self._calculate_white_space(obj.__doc__)
            )
            return obj

        # Function wrapper
        @wraps(obj)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return obj(*args, **kwargs)

        # Add docstring
        # version_note = self._generate_version_note()
        # if wrapper.__doc__ is None:
        #     wrapper.__doc__ = version_note
        # else:
        #     wrapper.__doc__ += version_note

        wrapper.__doc__ = (wrapper.__doc__ or "") + self._generate_version_note(
            num_of_white_spaces=self._calculate_white_space(wrapper.__doc__)
        )

        return wrapper

    def _calculate_white_space(self, docs: str | None) -> int:
        """
        Calculates the number of leading white spaces
        in __doc__ of original function
        """

        res = 0
        if docs is None:
            return res

        # # Index of the last whitespaces
        # # https://stackoverflow.com/a/13649118
        # res = next((i for i, c in enumerate(docs) if not c.isspace()), 0)
        # return res if res % 2 == 0 else res - 1

        # Alternative solution
        for char in docs:
            if char == " ":
                res += 1
            if char == "\t":
                res += 4
            if not char.isspace():
                break
        return res

    def _generate_version_note(self, num_of_white_spaces: int) -> str:
        """
        Generates the version note string based on the mode
        """
        reason_str = f": {self.reason}" if self.reason else ""
        # return f"{self._LINEBREAK}*{self.mode.value} in version {self.version}{reason_str}*"
        return _SPHINX_DOCS_TEMPLATE.substitute(
            line_break=self._LINEBREAK + " " * num_of_white_spaces,
            mode=self.mode.value,
            version=self.version,
            reason=reason_str,
        )


# Partial
# ---------------------------------------------------------------------------
versionadded = partial(SphinxDocstring, mode=SphinxDocstringMode.ADDED)
versionchanged = partial(SphinxDocstring, mode=SphinxDocstringMode.CHANGED)
deprecated = partial(SphinxDocstring, mode=SphinxDocstringMode.DEPRECATED)
