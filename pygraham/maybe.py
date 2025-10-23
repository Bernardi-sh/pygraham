"""
Maybe monad implementation for handling optional values elegantly
"""

from typing import TypeVar, Generic, Callable, Optional

T = TypeVar("T")
U = TypeVar("U")


class Maybe(Generic[T]):
    """
    Maybe monad for handling optional values without null checks.

    A Maybe[T] can be either Just(value) or Nothing, representing
    the presence or absence of a value.
    """

    def __init__(self, value: Optional[T] = None, is_nothing: bool = False):
        self._value = value
        self._is_nothing = is_nothing

    @staticmethod
    def of(value: Optional[T]) -> "Maybe[T]":
        """Create a Maybe from a value. None becomes Nothing."""
        if value is None:
            return Maybe.nothing()
        return Maybe(value, False)

    @staticmethod
    def just(value: T) -> "Maybe[T]":
        """Create a Just value (non-empty Maybe)."""
        return Maybe(value, False)

    @staticmethod
    def nothing() -> "Maybe[T]":
        """Create a Nothing value (empty Maybe)."""
        return Maybe(None, True)

    def is_nothing(self) -> bool:
        """Check if this is Nothing."""
        return self._is_nothing

    def is_just(self) -> bool:
        """Check if this is Just."""
        return not self._is_nothing

    def get(self) -> T:
        """
        Get the value or raise ValueError if Nothing.
        Use with caution - prefer get_or_else or map.
        """
        if self._is_nothing:
            raise ValueError("Cannot get value from Nothing")
        return self._value  # type: ignore

    def get_or_else(self, default: T) -> T:
        """Get the value or return default if Nothing."""
        if self._is_nothing:
            return default
        return self._value  # type: ignore

    def get_or_else_lazy(self, default_fn: Callable[[], T]) -> T:
        """Get the value or compute default if Nothing."""
        if self._is_nothing:
            return default_fn()
        return self._value  # type: ignore

    def map(self, fn: Callable[[T], U]) -> "Maybe[U]":
        """Apply function to value if Just, otherwise return Nothing."""
        if self._is_nothing:
            return Maybe.nothing()
        return Maybe.of(fn(self._value))  # type: ignore

    def flat_map(self, fn: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        """
        Apply function that returns Maybe to value if Just.
        Also known as bind or chain.
        """
        if self._is_nothing:
            return Maybe.nothing()
        return fn(self._value)  # type: ignore

    def filter(self, predicate: Callable[[T], bool]) -> "Maybe[T]":
        """Return this if Just and predicate is true, otherwise Nothing."""
        if self._is_nothing:
            return self
        if predicate(self._value):  # type: ignore
            return self
        return Maybe.nothing()

    def or_else(self, alternative: "Maybe[T]") -> "Maybe[T]":
        """Return this if Just, otherwise return alternative."""
        if self._is_nothing:
            return alternative
        return self

    def __repr__(self) -> str:
        if self._is_nothing:
            return "Nothing"
        return f"Just({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Maybe):
            return False
        if self._is_nothing and other._is_nothing:
            return True
        if self._is_nothing or other._is_nothing:
            return False
        return self._value == other._value

    def __bool__(self) -> bool:
        """Maybe is truthy if it's Just, falsy if Nothing."""
        return not self._is_nothing


# Convenience constructors
Just = Maybe.just
Nothing = Maybe.nothing
