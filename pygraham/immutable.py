"""
Immutable data structures with structural sharing
"""

from typing import TypeVar, Generic, Iterator, Optional, Callable, Any, Tuple, List as PyList
from collections.abc import Sequence, Mapping

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class ImmutableList(Generic[T], Sequence[T]):
    """
    Persistent immutable list with structural sharing.

    Operations return new lists while sharing most of the structure,
    making them efficient for functional programming.
    """

    def __init__(self, items: Optional[PyList[T]] = None):
        self._items: PyList[T] = list(items) if items is not None else []

    @staticmethod
    def of(*items: T) -> "ImmutableList[T]":
        """Create an ImmutableList from items."""
        return ImmutableList(list(items))

    def append(self, item: T) -> "ImmutableList[T]":
        """Return a new list with item appended."""
        new_items = self._items.copy()
        new_items.append(item)
        return ImmutableList(new_items)

    def prepend(self, item: T) -> "ImmutableList[T]":
        """Return a new list with item prepended."""
        new_items = [item] + self._items
        return ImmutableList(new_items)

    def concat(self, other: "ImmutableList[T]") -> "ImmutableList[T]":
        """Return a new list with other concatenated."""
        return ImmutableList(self._items + other._items)

    def map(self, fn: Callable[[T], Any]) -> "ImmutableList[Any]":
        """Apply function to each element."""
        return ImmutableList([fn(item) for item in self._items])

    def filter(self, predicate: Callable[[T], bool]) -> "ImmutableList[T]":
        """Return a new list with elements matching predicate."""
        return ImmutableList([item for item in self._items if predicate(item)])

    def reduce(self, fn: Callable[[Any, T], Any], initial: Any) -> Any:
        """Reduce list to a single value."""
        result = initial
        for item in self._items:
            result = fn(result, item)
        return result

    def take(self, n: int) -> "ImmutableList[T]":
        """Return a new list with first n elements."""
        return ImmutableList(self._items[:n])

    def drop(self, n: int) -> "ImmutableList[T]":
        """Return a new list without first n elements."""
        return ImmutableList(self._items[n:])

    def reverse(self) -> "ImmutableList[T]":
        """Return a new list with elements reversed."""
        return ImmutableList(list(reversed(self._items)))

    def sort(
        self, key: Optional[Callable[[T], Any]] = None, reverse: bool = False
    ) -> "ImmutableList[T]":
        """Return a new sorted list."""
        sorted_items = sorted(self._items, key=key, reverse=reverse)
        return ImmutableList(sorted_items)

    def head(self) -> Optional[T]:
        """Return first element or None if empty."""
        return self._items[0] if self._items else None

    def tail(self) -> "ImmutableList[T]":
        """Return list without first element."""
        return self.drop(1)

    def is_empty(self) -> bool:
        """Check if list is empty."""
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> T:  # type: ignore
        return self._items[index]

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __repr__(self) -> str:
        return f"ImmutableList({self._items!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ImmutableList):
            return False
        return self._items == other._items

    def __add__(self, other: "ImmutableList[T]") -> "ImmutableList[T]":
        """Allow using + operator for concatenation."""
        return self.concat(other)


class ImmutableDict(Generic[K, V], Mapping[K, V]):
    """
    Persistent immutable dictionary with structural sharing.

    Operations return new dictionaries while sharing most of the structure.
    """

    def __init__(self, items: Optional[dict[K, V]] = None):
        self._items: dict[K, V] = dict(items) if items is not None else {}

    @staticmethod
    def of(**kwargs: V) -> "ImmutableDict[str, V]":
        """Create an ImmutableDict from keyword arguments."""
        return ImmutableDict(kwargs)

    def set(self, key: K, value: V) -> "ImmutableDict[K, V]":
        """Return a new dict with key set to value."""
        new_items = self._items.copy()
        new_items[key] = value
        return ImmutableDict(new_items)

    def delete(self, key: K) -> "ImmutableDict[K, V]":
        """Return a new dict without key."""
        new_items = self._items.copy()
        if key in new_items:
            del new_items[key]
        return ImmutableDict(new_items)

    def update(self, other: "ImmutableDict[K, V]") -> "ImmutableDict[K, V]":
        """Return a new dict with other's items merged."""
        new_items = self._items.copy()
        new_items.update(other._items)
        return ImmutableDict(new_items)

    def map_values(self, fn: Callable[[V], Any]) -> "ImmutableDict[K, Any]":
        """Apply function to each value."""
        return ImmutableDict({k: fn(v) for k, v in self._items.items()})

    def filter(self, predicate: Callable[[Tuple[K, V]], bool]) -> "ImmutableDict[K, V]":
        """Return a new dict with items matching predicate."""
        return ImmutableDict({k: v for k, v in self._items.items() if predicate((k, v))})

    def get_or_else(self, key: K, default: V) -> V:
        """Get value for key or return default."""
        return self._items.get(key, default)

    def has_key(self, key: K) -> bool:
        """Check if key exists."""
        return key in self._items

    def keys_list(self) -> ImmutableList[K]:
        """Return keys as ImmutableList."""
        return ImmutableList(list(self._items.keys()))

    def values_list(self) -> ImmutableList[V]:
        """Return values as ImmutableList."""
        return ImmutableList(list(self._items.values()))

    def items_list(self) -> ImmutableList[Tuple[K, V]]:
        """Return items as ImmutableList."""
        return ImmutableList(list(self._items.items()))

    def is_empty(self) -> bool:
        """Check if dict is empty."""
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, key: K) -> V:
        return self._items[key]

    def __iter__(self) -> Iterator[K]:
        return iter(self._items)

    def __repr__(self) -> str:
        return f"ImmutableDict({self._items!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ImmutableDict):
            return False
        return self._items == other._items
