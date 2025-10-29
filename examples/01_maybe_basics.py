"""
Maybe Monad - Basic Tutorial

The Maybe monad helps you handle optional/missing values safely without
constant None checks and defensive programming.

Think of Maybe as a box that either:
- Contains a value (Just)
- Is empty (Nothing)

Why use Maybe?
- Eliminates None checks
- Makes optional values explicit
- Chains operations safely
- Prevents NullPointerException-style bugs
"""

from pygraham import Maybe, Just, Nothing

print("=" * 80)
print("MAYBE MONAD - BASIC EXAMPLES")
print("=" * 80)

# =============================================================================
# PROBLEM: Traditional Python approach with None
# =============================================================================

print("\n1. THE PROBLEM: Traditional None handling")
print("-" * 80)


def get_user_traditional(user_id: int):
    """Traditional approach - returns None if not found."""
    users = {1: {"name": "Alice", "age": 30}, 2: {"name": "Bob", "age": 25}}
    return users.get(user_id)


def get_age_traditional(user_id: int):
    """Lots of None checks needed!"""
    user = get_user_traditional(user_id)
    if user is None:
        return None

    age = user.get("age")
    if age is None:
        return None

    if age < 0:
        return None

    return age


print("Getting age for user 1:", get_age_traditional(1))  # 30
print("Getting age for user 999:", get_age_traditional(999))  # None
print("\nProblem: Lots of 'if None' checks everywhere!")

# =============================================================================
# SOLUTION: Using Maybe monad
# =============================================================================

print("\n2. THE SOLUTION: Using Maybe")
print("-" * 80)


def get_user_maybe(user_id: int):
    """Returns Maybe - either Just(user) or Nothing()."""
    users = {1: {"name": "Alice", "age": 30}, 2: {"name": "Bob", "age": 25}}
    user = users.get(user_id)
    return Maybe.of(user)  # Automatically wraps in Just or Nothing


def get_age_maybe(user_id: int):
    """No None checks needed - Maybe handles it!"""
    return (
        get_user_maybe(user_id)
        .map(lambda user: user.get("age"))  # Get age if user exists
        .filter(lambda age: age is not None)  # Keep only if age exists
        .filter(lambda age: age >= 0)  # Keep only if age is valid
        .get_or_else(0)  # Default to 0 if anything failed
    )


print("Getting age for user 1:", get_age_maybe(1))  # 30
print("Getting age for user 999:", get_age_maybe(999))  # 0
print("\nSolution: No None checks! Maybe handles it automatically.")

# =============================================================================
# CREATING MAYBE VALUES
# =============================================================================

print("\n3. CREATING MAYBE VALUES")
print("-" * 80)

# Create a Just (contains a value)
just_value = Just(42)
print("Just(42):", just_value)
print("Has value?", not just_value.is_nothing())  # True
print("Get value:", just_value.get())  # 42

# Create a Nothing (empty)
nothing_value = Nothing()
print("\nNothing():", nothing_value)
print("Has value?", not nothing_value.is_nothing())  # False
# print("Get value:", nothing_value.get())  # Would raise ValueError!

# Smart constructor - automatically chooses Just or Nothing
maybe_value = Maybe.of(None)
print("\nMaybe.of(None):", maybe_value)  # Nothing
print("Is nothing?", maybe_value.is_nothing())  # True

maybe_value = Maybe.of("hello")
print("\nMaybe.of('hello'):", maybe_value)  # Just('hello')
print("Is nothing?", maybe_value.is_nothing())  # False

# =============================================================================
# MAP: Transform the value inside Maybe
# =============================================================================

print("\n4. MAP: Transform values safely")
print("-" * 80)

number = Just(5)
doubled = number.map(lambda x: x * 2)
print("Just(5).map(x * 2):", doubled.get())  # 10

# Map on Nothing does nothing!
nothing = Nothing()
result = nothing.map(lambda x: x * 2)
print("Nothing().map(x * 2):", result)  # Still Nothing
print("Is nothing?", result.is_nothing())  # True

# Real example: safe string operations
name = Maybe.of("alice")
uppercase = name.map(lambda s: s.upper())
print("\nMaybe.of('alice').map(upper):", uppercase.get())  # ALICE

missing_name = Maybe.of(None)
result = missing_name.map(lambda s: s.upper())
print("Maybe.of(None).map(upper):", result)  # Nothing (no error!)

# =============================================================================
# FLAT_MAP: Chain operations that return Maybe
# =============================================================================

print("\n5. FLAT_MAP: Chain Maybe-returning operations")
print("-" * 80)


def safe_divide(x, y):
    """Returns Maybe - Just(result) or Nothing if division by zero."""
    if y == 0:
        return Nothing()
    return Just(x / y)


# Chain operations
result = Just(10).flat_map(lambda x: safe_divide(x, 2))
print("Just(10).flat_map(divide by 2):", result.get())  # 5.0

# Fails safely
result = Just(10).flat_map(lambda x: safe_divide(x, 0))
print("Just(10).flat_map(divide by 0):", result)  # Nothing

# Chain multiple operations
result = (
    Just(20)
    .flat_map(lambda x: safe_divide(x, 2))  # 20 / 2 = 10
    .flat_map(lambda x: safe_divide(x, 5))  # 10 / 5 = 2
    .map(lambda x: x + 1)  # 2 + 1 = 3
)
print("\nChained operations:", result.get())  # 3.0

# If any operation fails, entire chain returns Nothing
result = (
    Just(20)
    .flat_map(lambda x: safe_divide(x, 2))  # OK: 10
    .flat_map(lambda x: safe_divide(x, 0))  # FAIL: division by zero
    .map(lambda x: x + 1)  # Skipped!
)
print("Chain with failure:", result)  # Nothing

# =============================================================================
# FILTER: Keep value only if predicate is true
# =============================================================================

print("\n6. FILTER: Conditional filtering")
print("-" * 80)

# Keep value if it passes test
age = Just(25)
adult = age.filter(lambda x: x >= 18)
print("Just(25).filter(>= 18):", adult.get())  # 25

# Filter out value that fails test
age = Just(15)
adult = age.filter(lambda x: x >= 18)
print("Just(15).filter(>= 18):", adult)  # Nothing

# Real example: validate email
email = Maybe.of("user@example.com")
valid_email = email.filter(lambda e: "@" in e and "." in e)
print("\nValid email:", valid_email.get())  # user@example.com

invalid_email = Maybe.of("invalid-email")
valid_email = invalid_email.filter(lambda e: "@" in e and "." in e)
print("Invalid email:", valid_email)  # Nothing

# =============================================================================
# GET_OR_ELSE: Extract value with default
# =============================================================================

print("\n7. GET_OR_ELSE: Safe value extraction")
print("-" * 80)

# Get value if exists
value = Just(42).get_or_else(0)
print("Just(42).get_or_else(0):", value)  # 42

# Get default if Nothing
value = Nothing().get_or_else(0)
print("Nothing().get_or_else(0):", value)  # 0

# Real example: configuration with defaults
config = Maybe.of(None)
port = config.map(lambda c: c.get("port")).get_or_else(8080)
print("\nMissing config, use default port:", port)  # 8080

config = Maybe.of({"port": 3000})
port = config.map(lambda c: c.get("port")).get_or_else(8080)
print("Config present, use configured port:", port)  # 3000

# =============================================================================
# OR_ELSE: Provide alternative Maybe
# =============================================================================

print("\n8. OR_ELSE: Fallback to alternative")
print("-" * 80)

# Use primary value if available
primary = Just(1)
fallback = Just(2)
result = primary.or_else(fallback)
print("Just(1).or_else(Just(2)):", result.get())  # 1

# Use fallback if primary is Nothing
primary = Nothing()
fallback = Just(2)
result = primary.or_else(fallback)
print("Nothing().or_else(Just(2)):", result.get())  # 2

# Real example: try multiple sources
def get_from_cache(key):
    return Nothing()  # Cache miss


def get_from_database(key):
    return Just("value from DB")


value = get_from_cache("user:1").or_else(get_from_database("user:1"))
print("\nTry cache, fallback to DB:", value.get())  # value from DB

# =============================================================================
# REAL WORLD EXAMPLE: Safe dictionary access
# =============================================================================

print("\n9. REAL WORLD: Safe nested dictionary access")
print("-" * 80)

# Deeply nested data
data = {"user": {"profile": {"settings": {"theme": "dark", "notifications": True}}}}


# Traditional approach - lots of checks
def get_theme_traditional(data):
    if data is None:
        return "light"
    user = data.get("user")
    if user is None:
        return "light"
    profile = user.get("profile")
    if profile is None:
        return "light"
    settings = profile.get("settings")
    if settings is None:
        return "light"
    theme = settings.get("theme")
    if theme is None:
        return "light"
    return theme


# Maybe approach - clean and safe
def get_theme_maybe(data):
    return (
        Maybe.of(data)
        .map(lambda d: d.get("user"))
        .map(lambda u: u.get("profile"))
        .map(lambda p: p.get("settings"))
        .map(lambda s: s.get("theme"))
        .get_or_else("light")
    )


print("Traditional approach:", get_theme_traditional(data))
print("Maybe approach:", get_theme_maybe(data))

# Works even with missing data
incomplete_data = {"user": {"profile": {}}}
print("\nWith incomplete data:")
print("Maybe approach:", get_theme_maybe(incomplete_data))  # light (default)

# =============================================================================
# REAL WORLD EXAMPLE: Form validation
# =============================================================================

print("\n10. REAL WORLD: Form validation")
print("-" * 80)


def validate_username(username):
    """Returns Just(username) if valid, Nothing otherwise."""
    return (
        Maybe.of(username)
        .filter(lambda u: u is not None)
        .filter(lambda u: len(u) >= 3)
        .filter(lambda u: len(u) <= 20)
        .filter(lambda u: u.isalnum())
    )


def validate_email(email):
    """Returns Just(email) if valid, Nothing otherwise."""
    return Maybe.of(email).filter(lambda e: e is not None).filter(lambda e: "@" in e).filter(lambda e: "." in e)


def validate_age(age):
    """Returns Just(age) if valid, Nothing otherwise."""
    return Maybe.of(age).filter(lambda a: a is not None).filter(lambda a: a >= 18).filter(lambda a: a <= 120)


# Test validation
print("Valid username:", validate_username("alice123").get_or_else("invalid"))
print("Invalid username (too short):", validate_username("ab").get_or_else("invalid"))
print("Invalid username (special chars):", validate_username("alice@123").get_or_else("invalid"))

print("\nValid email:", validate_email("user@example.com").get_or_else("invalid"))
print("Invalid email:", validate_email("not-an-email").get_or_else("invalid"))

print("\nValid age:", validate_age(25).get_or_else("invalid"))
print("Invalid age (too young):", validate_age(15).get_or_else("invalid"))

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================

print("\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)
print(
    """
1. Maybe eliminates None checks
2. Just(value) = contains a value
3. Nothing() = empty/missing value
4. map() = transform the value inside
5. flat_map() = chain operations that return Maybe
6. filter() = keep value only if condition is true
7. get_or_else() = extract value with default
8. or_else() = try alternative Maybe
9. Makes code safer and more readable
10. No more NullPointerException-style bugs!
"""
)
