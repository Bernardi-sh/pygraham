"""
Function composition utilities
"""

from typing import TypeVar, Callable, Any
from functools import reduce, wraps

T = TypeVar("T")


def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Compose functions from right to left.

    compose(f, g, h)(x) == f(g(h(x)))

    Example:
        >>> add_one = lambda x: x + 1
        >>> double = lambda x: x * 2
        >>> f = compose(double, add_one)
        >>> f(3)  # (3 + 1) * 2
        8
    """
    if not functions:
        return lambda x: x

    def _compose(f: Callable[[Any], Any], g: Callable[[Any], Any]) -> Callable[[Any], Any]:
        @wraps(f)
        def composed(x: Any) -> Any:
            return f(g(x))

        return composed

    return reduce(_compose, functions)


def pipe(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Compose functions from left to right.

    pipe(f, g, h)(x) == h(g(f(x)))

    Example:
        >>> add_one = lambda x: x + 1
        >>> double = lambda x: x * 2
        >>> f = pipe(add_one, double)
        >>> f(3)  # (3 + 1) * 2
        8
    """
    return compose(*reversed(functions))


def curry(fn: Callable[..., T]) -> Callable[..., Any]:
    """
    Transform a function that takes multiple arguments into a sequence
    of functions that each take a single argument.

    Example:
        >>> @curry
        ... def add(a, b, c):
        ...     return a + b + c
        >>> add(1)(2)(3)
        6
        >>> add(1, 2)(3)
        6
        >>> add(1)(2, 3)
        6
    """
    import inspect

    sig = inspect.signature(fn)
    num_params = len(sig.parameters)

    @wraps(fn)
    def curried(*args: Any, **kwargs: Any) -> Any:
        if len(args) + len(kwargs) >= num_params:
            return fn(*args, **kwargs)

        def partial(*more_args: Any, **more_kwargs: Any) -> Any:
            combined_args = args + more_args
            combined_kwargs = {**kwargs, **more_kwargs}
            return curried(*combined_args, **combined_kwargs)

        return partial

    return curried


def memoize(fn: Callable[..., T]) -> Callable[..., T]:
    """
    Memoize a function - cache results for given arguments.

    Example:
        >>> @memoize
        ... def fibonacci(n):
        ...     if n < 2:
        ...         return n
        ...     return fibonacci(n-1) + fibonacci(n-2)
    """
    cache: dict[tuple[Any, ...], T] = {}

    @wraps(fn)
    def memoized(*args: Any) -> T:
        if args in cache:
            return cache[args]
        result = fn(*args)
        cache[args] = result
        return result

    # Expose cache for inspection
    memoized.cache = cache  # type: ignore
    return memoized


def partial(fn: Callable[..., T], *fixed_args: Any, **fixed_kwargs: Any) -> Callable[..., T]:
    """
    Partial application of a function.

    Example:
        >>> def greet(greeting, name):
        ...     return f"{greeting}, {name}!"
        >>> hello = partial(greet, "Hello")
        >>> hello("World")
        'Hello, World!'
    """

    @wraps(fn)
    def partially_applied(*args: Any, **kwargs: Any) -> T:
        combined_args = fixed_args + args
        combined_kwargs = {**fixed_kwargs, **kwargs}
        return fn(*combined_args, **combined_kwargs)

    return partially_applied
