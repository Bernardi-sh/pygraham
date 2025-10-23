"""
Tests for immutable data structures
"""

import pytest
from pygraham import ImmutableList, ImmutableDict


class TestImmutableList:
    def test_creation(self):
        lst = ImmutableList.of(1, 2, 3)
        assert len(lst) == 3
        assert list(lst) == [1, 2, 3]

    def test_append(self):
        lst = ImmutableList.of(1, 2, 3)
        new_lst = lst.append(4)
        assert list(new_lst) == [1, 2, 3, 4]
        assert list(lst) == [1, 2, 3]  # Original unchanged

    def test_prepend(self):
        lst = ImmutableList.of(2, 3, 4)
        new_lst = lst.prepend(1)
        assert list(new_lst) == [1, 2, 3, 4]
        assert list(lst) == [2, 3, 4]

    def test_concat(self):
        lst1 = ImmutableList.of(1, 2)
        lst2 = ImmutableList.of(3, 4)
        result = lst1.concat(lst2)
        assert list(result) == [1, 2, 3, 4]
        assert list(lst1) == [1, 2]
        assert list(lst2) == [3, 4]

    def test_map(self):
        lst = ImmutableList.of(1, 2, 3)
        result = lst.map(lambda x: x * 2)
        assert list(result) == [2, 4, 6]
        assert list(lst) == [1, 2, 3]

    def test_filter(self):
        lst = ImmutableList.of(1, 2, 3, 4, 5)
        result = lst.filter(lambda x: x % 2 == 0)
        assert list(result) == [2, 4]
        assert list(lst) == [1, 2, 3, 4, 5]

    def test_reduce(self):
        lst = ImmutableList.of(1, 2, 3, 4)
        result = lst.reduce(lambda acc, x: acc + x, 0)
        assert result == 10

    def test_take(self):
        lst = ImmutableList.of(1, 2, 3, 4, 5)
        result = lst.take(3)
        assert list(result) == [1, 2, 3]

    def test_drop(self):
        lst = ImmutableList.of(1, 2, 3, 4, 5)
        result = lst.drop(2)
        assert list(result) == [3, 4, 5]

    def test_reverse(self):
        lst = ImmutableList.of(1, 2, 3)
        result = lst.reverse()
        assert list(result) == [3, 2, 1]

    def test_sort(self):
        lst = ImmutableList.of(3, 1, 4, 1, 5)
        result = lst.sort()
        assert list(result) == [1, 1, 3, 4, 5]

    def test_head(self):
        lst = ImmutableList.of(1, 2, 3)
        assert lst.head() == 1

    def test_head_empty(self):
        lst = ImmutableList()
        assert lst.head() is None

    def test_tail(self):
        lst = ImmutableList.of(1, 2, 3)
        result = lst.tail()
        assert list(result) == [2, 3]

    def test_is_empty(self):
        assert ImmutableList().is_empty()
        assert not ImmutableList.of(1).is_empty()

    def test_getitem(self):
        lst = ImmutableList.of(1, 2, 3)
        assert lst[0] == 1
        assert lst[2] == 3

    def test_add_operator(self):
        lst1 = ImmutableList.of(1, 2)
        lst2 = ImmutableList.of(3, 4)
        result = lst1 + lst2
        assert list(result) == [1, 2, 3, 4]

    def test_equality(self):
        lst1 = ImmutableList.of(1, 2, 3)
        lst2 = ImmutableList.of(1, 2, 3)
        lst3 = ImmutableList.of(1, 2, 4)
        assert lst1 == lst2
        assert lst1 != lst3

    def test_chaining(self):
        result = (
            ImmutableList.of(1, 2, 3, 4, 5)
            .filter(lambda x: x % 2 == 0)
            .map(lambda x: x * 2)
            .append(100)
            .reverse()
        )
        assert list(result) == [100, 8, 4]


class TestImmutableDict:
    def test_creation(self):
        d = ImmutableDict.of(a=1, b=2, c=3)
        assert len(d) == 3
        assert d["a"] == 1

    def test_set(self):
        d = ImmutableDict.of(a=1, b=2)
        new_d = d.set("c", 3)
        assert new_d["c"] == 3
        assert "c" not in d

    def test_set_overwrite(self):
        d = ImmutableDict.of(a=1, b=2)
        new_d = d.set("a", 10)
        assert new_d["a"] == 10
        assert d["a"] == 1

    def test_delete(self):
        d = ImmutableDict.of(a=1, b=2, c=3)
        new_d = d.delete("b")
        assert "b" not in new_d
        assert "b" in d

    def test_update(self):
        d1 = ImmutableDict.of(a=1, b=2)
        d2 = ImmutableDict.of(c=3, d=4)
        result = d1.update(d2)
        assert len(result) == 4
        assert len(d1) == 2

    def test_map_values(self):
        d = ImmutableDict.of(a=1, b=2, c=3)
        result = d.map_values(lambda x: x * 2)
        assert result["a"] == 2
        assert result["b"] == 4

    def test_filter(self):
        d = ImmutableDict.of(a=1, b=2, c=3, d=4)
        result = d.filter(lambda item: item[1] % 2 == 0)
        assert len(result) == 2
        assert "b" in result
        assert "d" in result

    def test_get_or_else(self):
        d = ImmutableDict.of(a=1, b=2)
        assert d.get_or_else("a", 10) == 1
        assert d.get_or_else("c", 10) == 10

    def test_has_key(self):
        d = ImmutableDict.of(a=1, b=2)
        assert d.has_key("a")
        assert not d.has_key("c")

    def test_keys_list(self):
        d = ImmutableDict.of(a=1, b=2, c=3)
        keys = d.keys_list()
        assert len(keys) == 3
        assert "a" in list(keys)

    def test_values_list(self):
        d = ImmutableDict.of(a=1, b=2, c=3)
        values = d.values_list()
        assert len(values) == 3
        assert 1 in list(values)

    def test_items_list(self):
        d = ImmutableDict.of(a=1, b=2)
        items = d.items_list()
        assert len(items) == 2

    def test_is_empty(self):
        assert ImmutableDict().is_empty()
        assert not ImmutableDict.of(a=1).is_empty()

    def test_equality(self):
        d1 = ImmutableDict.of(a=1, b=2)
        d2 = ImmutableDict.of(a=1, b=2)
        d3 = ImmutableDict.of(a=1, b=3)
        assert d1 == d2
        assert d1 != d3

    def test_chaining(self):
        result = (
            ImmutableDict.of(a=1, b=2, c=3)
            .set("d", 4)
            .filter(lambda item: item[1] % 2 == 0)
            .map_values(lambda x: x * 10)
        )
        assert result["b"] == 20
        assert result["d"] == 40
        assert "a" not in result
