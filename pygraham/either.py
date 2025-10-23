"""
Either monad implementation for error handling without exceptions
"""
from typing import TypeVar, Generic, Callable, Union

L = TypeVar('L')
R = TypeVar('R')
U = TypeVar('U')


class Either(Generic[L, R]):
    """
    Either monad for error handling.

    An Either[L, R] can be either Left(error) or Right(value),
    representing failure or success respectively.
    """

    def __init__(self, value: Union[L, R], is_left: bool):
        self._value = value
        self._is_left = is_left

    @staticmethod
    def left(value: L) -> 'Either[L, R]':
        """Create a Left value (error case)."""
        return Either(value, True)

    @staticmethod
    def right(value: R) -> 'Either[L, R]':
        """Create a Right value (success case)."""
        return Either(value, False)

    def is_left(self) -> bool:
        """Check if this is Left (error)."""
        return self._is_left

    def is_right(self) -> bool:
        """Check if this is Right (success)."""
        return not self._is_left

    def get_left(self) -> L:
        """Get the left value or raise ValueError if Right."""
        if not self._is_left:
            raise ValueError("Cannot get left value from Right")
        return self._value  # type: ignore

    def get_right(self) -> R:
        """Get the right value or raise ValueError if Left."""
        if self._is_left:
            raise ValueError("Cannot get right value from Left")
        return self._value  # type: ignore

    def get_or_else(self, default: R) -> R:
        """Get the right value or return default if Left."""
        if self._is_left:
            return default
        return self._value  # type: ignore

    def map(self, fn: Callable[[R], U]) -> 'Either[L, U]':
        """Apply function to right value if Right, otherwise return Left."""
        if self._is_left:
            return Either.left(self._value)  # type: ignore
        return Either.right(fn(self._value))  # type: ignore

    def map_left(self, fn: Callable[[L], U]) -> 'Either[U, R]':
        """Apply function to left value if Left, otherwise return Right."""
        if self._is_left:
            return Either.left(fn(self._value))  # type: ignore
        return Either.right(self._value)  # type: ignore

    def flat_map(self, fn: Callable[[R], 'Either[L, U]']) -> 'Either[L, U]':
        """
        Apply function that returns Either to right value if Right.
        Also known as bind or chain.
        """
        if self._is_left:
            return Either.left(self._value)  # type: ignore
        return fn(self._value)  # type: ignore

    def fold(self, left_fn: Callable[[L], U], right_fn: Callable[[R], U]) -> U:
        """
        Apply left_fn if Left, right_fn if Right.
        Collapses the Either into a single value.
        """
        if self._is_left:
            return left_fn(self._value)  # type: ignore
        return right_fn(self._value)  # type: ignore

    def swap(self) -> 'Either[R, L]':
        """Swap Left and Right."""
        if self._is_left:
            return Either.right(self._value)  # type: ignore
        return Either.left(self._value)  # type: ignore

    def __repr__(self) -> str:
        if self._is_left:
            return f"Left({self._value!r})"
        return f"Right({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Either):
            return False
        if self._is_left != other._is_left:
            return False
        return self._value == other._value


# Convenience constructors
Left = Either.left
Right = Either.right
