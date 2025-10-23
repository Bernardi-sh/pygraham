# PyGraham 🚀

A high-performance functional programming library for Python that brings true functional programming capabilities with significant performance optimizations.

## Installation

```bash
pip install pygraham
```

## Why PyGraham?

PyGraham extends Python with truly functional programming capabilities while providing **significant performance improvements** over vanilla Python and other functional libraries.

### Key Features

- **Immutable Data Structures**: Persistent vectors, maps, and sets with structural sharing
- **Monads**: Maybe, Either, IO, and more for elegant error handling
- **Function Composition**: Compose, pipe, and curry functions with ease
- **Lazy Evaluation**: Efficient lazy sequences and streams
- **Pattern Matching**: Powerful pattern matching for complex data structures
- **Performance**: C++/Rust optimizations for critical operations

## Quick Examples

### Before (Vanilla Python)
```python
# Nested error handling
def process_data(data):
    if data is None:
        return None
    result = transform(data)
    if result is None:
        return None
    validated = validate(result)
    if validated is None:
        return None
    return save(validated)
```

### After (PyGraham)
```python
from pygraham import Maybe, pipe

process_data = pipe(
    transform,
    validate,
    save
)

result = Maybe.of(data).flat_map(process_data)
```

## Performance Benchmarks

See [examples/benchmarks](examples/benchmarks) for detailed performance comparisons.

## Documentation

Full documentation available at [https://github.com/Bernardi-sh/pygraham](https://github.com/Bernardi-sh/pygraham)

## License

MIT License - see LICENSE file for details
