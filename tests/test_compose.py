"""
Tests for function composition
"""

import pytest
from pygraham import compose, pipe, curry


class TestCompose:
    def test_compose_single_function(self):
        f = compose(lambda x: x * 2)
        assert f(5) == 10

    def test_compose_multiple_functions(self):
        add_one = lambda x: x + 1
        double = lambda x: x * 2
        f = compose(double, add_one)
        assert f(3) == 8  # (3 + 1) * 2

    def test_compose_three_functions(self):
        add_one = lambda x: x + 1
        double = lambda x: x * 2
        square = lambda x: x**2
        f = compose(square, double, add_one)
        assert f(3) == 64  # ((3 + 1) * 2) ** 2 = 8 ** 2

    def test_pipe_single_function(self):
        f = pipe(lambda x: x * 2)
        assert f(5) == 10

    def test_pipe_multiple_functions(self):
        add_one = lambda x: x + 1
        double = lambda x: x * 2
        f = pipe(add_one, double)
        assert f(3) == 8  # (3 + 1) * 2

    def test_pipe_three_functions(self):
        add_one = lambda x: x + 1
        double = lambda x: x * 2
        square = lambda x: x**2
        f = pipe(add_one, double, square)
        assert f(3) == 64  # ((3 + 1) * 2) ** 2

    def test_compose_vs_pipe(self):
        add_one = lambda x: x + 1
        double = lambda x: x * 2

        composed = compose(double, add_one)
        piped = pipe(add_one, double)

        assert composed(5) == piped(5)


class TestCurry:
    def test_curry_two_args(self):
        @curry
        def add(a, b):
            return a + b

        assert add(2)(3) == 5
        assert add(2, 3) == 5

    def test_curry_three_args(self):
        @curry
        def add_three(a, b, c):
            return a + b + c

        assert add_three(1)(2)(3) == 6
        assert add_three(1, 2)(3) == 6
        assert add_three(1)(2, 3) == 6
        assert add_three(1, 2, 3) == 6

    def test_curry_with_multiply(self):
        @curry
        def multiply(a, b, c):
            return a * b * c

        times_two = multiply(2)
        times_two_three = times_two(3)

        assert times_two_three(4) == 24
        assert times_two(3, 4) == 24

    def test_curry_partial_application(self):
        @curry
        def greet(greeting, name):
            return f"{greeting}, {name}!"

        hello = greet("Hello")
        assert hello("World") == "Hello, World!"
        assert hello("Python") == "Hello, Python!"
