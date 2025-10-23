"""
PyGraham - A high-performance functional programming library for Python
"""

from .maybe import Maybe, Just, Nothing
from .either import Either, Left, Right
from .compose import compose, pipe, curry
from .immutable import ImmutableList, ImmutableDict
from .lazy import lazy, LazySequence
from .pattern import match, case, _, Match, instance_of, has_attr, in_range

__version__ = "0.1.0"

__all__ = [
    "Maybe",
    "Just",
    "Nothing",
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
    "Match",
    "instance_of",
    "has_attr",
    "in_range",
]
