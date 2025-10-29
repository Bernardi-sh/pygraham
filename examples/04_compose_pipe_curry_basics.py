"""
Function Composition, Pipe, and Curry - Basic Tutorial

These tools help you combine small functions into larger ones.

COMPOSE: Combine functions right-to-left (like math: f(g(x)))
PIPE: Combine functions left-to-right (more natural reading)
CURRY: Transform function to accept one argument at a time

Why use them?
- Build complex operations from simple pieces
- Reusable function building blocks
- Clear data transformation pipelines
- No temporary variables needed
"""

from pygraham import compose, pipe, curry

print("=" * 80)
print("COMPOSE, PIPE, CURRY - BASIC EXAMPLES")
print("=" * 80)

# =============================================================================
# COMPOSE: Right-to-left function composition
# =============================================================================

print("\n1. COMPOSE: Right-to-left composition")
print("-" * 80)

# Simple functions
def add_one(x):
    return x + 1


def double(x):
    return x * 2


def square(x):
    return x**2


# Traditional nested calls (hard to read)
result = square(double(add_one(3)))
print("Nested: square(double(add_one(3))) =", result)  # ((3+1)*2)^2 = 64

# Using compose (reads right-to-left like math notation)
f = compose(square, double, add_one)
result = f(3)
print("Compose: compose(square, double, add_one)(3) =", result)  # 64

# How it works:
# add_one(3) -> 4
# double(4) -> 8
# square(8) -> 64

print("\nStep by step:")
print("  add_one(3) =", add_one(3))  # 4
print("  double(4) =", double(4))  # 8
print("  square(8) =", square(8))  # 64

# Another example
add_ten = lambda x: x + 10
multiply_by_three = lambda x: x * 3

f = compose(multiply_by_three, add_ten)
result = f(5)
print("\ncompose(x*3, x+10)(5):", result)  # (5+10)*3 = 45

# =============================================================================
# PIPE: Left-to-right function composition
# =============================================================================

print("\n2. PIPE: Left-to-right composition (easier to read)")
print("-" * 80)

# Same functions as before
# Pipe reads naturally from left to right
f = pipe(add_one, double, square)
result = f(3)
print("pipe(add_one, double, square)(3) =", result)  # 64

# Easier to understand:
# 3 -> add_one -> 4 -> double -> 8 -> square -> 64

# Another example: text processing pipeline
def remove_spaces(text):
    return text.replace(" ", "")


def uppercase(text):
    return text.upper()


def add_exclamation(text):
    return text + "!"


# Create text processing function
process_text = pipe(remove_spaces, uppercase, add_exclamation)

result = process_text("hello world")
print("\nText processing pipeline:")
print("  Input: 'hello world'")
print("  Output:", result)  # HELLOWORLD!

# Step by step:
print("\n  Step 1 (remove spaces):", remove_spaces("hello world"))  # helloworld
print("  Step 2 (uppercase):", uppercase("helloworld"))  # HELLOWORLD
print("  Step 3 (add !):", add_exclamation("HELLOWORLD"))  # HELLOWORLD!

# =============================================================================
# COMPOSE vs PIPE: When to use which?
# =============================================================================

print("\n3. COMPOSE vs PIPE")
print("-" * 80)

x = 10

# Compose: Right-to-left (like math notation f∘g∘h)
composed = compose(square, double, add_one)
print("Compose (R→L):", composed(x))  # ((10+1)*2)^2 = 484

# Pipe: Left-to-right (like data flow)
piped = pipe(add_one, double, square)
print("Pipe (L→R):", piped(x))  # ((10+1)*2)^2 = 484

# Same result, different reading order
# Use PIPE for data transformations (more intuitive)
# Use COMPOSE for mathematical operations (traditional notation)

# =============================================================================
# CURRY: Partial application of functions
# =============================================================================

print("\n4. CURRY: Transform multi-arg function to single-arg chain")
print("-" * 80)


# Regular function: takes all arguments at once
def add_three_numbers(a, b, c):
    return a + b + c


result = add_three_numbers(1, 2, 3)
print("Regular function: add_three_numbers(1, 2, 3) =", result)  # 6


# Curried version: can take arguments one at a time
@curry
def add_three_curried(a, b, c):
    return a + b + c


# All at once (still works)
result = add_three_curried(1, 2, 3)
print("\nCurried (all at once): add_three_curried(1, 2, 3) =", result)  # 6

# One at a time
result = add_three_curried(1)(2)(3)
print("Curried (one by one): add_three_curried(1)(2)(3) =", result)  # 6

# Partial application
add_one_and_two = add_three_curried(1, 2)  # Partially applied
result = add_one_and_two(3)
print("Partial application: add_one_and_two(3) =", result)  # 6

# Create specialized functions
add_five = add_three_curried(2, 3)  # Function waiting for last arg
print("add_five(10) =", add_five(10))  # 2 + 3 + 10 = 15
print("add_five(20) =", add_five(20))  # 2 + 3 + 20 = 25

# =============================================================================
# REAL WORLD: Curry for configuration
# =============================================================================

print("\n5. REAL WORLD: Curry for reusable configurations")
print("-" * 80)


@curry
def format_message(prefix, suffix, message):
    return f"{prefix} {message} {suffix}"


# Create specialized formatters
error_formatter = format_message("[ERROR]", "!!!")
warning_formatter = format_message("[WARNING]", ".")
info_formatter = format_message("[INFO]", "")

print("Error:", error_formatter("Database connection failed"))
print("Warning:", warning_formatter("Low disk space"))
print("Info:", info_formatter("Server started"))

# Another example: HTTP requests
@curry
def make_request(method, base_url, endpoint):
    return f"{method} {base_url}{endpoint}"


# Configure for specific API
api_get = make_request("GET", "https://api.example.com")
api_post = make_request("POST", "https://api.example.com")

print("\nAPI requests:")
print(api_get("/users"))  # GET https://api.example.com/users
print(api_get("/posts"))  # GET https://api.example.com/posts
print(api_post("/users"))  # POST https://api.example.com/users

# =============================================================================
# COMBINING COMPOSE, PIPE, AND CURRY
# =============================================================================

print("\n6. COMBINING: Compose + Pipe + Curry")
print("-" * 80)


# Curried functions for data processing
@curry
def multiply_by(factor, x):
    return x * factor


@curry
def add(n, x):
    return x + n


@curry
def power(exp, x):
    return x**exp


# Create specialized functions
double = multiply_by(2)
add_ten = add(10)
square = power(2)

# Compose them into pipeline
process = pipe(add_ten, double, square)

result = process(5)
print("Pipeline: (5 + 10) * 2 ^ 2 =", result)  # (5+10)*2^2 = 900

# Create different pipelines from same building blocks
pipeline1 = pipe(double, add_ten)
pipeline2 = pipe(add_ten, square)
pipeline3 = pipe(square, double, add_ten)

print("\nDifferent pipelines with same functions:")
print("  double then add_ten:", pipeline1(5))  # (5*2)+10 = 20
print("  add_ten then square:", pipeline2(5))  # (5+10)^2 = 225
print("  square, double, add_ten:", pipeline3(5))  # (5^2)*2+10 = 60

# =============================================================================
# REAL WORLD: Data transformation pipeline
# =============================================================================

print("\n7. REAL WORLD: E-commerce order processing")
print("-" * 80)


# Building blocks
@curry
def apply_discount(percent, price):
    return price * (1 - percent / 100)


@curry
def add_tax(percent, price):
    return price * (1 + percent / 100)


@curry
def add_shipping(cost, price):
    return price + cost


# Create pricing pipelines
standard_pricing = pipe(apply_discount(10), add_tax(8), add_shipping(5))

premium_pricing = pipe(apply_discount(20), add_tax(8), add_shipping(0))  # Free shipping

print("Standard order ($100):", f"${standard_pricing(100):.2f}")
# $100 -> $90 (10% off) -> $97.20 (8% tax) -> $102.20 (+$5 shipping)

print("Premium order ($100):", f"${premium_pricing(100):.2f}")
# $100 -> $80 (20% off) -> $86.40 (8% tax) -> $86.40 (free shipping)

# =============================================================================
# REAL WORLD: Text processing
# =============================================================================

print("\n8. REAL WORLD: Data cleaning pipeline")
print("-" * 80)


def trim(text):
    return text.strip()


def lowercase(text):
    return text.lower()


def remove_punctuation(text):
    return "".join(c for c in text if c.isalnum() or c.isspace())


def normalize_spaces(text):
    return " ".join(text.split())


# Create cleaning pipeline
clean_text = pipe(trim, lowercase, remove_punctuation, normalize_spaces)

dirty_text = "  Hello,  WORLD!!!  How  are   YOU?  "
clean = clean_text(dirty_text)

print("Dirty text:", repr(dirty_text))
print("Clean text:", repr(clean))  # 'hello world how are you'

# =============================================================================
# REAL WORLD: Number processing
# =============================================================================

print("\n9. REAL WORLD: Math calculation pipeline")
print("-" * 80)


@curry
def clamp(min_val, max_val, x):
    """Limit value between min and max."""
    return max(min_val, min(max_val, x))


@curry
def round_to(decimals, x):
    """Round to N decimal places."""
    return round(x, decimals)


# Create validators
validate_percentage = pipe(
    clamp(0, 100),  # Ensure 0-100
    round_to(2),  # Round to 2 decimals
)

print("validate_percentage(150):", validate_percentage(150))  # 100
print("validate_percentage(-10):", validate_percentage(-10))  # 0
print("validate_percentage(45.6789):", validate_percentage(45.6789))  # 45.68

# Temperature converter
celsius_to_fahrenheit = lambda c: c * 9 / 5 + 32
fahrenheit_to_celsius = lambda f: (f - 32) * 5 / 9

# With rounding
convert_to_f = pipe(celsius_to_fahrenheit, round_to(1))
convert_to_c = pipe(fahrenheit_to_celsius, round_to(1))

print("\nTemperature conversion:")
print("  25°C =", convert_to_f(25), "°F")  # 77.0
print("  77°F =", convert_to_c(77), "°C")  # 25.0

# =============================================================================
# PRACTICAL TIPS
# =============================================================================

print("\n10. PRACTICAL TIPS")
print("-" * 80)

print(
    """
When to use COMPOSE:
- Mathematical operations
- When you think in terms of function composition (f∘g∘h)
- Working with mathematical libraries

When to use PIPE:
- Data transformations
- When you want to read left-to-right
- Building processing pipelines
- Most real-world use cases

When to use CURRY:
- Creating specialized functions from general ones
- Configuration (set some args, use later)
- Building function libraries
- When you need partial application

Combine them:
- Create curried building blocks
- Compose them with pipe
- Build reusable, configurable pipelines
"""
)

# Example of all three together
@curry
def multiply(a, b):
    return a * b


@curry
def subtract(a, b):
    return b - a  # Note: order matters!


# Create specialized functions
double = multiply(2)
triple = multiply(3)
subtract_five = subtract(5)

# Combine into pipelines
pipeline_a = pipe(double, subtract_five)
pipeline_b = pipe(triple, subtract_five)

print("Pipeline A (double then -5):", pipeline_a(10))  # (10*2)-5 = 15
print("Pipeline B (triple then -5):", pipeline_b(10))  # (10*3)-5 = 25

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================

print("\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)
print(
    """
1. COMPOSE: Right-to-left composition (like math)
2. PIPE: Left-to-right composition (easier to read)
3. CURRY: Transform function to take args one at a time
4. Build complex operations from simple functions
5. Create reusable function building blocks
6. Pipelines are clear and maintainable
7. Curry enables partial application
8. Combine all three for powerful abstractions
9. No temporary variables needed
10. Pure functions = easy to test and reason about
"""
)
