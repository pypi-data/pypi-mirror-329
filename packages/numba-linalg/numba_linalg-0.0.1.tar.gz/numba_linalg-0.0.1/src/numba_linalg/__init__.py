"""Numba Linalg.

Linear algebra package using Numba and compatible with Numba
"""

__version__ = '0.0.1'

from importlib import import_module
from typing import TYPE_CHECKING
from sys import modules as _modules

from ._API import *
# ======================================================================
# Hinting types
if TYPE_CHECKING:
    from types import ModuleType

    # from . import subpackage
else:
    ModuleType = object
# ======================================================================
def __getattr__(name: str) -> ModuleType:
    if name in {'subpackage', }:
        module = import_module(f'.{name}', __package__)
        setattr(_modules[__package__], name, module)
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
