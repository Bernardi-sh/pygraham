"""
Tests for Either monad
"""
import pytest
from pygraham import Either, Left, Right


class TestEither:
    def test_right_creation(self):
        e = Right(5)
        assert e.is_right()
        assert not e.is_left()
        assert e.get_right() == 5

    def test_left_creation(self):
        e = Left("error")
        assert e.is_left()
        assert not e.is_right()
        assert e.get_left() == "error"

    def test_get_or_else_right(self):
        e = Right(5)
        assert e.get_or_else(10) == 5

    def test_get_or_else_left(self):
        e = Left("error")
        assert e.get_or_else(10) == 10

    def test_map_right(self):
        e = Right(5)
        result = e.map(lambda x: x * 2)
        assert result.get_right() == 10

    def test_map_left(self):
        e = Left("error")
        result = e.map(lambda x: x * 2)
        assert result.is_left()
        assert result.get_left() == "error"

    def test_map_left_method(self):
        e = Left("error")
        result = e.map_left(lambda x: x.upper())
        assert result.get_left() == "ERROR"

    def test_flat_map_right(self):
        e = Right(5)
        result = e.flat_map(lambda x: Right(x * 2))
        assert result.get_right() == 10

    def test_flat_map_to_left(self):
        e = Right(5)
        result = e.flat_map(lambda x: Left("error"))
        assert result.is_left()

    def test_flat_map_left(self):
        e = Left("error")
        result = e.flat_map(lambda x: Right(x * 2))
        assert result.is_left()
        assert result.get_left() == "error"

    def test_fold_right(self):
        e = Right(5)
        result = e.fold(
            lambda l: f"Error: {l}",
            lambda r: f"Success: {r}"
        )
        assert result == "Success: 5"

    def test_fold_left(self):
        e = Left("error")
        result = e.fold(
            lambda l: f"Error: {l}",
            lambda r: f"Success: {r}"
        )
        assert result == "Error: error"

    def test_swap_right(self):
        e = Right(5)
        swapped = e.swap()
        assert swapped.is_left()
        assert swapped.get_left() == 5

    def test_swap_left(self):
        e = Left("error")
        swapped = e.swap()
        assert swapped.is_right()
        assert swapped.get_right() == "error"

    def test_chaining(self):
        result = (Right(5)
                  .map(lambda x: x * 2)
                  .map(lambda x: x + 1)
                  .get_or_else(0))
        assert result == 11

    def test_error_handling_chain(self):
        def divide(x, y):
            if y == 0:
                return Left("Division by zero")
            return Right(x / y)

        result = (Right(10)
                  .flat_map(lambda x: divide(x, 2))
                  .flat_map(lambda x: divide(x, 0))
                  .fold(
                      lambda l: f"Error: {l}",
                      lambda r: f"Result: {r}"
                  ))
        assert result == "Error: Division by zero"

    def test_equality(self):
        assert Right(5) == Right(5)
        assert Left("error") == Left("error")
        assert Right(5) != Right(6)
        assert Left("a") != Left("b")
        assert Right(5) != Left(5)

    def test_repr(self):
        assert repr(Right(5)) == "Right(5)"
        assert repr(Left("error")) == "Left('error')"
