"""
Lazy evaluation utilities for efficient computation
"""
from typing import TypeVar, Callable, Iterator, Optional, Any
from itertools import islice

T = TypeVar('T')
U = TypeVar('U')


class LazySequence:
    """
    Lazy sequence that computes values on demand.

    Operations are not executed until values are needed,
    enabling efficient processing of large or infinite sequences.
    """

    def __init__(self, iterable: Iterator[Any]):
        self._iterator = iterable

    @staticmethod
    def from_iterable(iterable: Any) -> 'LazySequence':
        """Create a lazy sequence from any iterable."""
        return LazySequence(iter(iterable))

    @staticmethod
    def range(start: int, end: Optional[int] = None, step: int = 1) -> 'LazySequence':
        """Create a lazy range."""
        if end is None:
            end = start
            start = 0
        return LazySequence(iter(range(start, end, step)))

    @staticmethod
    def infinite(start: int = 0, step: int = 1) -> 'LazySequence':
        """Create an infinite lazy sequence."""
        def generator():
            current = start
            while True:
                yield current
                current += step
        return LazySequence(generator())

    @staticmethod
    def repeat(value: T, times: Optional[int] = None) -> 'LazySequence':
        """Repeat a value lazily."""
        if times is None:
            def generator():
                while True:
                    yield value
            return LazySequence(generator())
        else:
            return LazySequence(iter([value] * times))

    def map(self, fn: Callable[[Any], Any]) -> 'LazySequence':
        """Apply function to each element lazily."""
        return LazySequence(fn(x) for x in self._iterator)

    def filter(self, predicate: Callable[[Any], bool]) -> 'LazySequence':
        """Filter elements lazily."""
        return LazySequence(x for x in self._iterator if predicate(x))

    def take(self, n: int) -> 'LazySequence':
        """Take first n elements."""
        return LazySequence(islice(self._iterator, n))

    def drop(self, n: int) -> 'LazySequence':
        """Drop first n elements."""
        # Consume n elements
        for _ in range(n):
            try:
                next(self._iterator)
            except StopIteration:
                break
        return LazySequence(self._iterator)

    def take_while(self, predicate: Callable[[Any], bool]) -> 'LazySequence':
        """Take elements while predicate is true."""
        def generator():
            for item in self._iterator:
                if not predicate(item):
                    break
                yield item
        return LazySequence(generator())

    def drop_while(self, predicate: Callable[[Any], bool]) -> 'LazySequence':
        """Drop elements while predicate is true."""
        def generator():
            dropping = True
            for item in self._iterator:
                if dropping and predicate(item):
                    continue
                dropping = False
                yield item
        return LazySequence(generator())

    def flat_map(self, fn: Callable[[Any], Any]) -> 'LazySequence':
        """Map and flatten the results."""
        def generator():
            for item in self._iterator:
                result = fn(item)
                if hasattr(result, '__iter__') and not isinstance(result, str):
                    yield from result
                else:
                    yield result
        return LazySequence(generator())

    def zip_with(self, other: 'LazySequence', fn: Callable[[Any, Any], Any]) -> 'LazySequence':
        """Zip two sequences with a combining function."""
        return LazySequence(fn(x, y) for x, y in zip(self._iterator, other._iterator))

    def scan(self, fn: Callable[[Any, Any], Any], initial: Any) -> 'LazySequence':
        """
        Lazy accumulation (like reduce but returns all intermediate values).
        """
        def generator():
            acc = initial
            yield acc
            for item in self._iterator:
                acc = fn(acc, item)
                yield acc
        return LazySequence(generator())

    def chunk(self, size: int) -> 'LazySequence':
        """Split sequence into chunks of given size."""
        def generator():
            while True:
                chunk = list(islice(self._iterator, size))
                if not chunk:
                    break
                yield chunk
        return LazySequence(generator())

    def to_list(self) -> list[Any]:
        """Force evaluation and convert to list."""
        return list(self._iterator)

    def force(self) -> list[Any]:
        """Alias for to_list."""
        return self.to_list()

    def head(self) -> Optional[Any]:
        """Get first element or None."""
        try:
            return next(self._iterator)
        except StopIteration:
            return None

    def reduce(self, fn: Callable[[Any, Any], Any], initial: Any) -> Any:
        """Reduce sequence to a single value."""
        result = initial
        for item in self._iterator:
            result = fn(result, item)
        return result

    def __iter__(self) -> Iterator[Any]:
        return self._iterator


def lazy(fn: Callable[[], T]) -> Callable[[], T]:
    """
    Decorator to make a function lazy - result is computed once on first call
    and cached.

    Example:
        >>> @lazy
        ... def expensive_computation():
        ...     print("Computing...")
        ...     return sum(range(1000000))
        >>> result = expensive_computation  # Not computed yet
        >>> result()  # Computed now and cached
        Computing...
        499999500000
        >>> result()  # Uses cached value
        499999500000
    """
    cache: dict[str, T] = {}

    def wrapper() -> T:
        if 'value' not in cache:
            cache['value'] = fn()
        return cache['value']

    return wrapper
