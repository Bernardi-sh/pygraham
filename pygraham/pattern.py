"""
Pattern matching utilities
"""

from typing import Any, Callable, TypeVar, Optional

T = TypeVar("T")


class _WildCard:
    """Wildcard pattern that matches anything."""

    def __repr__(self) -> str:
        return "_"


# Singleton wildcard
_ = _WildCard()


class Case:
    """Represents a pattern matching case."""

    def __init__(self, pattern: Any, handler: Callable[[Any], Any]):
        self.pattern = pattern
        self.handler = handler

    def matches(self, value: Any) -> bool:
        """Check if value matches this case's pattern."""
        if isinstance(self.pattern, _WildCard):
            return True
        if isinstance(self.pattern, type):
            return isinstance(value, self.pattern)
        if callable(self.pattern):
            try:
                return bool(self.pattern(value))
            except Exception:
                return False
        return self.pattern == value

    def execute(self, value: Any) -> Any:
        """Execute the handler for this case."""
        if callable(self.handler):
            return self.handler(value)
        return self.handler


def case(pattern: Any, handler: Callable[[Any], Any]) -> Case:
    """
    Create a pattern matching case.

    Args:
        pattern: Can be:
            - A value to match exactly
            - A type to check isinstance
            - A callable predicate
            - _ (wildcard) to match anything
        handler: Function to execute if pattern matches

    Example:
        >>> case(1, lambda x: "one")
        >>> case(str, lambda x: f"string: {x}")
        >>> case(lambda x: x > 10, lambda x: "big number")
        >>> case(_, lambda x: "default")
    """
    return Case(pattern, handler)


def match(value: Any, *cases: Case) -> Any:
    """
    Pattern match a value against cases.

    Returns the result of the first matching case's handler.
    Raises ValueError if no case matches.

    Example:
        >>> def classify_number(n):
        ...     return match(n,
        ...         case(0, lambda x: "zero"),
        ...         case(lambda x: x < 0, lambda x: "negative"),
        ...         case(lambda x: x > 0, lambda x: "positive")
        ...     )
        >>> classify_number(5)
        'positive'
    """
    for c in cases:
        if c.matches(value):
            return c.execute(value)
    raise ValueError(f"No matching case for value: {value}")


def match_with_default(value: Any, default: Any, *cases: Case) -> Any:
    """
    Pattern match with a default value if no case matches.

    Example:
        >>> match_with_default(100, "unknown",
        ...     case(1, lambda x: "one"),
        ...     case(2, lambda x: "two")
        ... )
        'unknown'
    """
    for c in cases:
        if c.matches(value):
            return c.execute(value)
    return default


class Match:
    """
    Fluent interface for pattern matching.

    Example:
        >>> result = (Match(5)
        ...     .case(0, lambda x: "zero")
        ...     .case(lambda x: x < 0, lambda x: "negative")
        ...     .case(lambda x: x > 0, lambda x: "positive")
        ...     .execute())
        >>> result
        'positive'
    """

    def __init__(self, value: Any):
        self.value = value
        self.cases: list[Case] = []
        self.default_handler: Optional[Callable[[Any], Any]] = None

    def case(self, pattern: Any, handler: Callable[[Any], Any]) -> "Match":
        """Add a case to the match."""
        self.cases.append(Case(pattern, handler))
        return self

    def default(self, handler: Callable[[Any], Any]) -> "Match":
        """Set default handler if no case matches."""
        self.default_handler = handler
        return self

    def execute(self) -> Any:
        """Execute the pattern match."""
        for c in self.cases:
            if c.matches(self.value):
                return c.execute(self.value)
        if self.default_handler:
            return self.default_handler(self.value)
        raise ValueError(f"No matching case for value: {self.value}")


# Type-based pattern matching helpers
def instance_of(*types: type) -> Callable[[Any], bool]:
    """Create a predicate that checks if value is instance of any given types."""

    def predicate(value: Any) -> bool:
        return isinstance(value, types)

    return predicate


def has_attr(attr: str) -> Callable[[Any], bool]:
    """Create a predicate that checks if value has given attribute."""

    def predicate(value: Any) -> bool:
        return hasattr(value, attr)

    return predicate


def in_range(min_val: Any, max_val: Any) -> Callable[[Any], bool]:
    """Create a predicate that checks if value is in range."""

    def predicate(value: Any) -> bool:
        return min_val <= value <= max_val

    return predicate
