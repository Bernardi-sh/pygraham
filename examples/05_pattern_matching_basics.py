"""
Pattern Matching - Basic Tutorial

Pattern matching lets you handle different cases elegantly, like a powerful
switch statement on steroids.

Instead of many if-elif-else chains, you can match on:
- Exact values
- Types
- Predicates (custom conditions)
- Wildcards (catch-all)

Why use pattern matching?
- More readable than if-elif chains
- Ensures all cases are handled
- Natural for handling different data types
- Declarative (what, not how)
"""

from pygraham import match, case, _, Match, instance_of, in_range, has_attr

print("=" * 80)
print("PATTERN MATCHING - BASIC EXAMPLES")
print("=" * 80)

# =============================================================================
# PROBLEM: Traditional if-elif chains
# =============================================================================

print("\n1. THE PROBLEM: if-elif chains")
print("-" * 80)


def describe_number_traditional(n):
    """Traditional approach with if-elif."""
    if n == 0:
        return "zero"
    elif n < 0:
        return "negative"
    elif n < 10:
        return "small positive"
    elif n < 100:
        return "medium positive"
    else:
        return "large positive"


print("Traditional if-elif:")
print("  0 ->", describe_number_traditional(0))
print("  -5 ->", describe_number_traditional(-5))
print("  5 ->", describe_number_traditional(5))
print("  50 ->", describe_number_traditional(50))
print("  500 ->", describe_number_traditional(500))

print("\nProblem: Verbose, imperative, hard to see all cases at once")

# =============================================================================
# SOLUTION: Pattern matching
# =============================================================================

print("\n2. THE SOLUTION: Pattern matching")
print("-" * 80)


def describe_number_match(n):
    """Pattern matching approach."""
    return match(
        n,
        case(0, lambda x: "zero"),
        case(lambda x: x < 0, lambda x: "negative"),
        case(lambda x: x < 10, lambda x: "small positive"),
        case(lambda x: x < 100, lambda x: "medium positive"),
        case(_, lambda x: "large positive"),  # Wildcard catches all
    )


print("Pattern matching:")
print("  0 ->", describe_number_match(0))
print("  -5 ->", describe_number_match(-5))
print("  5 ->", describe_number_match(5))
print("  50 ->", describe_number_match(50))
print("  500 ->", describe_number_match(500))

print("\nSolution: Declarative, all cases visible, cleaner!")

# =============================================================================
# EXACT VALUE MATCHING
# =============================================================================

print("\n3. EXACT VALUE MATCHING")
print("-" * 80)


def day_type(day):
    """Match exact day names."""
    return match(
        day,
        case("Monday", lambda _: "Start of work week"),
        case("Friday", lambda _: "End of work week"),
        case("Saturday", lambda _: "Weekend!"),
        case("Sunday", lambda _: "Weekend!"),
        case(_, lambda d: f"Regular day: {d}"),
    )


print("Monday ->", day_type("Monday"))
print("Friday ->", day_type("Friday"))
print("Saturday ->", day_type("Saturday"))
print("Tuesday ->", day_type("Tuesday"))

# Number matching
def describe_roll(roll):
    """Match dice roll."""
    return match(
        roll,
        case(1, lambda _: "Snake eyes!"),
        case(6, lambda _: "Lucky!"),
        case(_, lambda n: f"You rolled {n}"),
    )


print("\nDice rolls:")
print("  1 ->", describe_roll(1))
print("  6 ->", describe_roll(6))
print("  4 ->", describe_roll(4))

# =============================================================================
# TYPE MATCHING
# =============================================================================

print("\n4. TYPE MATCHING")
print("-" * 80)


def describe_type(value):
    """Match based on type."""
    return match(
        value,
        case(int, lambda x: f"Integer: {x}"),
        case(str, lambda x: f"String: {x}"),
        case(list, lambda x: f"List with {len(x)} items"),
        case(dict, lambda x: f"Dict with {len(x)} keys"),
        case(_, lambda x: f"Unknown type: {type(x)}"),
    )


print("Type matching:")
print("  42 ->", describe_type(42))
print("  'hello' ->", describe_type("hello"))
print("  [1,2,3] ->", describe_type([1, 2, 3]))
print("  {'a':1} ->", describe_type({"a": 1}))
print("  3.14 ->", describe_type(3.14))

# =============================================================================
# PREDICATE MATCHING (Custom conditions)
# =============================================================================

print("\n5. PREDICATE MATCHING (Custom conditions)")
print("-" * 80)


def classify_age(age):
    """Match using predicates."""
    return match(
        age,
        case(lambda a: a < 0, lambda _: "Invalid age"),
        case(lambda a: a < 13, lambda a: f"Child ({a})"),
        case(lambda a: a < 20, lambda a: f"Teenager ({a})"),
        case(lambda a: a < 65, lambda a: f"Adult ({a})"),
        case(_, lambda a: f"Senior ({a})"),
    )


print("Age classification:")
print("  -5 ->", classify_age(-5))
print("  8 ->", classify_age(8))
print("  16 ->", classify_age(16))
print("  35 ->", classify_age(35))
print("  70 ->", classify_age(70))

# String predicates
def classify_string(s):
    """Match string properties."""
    return match(
        s,
        case(lambda x: len(x) == 0, lambda _: "Empty string"),
        case(lambda x: x.isdigit(), lambda x: f"Number string: {x}"),
        case(lambda x: x.isalpha(), lambda x: f"Letters only: {x}"),
        case(lambda x: x.isupper(), lambda x: f"UPPERCASE: {x}"),
        case(_, lambda x: f"Mixed: {x}"),
    )


print("\nString classification:")
print("  '' ->", classify_string(""))
print("  '123' ->", classify_string("123"))
print("  'hello' ->", classify_string("hello"))
print("  'WORLD' ->", classify_string("WORLD"))
print("  'Hi123' ->", classify_string("Hi123"))

# =============================================================================
# WILDCARD (_) - Catch all remaining cases
# =============================================================================

print("\n6. WILDCARD (_) - Default case")
print("-" * 80)


def grade_score(score):
    """Match score ranges with wildcard default."""
    return match(
        score,
        case(lambda s: s >= 90, lambda _: "A"),
        case(lambda s: s >= 80, lambda _: "B"),
        case(lambda s: s >= 70, lambda _: "C"),
        case(lambda s: s >= 60, lambda _: "D"),
        case(_, lambda _: "F"),  # Everything else
    )


print("Grade scores:")
print("  95 ->", grade_score(95))
print("  85 ->", grade_score(85))
print("  75 ->", grade_score(75))
print("  65 ->", grade_score(65))
print("  50 ->", grade_score(50))

# =============================================================================
# HELPER FUNCTIONS: instance_of, in_range, has_attr
# =============================================================================

print("\n7. HELPER FUNCTIONS")
print("-" * 80)

# instance_of - check multiple types
def describe_value(value):
    """Using instance_of helper."""
    return match(
        value,
        case(instance_of(int, float), lambda x: f"Number: {x}"),
        case(instance_of(str), lambda x: f"String: {x}"),
        case(instance_of(list, tuple), lambda x: f"Sequence: {x}"),
        case(_, lambda x: f"Other: {x}"),
    )


print("instance_of helper:")
print("  42 ->", describe_value(42))
print("  3.14 ->", describe_value(3.14))
print("  'hi' ->", describe_value("hi"))
print("  [1,2] ->", describe_value([1, 2]))

# in_range - check if value in range
def classify_temperature(temp):
    """Using in_range helper."""
    return match(
        temp,
        case(in_range(-100, 0), lambda t: f"Freezing: {t}°C"),
        case(in_range(0, 15), lambda t: f"Cold: {t}°C"),
        case(in_range(15, 25), lambda t: f"Mild: {t}°C"),
        case(in_range(25, 35), lambda t: f"Warm: {t}°C"),
        case(_, lambda t: f"Hot: {t}°C"),
    )


print("\nin_range helper:")
print("  -10 ->", classify_temperature(-10))
print("  10 ->", classify_temperature(10))
print("  20 ->", classify_temperature(20))
print("  30 ->", classify_temperature(30))
print("  40 ->", classify_temperature(40))


# has_attr - check if object has attribute
class User:
    def __init__(self, name, email=None):
        self.name = name
        if email:
            self.email = email


def describe_user(user):
    """Using has_attr helper."""
    return match(
        user,
        case(has_attr("email"), lambda u: f"User {u.name} with email {u.email}"),
        case(has_attr("name"), lambda u: f"User {u.name} (no email)"),
        case(_, lambda _: "Unknown user"),
    )


print("\nhas_attr helper:")
print("  With email ->", describe_user(User("Alice", "alice@example.com")))
print("  Without email ->", describe_user(User("Bob")))

# =============================================================================
# FLUENT INTERFACE: Match class
# =============================================================================

print("\n8. FLUENT INTERFACE: Match class")
print("-" * 80)


def classify_number_fluent(n):
    """Using Match class for fluent API."""
    return (
        Match(n)
        .case(0, lambda x: "zero")
        .case(lambda x: x < 0, lambda x: "negative")
        .case(lambda x: x < 10, lambda x: "small")
        .case(lambda x: x < 100, lambda x: "medium")
        .default(lambda x: "large")
        .execute()
    )


print("Fluent API:")
print("  0 ->", classify_number_fluent(0))
print("  -5 ->", classify_number_fluent(-5))
print("  5 ->", classify_number_fluent(5))
print("  50 ->", classify_number_fluent(50))
print("  500 ->", classify_number_fluent(500))

# =============================================================================
# REAL WORLD: HTTP status codes
# =============================================================================

print("\n9. REAL WORLD: HTTP status code handler")
print("-" * 80)


def handle_http_status(status_code):
    """Handle different HTTP status codes."""
    return match(
        status_code,
        case(200, lambda _: "OK - Success"),
        case(201, lambda _: "Created - Resource created"),
        case(204, lambda _: "No Content - Success, no data"),
        case(400, lambda _: "Bad Request - Invalid input"),
        case(401, lambda _: "Unauthorized - Authentication required"),
        case(403, lambda _: "Forbidden - Access denied"),
        case(404, lambda _: "Not Found - Resource doesn't exist"),
        case(in_range(400, 499), lambda c: f"Client Error: {c}"),
        case(in_range(500, 599), lambda c: f"Server Error: {c}"),
        case(_, lambda c: f"Unknown status: {c}"),
    )


print("HTTP status handling:")
print("  200 ->", handle_http_status(200))
print("  404 ->", handle_http_status(404))
print("  418 ->", handle_http_status(418))
print("  500 ->", handle_http_status(500))

# =============================================================================
# REAL WORLD: Command processing
# =============================================================================

print("\n10. REAL WORLD: Command line parser")
print("-" * 80)


def process_command(cmd):
    """Process different command types."""
    if isinstance(cmd, str):
        parts = cmd.split()
        command = parts[0] if parts else ""
        args = parts[1:] if len(parts) > 1 else []

        return match(
            command,
            case("help", lambda _: "Showing help..."),
            case("exit", lambda _: "Exiting..."),
            case("save", lambda _: f"Saving file: {args[0]}" if args else "Error: No filename"),
            case("load", lambda _: f"Loading file: {args[0]}" if args else "Error: No filename"),
            case(
                lambda c: c.startswith("set"),
                lambda _: f"Setting {args[0]}={args[1]}" if len(args) >= 2 else "Error: Invalid set command",
            ),
            case(_, lambda c: f"Unknown command: {c}"),
        )
    return "Invalid command format"


print("Command processing:")
print("  'help' ->", process_command("help"))
print("  'exit' ->", process_command("exit"))
print("  'save file.txt' ->", process_command("save file.txt"))
print("  'set debug true' ->", process_command("set debug true"))
print("  'unknown' ->", process_command("unknown"))

# =============================================================================
# REAL WORLD: Data validation
# =============================================================================

print("\n11. REAL WORLD: Input validation")
print("-" * 80)


def validate_input(value):
    """Validate different input types."""
    return (
        Match(value)
        .case(lambda v: v is None, lambda _: ("error", "Value cannot be None"))
        .case(lambda v: isinstance(v, str) and len(v) == 0, lambda _: ("error", "String cannot be empty"))
        .case(lambda v: isinstance(v, int) and v < 0, lambda _: ("error", "Number must be positive"))
        .case(lambda v: isinstance(v, list) and len(v) == 0, lambda _: ("error", "List cannot be empty"))
        .case(instance_of(str), lambda v: ("success", f"Valid string: {v}"))
        .case(instance_of(int), lambda v: ("success", f"Valid number: {v}"))
        .case(instance_of(list), lambda v: ("success", f"Valid list with {len(v)} items"))
        .default(lambda v: ("success", f"Valid value: {v}"))
        .execute()
    )


print("Input validation:")
print("  None ->", validate_input(None))
print("  '' ->", validate_input(""))
print("  -5 ->", validate_input(-5))
print("  [] ->", validate_input([]))
print("  'hello' ->", validate_input("hello"))
print("  42 ->", validate_input(42))
print("  [1,2,3] ->", validate_input([1, 2, 3]))

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================

print("\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)
print(
    """
1. Pattern matching replaces if-elif chains
2. Match exact values: case(42, handler)
3. Match types: case(str, handler)
4. Match conditions: case(lambda x: x > 10, handler)
5. Wildcard catches all: case(_, handler)
6. Helpers: instance_of(), in_range(), has_attr()
7. Fluent API with Match class
8. More declarative than imperative
9. All cases visible at once
10. Cleaner and more maintainable code
"""
)
