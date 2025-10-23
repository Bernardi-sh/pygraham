"""
PyGraham - A high-performance functional programming library for Python
"""

from .maybe import Maybe
from .either import Either, Left, Right
from .compose import compose, pipe, curry
from .immutable import ImmutableList, ImmutableDict
from .lazy import lazy, LazySequence
from .pattern import match, case, _

__version__ = "0.1.0"

__all__ = [
    "Maybe",
    "Either",
    "Left",
    "Right",
    "compose",
    "pipe",
    "curry",
    "ImmutableList",
    "ImmutableDict",
    "lazy",
    "LazySequence",
    "match",
    "case",
    "_",
]
