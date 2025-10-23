"""
Tests for Maybe monad
"""
import pytest
from pygraham import Maybe, Just, Nothing


class TestMaybe:
    def test_just_creation(self):
        m = Just(5)
        assert m.is_just()
        assert not m.is_nothing()
        assert m.get() == 5

    def test_nothing_creation(self):
        m = Nothing()
        assert m.is_nothing()
        assert not m.is_just()

    def test_of_with_value(self):
        m = Maybe.of(10)
        assert m.is_just()
        assert m.get() == 10

    def test_of_with_none(self):
        m = Maybe.of(None)
        assert m.is_nothing()

    def test_get_or_else_just(self):
        m = Just(5)
        assert m.get_or_else(10) == 5

    def test_get_or_else_nothing(self):
        m = Nothing()
        assert m.get_or_else(10) == 10

    def test_map_just(self):
        m = Just(5)
        result = m.map(lambda x: x * 2)
        assert result.get() == 10

    def test_map_nothing(self):
        m = Nothing()
        result = m.map(lambda x: x * 2)
        assert result.is_nothing()

    def test_flat_map_just(self):
        m = Just(5)
        result = m.flat_map(lambda x: Just(x * 2))
        assert result.get() == 10

    def test_flat_map_to_nothing(self):
        m = Just(5)
        result = m.flat_map(lambda x: Nothing())
        assert result.is_nothing()

    def test_flat_map_nothing(self):
        m = Nothing()
        result = m.flat_map(lambda x: Just(x * 2))
        assert result.is_nothing()

    def test_filter_match(self):
        m = Just(5)
        result = m.filter(lambda x: x > 3)
        assert result.is_just()
        assert result.get() == 5

    def test_filter_no_match(self):
        m = Just(5)
        result = m.filter(lambda x: x > 10)
        assert result.is_nothing()

    def test_filter_nothing(self):
        m = Nothing()
        result = m.filter(lambda x: True)
        assert result.is_nothing()

    def test_or_else_just(self):
        m = Just(5)
        result = m.or_else(Just(10))
        assert result.get() == 5

    def test_or_else_nothing(self):
        m = Nothing()
        result = m.or_else(Just(10))
        assert result.get() == 10

    def test_chaining(self):
        result = (Just(5)
                  .map(lambda x: x * 2)
                  .filter(lambda x: x > 5)
                  .map(lambda x: x + 1)
                  .get_or_else(0))
        assert result == 11

    def test_equality(self):
        assert Just(5) == Just(5)
        assert Nothing() == Nothing()
        assert Just(5) != Just(6)
        assert Just(5) != Nothing()

    def test_bool_conversion(self):
        assert bool(Just(5)) is True
        assert bool(Nothing()) is False

    def test_repr(self):
        assert repr(Just(5)) == "Just(5)"
        assert repr(Nothing()) == "Nothing"
