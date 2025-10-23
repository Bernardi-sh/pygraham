"""
Fast operations using C++ extensions when available, fallback to Python
"""
from typing import TypeVar, Callable, List, Any

T = TypeVar('T')
U = TypeVar('U')

# Try to import C++ extensions
try:
    from . import _fast
    HAS_FAST = True
except ImportError:
    HAS_FAST = False


def fast_map(items: List[Any], func: Callable[[Any], Any]) -> List[Any]:
    """
    High-performance map operation.
    Uses C++ implementation when available.
    """
    if not HAS_FAST:
        return [func(item) for item in items]

    # Check if we can use optimized paths
    if items and isinstance(items[0], int):
        try:
            return _fast.fast_map_int(items, func)
        except Exception:
            pass
    elif items and isinstance(items[0], float):
        try:
            return _fast.fast_map_double(items, func)
        except Exception:
            pass

    # Fallback
    return [func(item) for item in items]


def fast_filter(items: List[Any], predicate: Callable[[Any], bool]) -> List[Any]:
    """
    High-performance filter operation.
    Uses C++ implementation when available.
    """
    if not HAS_FAST:
        return [item for item in items if predicate(item)]

    # Check if we can use optimized paths
    if items and isinstance(items[0], int):
        try:
            return _fast.fast_filter_int(items, predicate)
        except Exception:
            pass
    elif items and isinstance(items[0], float):
        try:
            return _fast.fast_filter_double(items, predicate)
        except Exception:
            pass

    # Fallback
    return [item for item in items if predicate(item)]


def fast_sum(items: List[Any]) -> Any:
    """
    High-performance sum operation.
    Uses C++ implementation when available.
    """
    if not HAS_FAST:
        return sum(items)

    if items and isinstance(items[0], int):
        try:
            return _fast.fast_sum_int(items)
        except Exception:
            pass
    elif items and isinstance(items[0], float):
        try:
            return _fast.fast_sum_double(items)
        except Exception:
            pass

    return sum(items)


class FastPipeline:
    """
    High-performance function pipeline.
    Uses C++ implementation when available for better performance.
    """

    def __init__(self):
        self.functions: List[Callable[[Any], Any]] = []
        if HAS_FAST:
            self._cpp_pipeline = _fast.FastPipeline()
        else:
            self._cpp_pipeline = None

    def add(self, func: Callable[[Any], Any]) -> 'FastPipeline':
        """Add a function to the pipeline."""
        self.functions.append(func)
        if self._cpp_pipeline:
            self._cpp_pipeline.add_function(func)
        return self

    def execute(self, input_value: Any) -> Any:
        """Execute the pipeline on an input value."""
        if self._cpp_pipeline:
            try:
                return self._cpp_pipeline.execute(input_value)
            except Exception:
                pass

        # Fallback to Python
        result = input_value
        for func in self.functions:
            result = func(result)
        return result

    def __call__(self, input_value: Any) -> Any:
        return self.execute(input_value)
