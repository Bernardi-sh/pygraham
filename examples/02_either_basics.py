"""
Either Monad - Basic Tutorial

The Either monad helps you handle errors explicitly without exceptions.

Think of Either as a box that contains either:
- An error value (Left)
- A success value (Right)

Why use Either?
- Makes errors explicit in the type
- No hidden exceptions
- Forces you to handle errors
- Easy to chain operations
- Errors flow through computation
"""

from pygraham import Either, Left, Right

print("=" * 80)
print("EITHER MONAD - BASIC EXAMPLES")
print("=" * 80)

# =============================================================================
# PROBLEM: Traditional Python approach with exceptions
# =============================================================================

print("\n1. THE PROBLEM: Traditional exception handling")
print("-" * 80)


def divide_traditional(x, y):
    """Traditional approach - raises exception."""
    if y == 0:
        raise ValueError("Division by zero")
    return x / y


def calculate_traditional(a, b, c):
    """Nested try-except blocks - messy!"""
    try:
        result1 = divide_traditional(a, b)
        try:
            result2 = divide_traditional(result1, c)
            return result2
        except ValueError as e:
            return f"Error: {e}"
    except ValueError as e:
        return f"Error: {e}"


print("Success:", calculate_traditional(10, 2, 5))  # 1.0
print("Failure:", calculate_traditional(10, 0, 5))  # Error: Division by zero
print("\nProblem: Nested try-except is hard to read and maintain!")

# =============================================================================
# SOLUTION: Using Either monad
# =============================================================================

print("\n2. THE SOLUTION: Using Either")
print("-" * 80)


def divide_either(x, y):
    """Returns Either - Left(error) or Right(success)."""
    if y == 0:
        return Left("Division by zero")
    return Right(x / y)


def calculate_either(a, b, c):
    """No try-except needed - Either handles it!"""
    return (
        divide_either(a, b)
        .flat_map(lambda result: divide_either(result, c))
        .fold(lambda error: f"Error: {error}", lambda value: f"Success: {value}")
    )


print("Success:", calculate_either(10, 2, 5))  # Success: 1.0
print("Failure:", calculate_either(10, 0, 5))  # Error: Division by zero
print("\nSolution: Clean, composable, no exceptions!")

# =============================================================================
# CREATING EITHER VALUES
# =============================================================================

print("\n3. CREATING EITHER VALUES")
print("-" * 80)

# Create a Right (success value)
success = Right(42)
print("Right(42):", success)
print("Is left (error)?", success.is_left())  # False
print("Is right (success)?", success.is_right())  # True

# Create a Left (error value)
error = Left("Something went wrong")
print("\nLeft('error'):", error)
print("Is left (error)?", error.is_left())  # True
print("Is right (success)?", error.is_right())  # False

# Convention: Left = error, Right = success (right = correct)

# =============================================================================
# MAP: Transform the success value
# =============================================================================

print("\n4. MAP: Transform success values")
print("-" * 80)

# Map transforms Right values
number = Right(5)
doubled = number.map(lambda x: x * 2)
print("Right(5).map(x * 2):")
print("  Value:", doubled.fold(lambda e: e, lambda v: v))  # 10

# Map does nothing to Left values
error = Left("error")
result = error.map(lambda x: x * 2)
print("\nLeft('error').map(x * 2):")
print("  Is still error?", result.is_left())  # True
print("  Error:", result.fold(lambda e: e, lambda v: v))  # error

# Real example: safe string operations
name = Right("alice")
uppercase = name.map(lambda s: s.upper())
print("\nRight('alice').map(upper):", uppercase.fold(lambda e: e, lambda v: v))  # ALICE

# =============================================================================
# MAP_LEFT: Transform the error value
# =============================================================================

print("\n5. MAP_LEFT: Transform error values")
print("-" * 80)

# Map left transforms error messages
error = Left("file not found")
enhanced_error = error.map_left(lambda e: f"ERROR: {e.upper()}")
print("Left('file not found').map_left(enhance):")
print("  Error:", enhanced_error.fold(lambda e: e, lambda v: v))  # ERROR: FILE NOT FOUND

# Map left does nothing to Right values
success = Right(42)
result = success.map_left(lambda e: f"ERROR: {e}")
print("\nRight(42).map_left(enhance):")
print("  Still success?", result.is_right())  # True
print("  Value:", result.fold(lambda e: e, lambda v: v))  # 42

# =============================================================================
# FLAT_MAP: Chain operations that return Either
# =============================================================================

print("\n6. FLAT_MAP: Chain Either-returning operations")
print("-" * 80)


def safe_sqrt(x):
    """Returns Either - Left if negative, Right if valid."""
    if x < 0:
        return Left(f"Cannot take square root of negative number: {x}")
    return Right(x**0.5)


# Chain operations
result = Right(16).flat_map(safe_sqrt)
print("Right(16).flat_map(sqrt):", result.fold(lambda e: e, lambda v: v))  # 4.0

# Fails safely
result = Right(-4).flat_map(safe_sqrt)
print("Right(-4).flat_map(sqrt):", result.fold(lambda e: e, lambda v: v))
# Cannot take square root of negative number: -4

# Chain multiple operations
result = Right(100).flat_map(safe_sqrt).flat_map(safe_sqrt).map(lambda x: round(x, 2))
print("\nRight(100).flat_map(sqrt).flat_map(sqrt):", result.fold(lambda e: e, lambda v: v))
# sqrt(100) = 10, sqrt(10) = 3.16

# If any operation fails, entire chain returns Left
result = Right(100).flat_map(safe_sqrt).map(lambda x: -x).flat_map(safe_sqrt)
print("Chain with failure:", result.fold(lambda e: e, lambda v: v))
# Cannot take square root of negative number: -10.0

# =============================================================================
# FOLD: Handle both cases
# =============================================================================

print("\n7. FOLD: Extract value from Either")
print("-" * 80)

# Fold handles both Left and Right
success = Right(42)
result = success.fold(lambda error: f"Error: {error}", lambda value: f"Success: {value}")
print("Right(42).fold():", result)  # Success: 42

error = Left("something failed")
result = error.fold(lambda error: f"Error: {error}", lambda value: f"Success: {value}")
print("Left('error').fold():", result)  # Error: something failed

# Real example: HTTP response handling
def handle_response(response):
    return response.fold(
        lambda error: {"status": "error", "message": error}, lambda data: {"status": "success", "data": data}
    )


good_response = Right({"user": "alice", "id": 1})
bad_response = Left("404 Not Found")

print("\nGood response:", handle_response(good_response))
print("Bad response:", handle_response(bad_response))

# =============================================================================
# GET_OR_ELSE: Extract value with default
# =============================================================================

print("\n8. GET_OR_ELSE: Safe value extraction")
print("-" * 80)

# Get value if Right
value = Right(42).get_or_else(0)
print("Right(42).get_or_else(0):", value)  # 42

# Get default if Left
value = Left("error").get_or_else(0)
print("Left('error').get_or_else(0):", value)  # 0

# Real example: configuration with fallback
config = Left("config file not found")
port = config.map(lambda c: c.get("port")).get_or_else(8080)
print("\nMissing config, use default:", port)  # 8080

# =============================================================================
# OR_ELSE: Provide alternative Either
# =============================================================================

print("\n9. OR_ELSE: Fallback to alternative")
print("-" * 80)


def get_from_cache(key):
    return Left("Cache miss")


def get_from_database(key):
    return Right("value from DB")


def get_from_api(key):
    return Right("value from API")


# Try cache, fallback to database
value = get_from_cache("user:1").or_else(get_from_database("user:1"))
print("Cache miss, try DB:", value.fold(lambda e: e, lambda v: v))  # value from DB

# Chain multiple fallbacks
value = get_from_cache("user:1").or_else(get_from_database("user:1")).or_else(get_from_api("user:1"))
print("Multiple fallbacks:", value.fold(lambda e: e, lambda v: v))

# =============================================================================
# REAL WORLD EXAMPLE: Validation
# =============================================================================

print("\n10. REAL WORLD: Form validation")
print("-" * 80)


def validate_username(username):
    """Returns Right(username) if valid, Left(error) otherwise."""
    if username is None or len(username) == 0:
        return Left("Username cannot be empty")
    if len(username) < 3:
        return Left("Username must be at least 3 characters")
    if len(username) > 20:
        return Left("Username must be at most 20 characters")
    if not username.isalnum():
        return Left("Username must contain only letters and numbers")
    return Right(username)


def validate_email(email):
    """Returns Right(email) if valid, Left(error) otherwise."""
    if email is None or len(email) == 0:
        return Left("Email cannot be empty")
    if "@" not in email:
        return Left("Email must contain @")
    if "." not in email:
        return Left("Email must contain a domain")
    return Right(email)


def validate_age(age):
    """Returns Right(age) if valid, Left(error) otherwise."""
    if age is None:
        return Left("Age cannot be empty")
    if age < 18:
        return Left("Must be at least 18 years old")
    if age > 120:
        return Left("Invalid age")
    return Right(age)


# Test validation
print("Valid username:", validate_username("alice123").fold(lambda e: f"Error: {e}", lambda v: f"OK: {v}"))
print("Invalid username:", validate_username("ab").fold(lambda e: f"Error: {e}", lambda v: f"OK: {v}"))

print("\nValid email:", validate_email("user@example.com").fold(lambda e: f"Error: {e}", lambda v: f"OK: {v}"))
print("Invalid email:", validate_email("not-an-email").fold(lambda e: f"Error: {e}", lambda v: f"OK: {v}"))

print("\nValid age:", validate_age(25).fold(lambda e: f"Error: {e}", lambda v: f"OK: {v}"))
print("Invalid age:", validate_age(15).fold(lambda e: f"Error: {e}", lambda v: f"OK: {v}"))

# =============================================================================
# REAL WORLD EXAMPLE: File operations
# =============================================================================

print("\n11. REAL WORLD: Safe file operations")
print("-" * 80)


def read_file(filename):
    """Simulates reading a file."""
    files = {"config.txt": "port=8080\nhost=localhost", "data.txt": "some data"}
    if filename not in files:
        return Left(f"File not found: {filename}")
    return Right(files[filename])


def parse_config(content):
    """Parse config content."""
    try:
        config = {}
        for line in content.split("\n"):
            if "=" in line:
                key, value = line.split("=")
                config[key.strip()] = value.strip()
        if not config:
            return Left("Empty configuration")
        return Right(config)
    except Exception as e:
        return Left(f"Parse error: {e}")


def get_port(config):
    """Extract port from config."""
    port = config.get("port")
    if port is None:
        return Left("Port not specified in config")
    try:
        return Right(int(port))
    except ValueError:
        return Left(f"Invalid port: {port}")


# Chain all operations
result = read_file("config.txt").flat_map(parse_config).flat_map(get_port).fold(
    lambda error: f"Failed: {error}", lambda port: f"Server will run on port {port}"
)

print("Read and parse config:", result)

# Test with missing file
result = read_file("missing.txt").flat_map(parse_config).flat_map(get_port).fold(
    lambda error: f"Failed: {error}", lambda port: f"Server will run on port {port}"
)

print("Missing file:", result)

# =============================================================================
# REAL WORLD EXAMPLE: API calls
# =============================================================================

print("\n12. REAL WORLD: API error handling")
print("-" * 80)


def fetch_user(user_id):
    """Simulates API call."""
    users = {1: {"name": "Alice", "email": "alice@example.com"}, 2: {"name": "Bob", "email": "bob@example.com"}}
    if user_id not in users:
        return Left(f"User {user_id} not found")
    return Right(users[user_id])


def fetch_posts(user):
    """Simulates fetching user posts."""
    posts = {
        "alice@example.com": [{"title": "Hello World", "likes": 10}],
        "bob@example.com": [{"title": "Python Tips", "likes": 25}],
    }
    email = user.get("email")
    if email not in posts:
        return Left(f"No posts found for {email}")
    return Right(posts[email])


def calculate_total_likes(posts):
    """Calculate total likes."""
    total = sum(post["likes"] for post in posts)
    return Right(total)


# Chain API calls
result = fetch_user(1).flat_map(fetch_posts).flat_map(calculate_total_likes).fold(
    lambda error: f"Error: {error}", lambda likes: f"Total likes: {likes}"
)

print("Fetch user and count likes:", result)

# Test with missing user
result = fetch_user(999).flat_map(fetch_posts).flat_map(calculate_total_likes).fold(
    lambda error: f"Error: {error}", lambda likes: f"Total likes: {likes}"
)

print("Missing user:", result)

# =============================================================================
# COMBINING MULTIPLE VALIDATIONS
# =============================================================================

print("\n13. COMBINING VALIDATIONS")
print("-" * 80)


def validate_registration(username, email, age):
    """Validate all fields - stops at first error."""
    return (
        validate_username(username)
        .flat_map(lambda u: validate_email(email).map(lambda e: (u, e)))
        .flat_map(lambda ue: validate_age(age).map(lambda a: {"username": ue[0], "email": ue[1], "age": a}))
        .fold(lambda error: f"Validation failed: {error}", lambda user: f"User registered: {user}")
    )


# All valid
print("Valid registration:", validate_registration("alice123", "alice@example.com", 25))

# Invalid username
print("\nInvalid username:", validate_registration("ab", "alice@example.com", 25))

# Invalid email
print("Invalid email:", validate_registration("alice123", "not-an-email", 25))

# Invalid age
print("Invalid age:", validate_registration("alice123", "alice@example.com", 15))

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================

print("\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)
print(
    """
1. Either represents success (Right) or error (Left)
2. Right(value) = success value
3. Left(error) = error value
4. Convention: "Right" means "correct"
5. map() = transform the success value
6. map_left() = transform the error value
7. flat_map() = chain operations that return Either
8. fold() = handle both cases (required!)
9. get_or_else() = extract value with default
10. or_else() = try alternative Either
11. No exceptions thrown - errors are explicit
12. Forces you to handle errors properly
13. Easy to chain operations - errors flow through
14. Makes code safer and more predictable
"""
)
