"""
Tests for pattern matching
"""
import pytest
from pygraham import match, case, _, Match, instance_of, has_attr, in_range


class TestPatternMatching:
    def test_exact_match(self):
        result = match(5,
                       case(5, lambda x: "five"),
                       case(10, lambda x: "ten"))
        assert result == "five"

    def test_wildcard_match(self):
        result = match(100,
                       case(5, lambda x: "five"),
                       case(_, lambda x: "other"))
        assert result == "other"

    def test_type_match(self):
        result = match("hello",
                       case(int, lambda x: "integer"),
                       case(str, lambda x: "string"))
        assert result == "string"

    def test_predicate_match(self):
        result = match(15,
                       case(lambda x: x < 10, lambda x: "small"),
                       case(lambda x: x < 20, lambda x: "medium"),
                       case(lambda x: x >= 20, lambda x: "large"))
        assert result == "medium"

    def test_no_match_raises(self):
        with pytest.raises(ValueError):
            match(100,
                  case(1, lambda x: "one"),
                  case(2, lambda x: "two"))

    def test_complex_pattern(self):
        def classify_number(n):
            return match(n,
                         case(0, lambda x: "zero"),
                         case(lambda x: x < 0, lambda x: "negative"),
                         case(lambda x: 0 < x < 10, lambda x: "small positive"),
                         case(lambda x: x >= 10, lambda x: "large positive"))

        assert classify_number(0) == "zero"
        assert classify_number(-5) == "negative"
        assert classify_number(5) == "small positive"
        assert classify_number(100) == "large positive"

    def test_fluent_interface(self):
        result = (Match(5)
                  .case(1, lambda x: "one")
                  .case(2, lambda x: "two")
                  .case(5, lambda x: "five")
                  .execute())
        assert result == "five"

    def test_fluent_with_default(self):
        result = (Match(100)
                  .case(1, lambda x: "one")
                  .case(2, lambda x: "two")
                  .default(lambda x: "other")
                  .execute())
        assert result == "other"

    def test_instance_of_helper(self):
        predicate = instance_of(int, float)
        assert predicate(5) is True
        assert predicate(5.5) is True
        assert predicate("string") is False

    def test_has_attr_helper(self):
        predicate = has_attr("append")
        assert predicate([]) is True
        assert predicate({}) is False

    def test_in_range_helper(self):
        predicate = in_range(10, 20)
        assert predicate(15) is True
        assert predicate(5) is False
        assert predicate(25) is False

    def test_custom_type_matching(self):
        class Dog:
            pass

        class Cat:
            pass

        result = match(Dog(),
                       case(Dog, lambda x: "woof"),
                       case(Cat, lambda x: "meow"))
        assert result == "woof"

    def test_list_length_matching(self):
        def describe_list(lst):
            return match(len(lst),
                         case(0, lambda x: "empty"),
                         case(1, lambda x: "single"),
                         case(lambda x: x > 1, lambda x: "multiple"))

        assert describe_list([]) == "empty"
        assert describe_list([1]) == "single"
        assert describe_list([1, 2, 3]) == "multiple"
