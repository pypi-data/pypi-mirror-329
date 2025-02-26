"""
Absfuyu: Core
-------------
Dummy functions when other libraries are unvailable

Version: 5.0.0
Date updated: 14/02/2025 (dd/mm/yyyy)
"""

# Module Package
# ---------------------------------------------------------------------------
__all__ = [
    "tqdm",
    "unidecode",
]


# Library
# ---------------------------------------------------------------------------
from importlib import import_module

# Wrapper
# ---------------------------------------------------------------------------
# tqdm wrapper
try:
    tqdm = import_module("tqdm").tqdm
except ModuleNotFoundError:

    def tqdm(iterable, *args, **kwargs):
        """
        Dummy tqdm function,
        install package ``tqdm`` to fully use this feature
        """
        return iterable


# unidecode wrapper
try:
    unidecode = import_module("unidecode").unidecode
except ModuleNotFoundError:

    def unidecode(*args, **kwargs):
        """
        Dummy unidecode function,
        install package ``unidecode`` to fully use this feature
        """
        return args[0]
