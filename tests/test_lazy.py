"""
Tests for lazy evaluation
"""
import pytest
from pygraham import lazy, LazySequence


class TestLazySequence:
    def test_from_iterable(self):
        seq = LazySequence.from_iterable([1, 2, 3, 4])
        result = seq.to_list()
        assert result == [1, 2, 3, 4]

    def test_range(self):
        seq = LazySequence.range(5)
        result = seq.to_list()
        assert result == [0, 1, 2, 3, 4]

    def test_range_with_start(self):
        seq = LazySequence.range(2, 5)
        result = seq.to_list()
        assert result == [2, 3, 4]

    def test_infinite_with_take(self):
        seq = LazySequence.infinite(1).take(5)
        result = seq.to_list()
        assert result == [1, 2, 3, 4, 5]

    def test_repeat(self):
        seq = LazySequence.repeat(42, 3)
        result = seq.to_list()
        assert result == [42, 42, 42]

    def test_map(self):
        seq = LazySequence.from_iterable([1, 2, 3])
        result = seq.map(lambda x: x * 2).to_list()
        assert result == [2, 4, 6]

    def test_filter(self):
        seq = LazySequence.from_iterable([1, 2, 3, 4, 5])
        result = seq.filter(lambda x: x % 2 == 0).to_list()
        assert result == [2, 4]

    def test_take(self):
        seq = LazySequence.from_iterable([1, 2, 3, 4, 5])
        result = seq.take(3).to_list()
        assert result == [1, 2, 3]

    def test_drop(self):
        seq = LazySequence.from_iterable([1, 2, 3, 4, 5])
        result = seq.drop(2).to_list()
        assert result == [3, 4, 5]

    def test_take_while(self):
        seq = LazySequence.from_iterable([1, 2, 3, 4, 5])
        result = seq.take_while(lambda x: x < 4).to_list()
        assert result == [1, 2, 3]

    def test_drop_while(self):
        seq = LazySequence.from_iterable([1, 2, 3, 4, 5])
        result = seq.drop_while(lambda x: x < 3).to_list()
        assert result == [3, 4, 5]

    def test_flat_map(self):
        seq = LazySequence.from_iterable([1, 2, 3])
        result = seq.flat_map(lambda x: [x, x * 10]).to_list()
        assert result == [1, 10, 2, 20, 3, 30]

    def test_scan(self):
        seq = LazySequence.from_iterable([1, 2, 3, 4])
        result = seq.scan(lambda acc, x: acc + x, 0).to_list()
        assert result == [0, 1, 3, 6, 10]

    def test_chunk(self):
        seq = LazySequence.from_iterable([1, 2, 3, 4, 5, 6, 7])
        result = seq.chunk(3).to_list()
        assert result == [[1, 2, 3], [4, 5, 6], [7]]

    def test_head(self):
        seq = LazySequence.from_iterable([1, 2, 3])
        assert seq.head() == 1

    def test_head_empty(self):
        seq = LazySequence.from_iterable([])
        assert seq.head() is None

    def test_reduce(self):
        seq = LazySequence.from_iterable([1, 2, 3, 4])
        result = seq.reduce(lambda acc, x: acc + x, 0)
        assert result == 10

    def test_chaining(self):
        result = (LazySequence.range(1, 11)
                  .filter(lambda x: x % 2 == 0)
                  .map(lambda x: x * 2)
                  .take(3)
                  .to_list())
        assert result == [4, 8, 12]

    def test_lazy_evaluation(self):
        """Test that operations are truly lazy"""
        counter = {"count": 0}

        def increment(x):
            counter["count"] += 1
            return x * 2

        # Create a lazy sequence
        seq = LazySequence.range(1000).map(increment)

        # Counter should still be 0 - nothing evaluated yet
        assert counter["count"] == 0

        # Take only 5 elements
        result = seq.take(5).to_list()

        # Counter should be 5, not 1000
        assert counter["count"] == 5
        assert result == [0, 2, 4, 6, 8]


class TestLazyDecorator:
    def test_lazy_decorator(self):
        counter = {"count": 0}

        @lazy
        def expensive_computation():
            counter["count"] += 1
            return 42

        # Not computed yet
        assert counter["count"] == 0

        # Compute on first call
        result1 = expensive_computation()
        assert result1 == 42
        assert counter["count"] == 1

        # Use cached value on second call
        result2 = expensive_computation()
        assert result2 == 42
        assert counter["count"] == 1  # Still 1, not 2

    def test_lazy_with_complex_computation(self):
        @lazy
        def fibonacci_sum():
            fib = [1, 1]
            for _ in range(98):
                fib.append(fib[-1] + fib[-2])
            return sum(fib)

        result = fibonacci_sum()
        assert result > 0
        # Result is cached, so second call should be instant
        result2 = fibonacci_sum()
        assert result == result2
