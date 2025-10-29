"""
ImmutableList - Basic Tutorial

ImmutableList is a list that never changes. Once created, it stays the same forever.
Operations return NEW lists instead of modifying the original.

Why use ImmutableList?
- Thread-safe (multiple threads can read safely)
- No accidental modifications
- Easy to reason about (doesn't change under you)
- Undo/redo becomes trivial (keep old versions)
- Pure functions (same input = same output)
"""

from pygraham import ImmutableList

print("=" * 80)
print("IMMUTABLELIST - BASIC EXAMPLES")
print("=" * 80)

# =============================================================================
# PROBLEM: Regular Python lists are mutable
# =============================================================================

print("\n1. THE PROBLEM: Mutable lists")
print("-" * 80)

# Regular list - MUTABLE
numbers = [1, 2, 3]
print("Original list:", numbers)

# Modify it
numbers.append(4)
print("After append:", numbers)  # Changed!

# This causes bugs
original = [1, 2, 3]
modified = original  # NOT a copy!
modified.append(4)
print("\nOriginal:", original)  # [1, 2, 3, 4] - CHANGED!
print("Modified:", modified)  # [1, 2, 3, 4]
print("Problem: Modifying one changed both!")

# =============================================================================
# SOLUTION: ImmutableList never changes
# =============================================================================

print("\n2. THE SOLUTION: ImmutableList")
print("-" * 80)

# ImmutableList - IMMUTABLE
numbers = ImmutableList.of(1, 2, 3)
print("Original ImmutableList:", list(numbers))

# "Modify" it - returns NEW list
new_numbers = numbers.append(4)
print("After append:")
print("  Original:", list(numbers))  # [1, 2, 3] - UNCHANGED!
print("  New:", list(new_numbers))  # [1, 2, 3, 4]
print("Solution: Original never changes!")

# =============================================================================
# CREATING IMMUTABLELISTS
# =============================================================================

print("\n3. CREATING IMMUTABLELISTS")
print("-" * 80)

# From individual elements
list1 = ImmutableList.of(1, 2, 3, 4, 5)
print("ImmutableList.of(1, 2, 3, 4, 5):", list(list1))

# From a Python list
list2 = ImmutableList([10, 20, 30])
print("ImmutableList([10, 20, 30]):", list(list2))

# Empty list
empty = ImmutableList()
print("ImmutableList():", list(empty))

# From range
list3 = ImmutableList(range(5))
print("ImmutableList(range(5)):", list(list3))

# =============================================================================
# BASIC OPERATIONS
# =============================================================================

print("\n4. BASIC OPERATIONS")
print("-" * 80)

numbers = ImmutableList.of(1, 2, 3, 4, 5)

# Length
print("Length:", len(numbers))  # 5

# Access by index
print("First element:", numbers[0])  # 1
print("Last element:", numbers[-1])  # 5

# Slicing
print("First 3:", list(numbers[:3]))  # [1, 2, 3]
print("Last 2:", list(numbers[-2:]))  # [4, 5]

# Check if element exists
print("Contains 3?", 3 in numbers)  # True
print("Contains 10?", 10 in numbers)  # False

# Convert to regular list
regular_list = list(numbers)
print("As regular list:", regular_list)

# =============================================================================
# APPEND: Add element to end
# =============================================================================

print("\n5. APPEND: Add to end (returns NEW list)")
print("-" * 80)

numbers = ImmutableList.of(1, 2, 3)
print("Original:", list(numbers))

# Append returns NEW list
new_numbers = numbers.append(4)
print("After append(4):")
print("  Original:", list(numbers))  # [1, 2, 3] - unchanged
print("  New:", list(new_numbers))  # [1, 2, 3, 4]

# Chain multiple appends
result = numbers.append(4).append(5).append(6)
print("\nChain appends:", list(result))  # [1, 2, 3, 4, 5, 6]
print("Original still:", list(numbers))  # [1, 2, 3]

# =============================================================================
# PREPEND: Add element to beginning
# =============================================================================

print("\n6. PREPEND: Add to beginning (returns NEW list)")
print("-" * 80)

numbers = ImmutableList.of(2, 3, 4)
print("Original:", list(numbers))

new_numbers = numbers.prepend(1)
print("After prepend(1):", list(new_numbers))  # [1, 2, 3, 4]
print("Original:", list(numbers))  # [2, 3, 4] - unchanged

# =============================================================================
# MAP: Transform each element
# =============================================================================

print("\n7. MAP: Transform elements")
print("-" * 80)

numbers = ImmutableList.of(1, 2, 3, 4, 5)
print("Original:", list(numbers))

# Double each number
doubled = numbers.map(lambda x: x * 2)
print("Doubled:", list(doubled))  # [2, 4, 6, 8, 10]

# Square each number
squared = numbers.map(lambda x: x**2)
print("Squared:", list(squared))  # [1, 4, 9, 16, 25]

# Convert to strings
strings = numbers.map(str)
print("As strings:", list(strings))  # ['1', '2', '3', '4', '5']

# Real example: process user data
users = ImmutableList.of({"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}, {"name": "Charlie", "age": 35})

names = users.map(lambda user: user["name"])
print("\nUser names:", list(names))  # ['Alice', 'Bob', 'Charlie']

# =============================================================================
# FILTER: Keep only elements that match
# =============================================================================

print("\n8. FILTER: Keep matching elements")
print("-" * 80)

numbers = ImmutableList.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
print("Original:", list(numbers))

# Keep only even numbers
evens = numbers.filter(lambda x: x % 2 == 0)
print("Evens:", list(evens))  # [2, 4, 6, 8, 10]

# Keep only numbers > 5
large = numbers.filter(lambda x: x > 5)
print("Greater than 5:", list(large))  # [6, 7, 8, 9, 10]

# Real example: filter users
users = ImmutableList.of({"name": "Alice", "age": 30}, {"name": "Bob", "age": 17}, {"name": "Charlie", "age": 25})

adults = users.filter(lambda user: user["age"] >= 18)
print("\nAdults:", list(adults))
# [{'name': 'Alice', 'age': 30}, {'name': 'Charlie', 'age': 25}]

# =============================================================================
# REDUCE: Combine elements into single value
# =============================================================================

print("\n9. REDUCE: Combine all elements")
print("-" * 80)

numbers = ImmutableList.of(1, 2, 3, 4, 5)
print("Original:", list(numbers))

# Sum all numbers
total = numbers.reduce(lambda acc, x: acc + x, 0)
print("Sum:", total)  # 15

# Product of all numbers
product = numbers.reduce(lambda acc, x: acc * x, 1)
print("Product:", product)  # 120

# Find maximum
maximum = numbers.reduce(lambda acc, x: max(acc, x), float("-inf"))
print("Maximum:", maximum)  # 5

# Concatenate strings
words = ImmutableList.of("Hello", "World", "from", "Python")
sentence = words.reduce(lambda acc, word: acc + " " + word, "").strip()
print("\nConcatenate:", sentence)  # Hello World from Python

# =============================================================================
# FLAT_MAP: Map and flatten
# =============================================================================

print("\n10. FLAT_MAP: Map then flatten")
print("-" * 80)

# Create nested structure
numbers = ImmutableList.of(1, 2, 3)

# Regular map creates nested lists
nested = numbers.map(lambda x: ImmutableList.of(x, x * 10))
print("With map (nested):", list(list(item) for item in nested))
# [[1, 10], [2, 20], [3, 30]]

# Flat map flattens automatically
flattened = numbers.flat_map(lambda x: ImmutableList.of(x, x * 10))
print("With flat_map:", list(flattened))  # [1, 10, 2, 20, 3, 30]

# Real example: expand ranges
ranges = ImmutableList.of((1, 3), (5, 7), (10, 12))
expanded = ranges.flat_map(lambda r: ImmutableList(range(r[0], r[1])))
print("\nExpanded ranges:", list(expanded))  # [1, 2, 5, 6, 10, 11]

# =============================================================================
# CHAINING OPERATIONS
# =============================================================================

print("\n11. CHAINING OPERATIONS")
print("-" * 80)

numbers = ImmutableList.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
print("Original:", list(numbers))

# Chain multiple operations
result = numbers.filter(lambda x: x % 2 == 0).map(lambda x: x * 2).filter(lambda x: x > 10)

print("Evens, doubled, > 10:", list(result))  # [12, 16, 20]

# Complex chain
numbers = ImmutableList(range(1, 11))
result = (
    numbers.filter(lambda x: x > 3)  # [4, 5, 6, 7, 8, 9, 10]
    .map(lambda x: x**2)  # [16, 25, 36, 49, 64, 81, 100]
    .filter(lambda x: x < 50)  # [16, 25, 36, 49]
    .reduce(lambda acc, x: acc + x, 0)  # 126
)

print("Complex chain result:", result)  # 126

# =============================================================================
# TAKE: Get first N elements
# =============================================================================

print("\n12. TAKE: Get first N elements")
print("-" * 80)

numbers = ImmutableList.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
print("Original:", list(numbers))

first_3 = numbers.take(3)
print("First 3:", list(first_3))  # [1, 2, 3]

first_5 = numbers.take(5)
print("First 5:", list(first_5))  # [1, 2, 3, 4, 5]

# Useful with infinite sequences (when combined with LazySequence)

# =============================================================================
# DROP: Skip first N elements
# =============================================================================

print("\n13. DROP: Skip first N elements")
print("-" * 80)

numbers = ImmutableList.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
print("Original:", list(numbers))

skip_3 = numbers.drop(3)
print("Skip first 3:", list(skip_3))  # [4, 5, 6, 7, 8, 9, 10]

skip_5 = numbers.drop(5)
print("Skip first 5:", list(skip_5))  # [6, 7, 8, 9, 10]

# =============================================================================
# REVERSE: Reverse the list
# =============================================================================

print("\n14. REVERSE: Reverse order")
print("-" * 80)

numbers = ImmutableList.of(1, 2, 3, 4, 5)
print("Original:", list(numbers))

reversed_list = numbers.reverse()
print("Reversed:", list(reversed_list))  # [5, 4, 3, 2, 1]
print("Original unchanged:", list(numbers))  # [1, 2, 3, 4, 5]

# =============================================================================
# SORT: Sort the list
# =============================================================================

print("\n15. SORT: Sort elements")
print("-" * 80)

numbers = ImmutableList.of(5, 2, 8, 1, 9, 3)
print("Original:", list(numbers))

sorted_list = numbers.sort()
print("Sorted:", list(sorted_list))  # [1, 2, 3, 5, 8, 9]

reverse_sorted = numbers.sort(reverse=True)
print("Reverse sorted:", list(reverse_sorted))  # [9, 8, 5, 3, 2, 1]

# Sort with key
words = ImmutableList.of("apple", "pie", "zoo", "a")
by_length = words.sort(key=len)
print("\nSort by length:", list(by_length))  # ['a', 'pie', 'zoo', 'apple']

# =============================================================================
# REAL WORLD EXAMPLE: Process shopping cart
# =============================================================================

print("\n16. REAL WORLD: Shopping cart processing")
print("-" * 80)

cart = ImmutableList.of(
    {"name": "Apple", "price": 1.5, "quantity": 3},
    {"name": "Banana", "price": 0.5, "quantity": 6},
    {"name": "Orange", "price": 2.0, "quantity": 2},
    {"name": "Grape", "price": 3.0, "quantity": 1},
)

# Calculate total for each item
with_totals = cart.map(lambda item: {**item, "total": item["price"] * item["quantity"]})

print("Items with totals:")
for item in with_totals:
    print(f"  {item['name']}: ${item['total']:.2f}")

# Calculate grand total
grand_total = with_totals.reduce(lambda acc, item: acc + item["total"], 0)
print(f"\nGrand total: ${grand_total:.2f}")

# Find expensive items (> $3)
expensive = cart.filter(lambda item: item["price"] * item["quantity"] > 3)
print("\nExpensive items (total > $3):")
for item in expensive:
    print(f"  {item['name']}: ${item['price'] * item['quantity']:.2f}")

# =============================================================================
# REAL WORLD EXAMPLE: Data pipeline
# =============================================================================

print("\n17. REAL WORLD: Data transformation pipeline")
print("-" * 80)

# Raw data
data = ImmutableList.of(
    {"name": "alice", "score": 85, "active": True},
    {"name": "bob", "score": 92, "active": False},
    {"name": "charlie", "score": 78, "active": True},
    {"name": "david", "score": 95, "active": True},
    {"name": "eve", "score": 88, "active": False},
)

# Process: filter active, normalize names, add grade
result = (
    data.filter(lambda user: user["active"])  # Only active users
    .map(
        lambda user: {
            **user,
            "name": user["name"].upper(),  # Uppercase names
        }
    )
    .map(
        lambda user: {
            **user,
            "grade": "A" if user["score"] >= 90 else "B" if user["score"] >= 80 else "C",
        }
    )
    .sort(key=lambda user: user["score"], reverse=True)  # Sort by score
)

print("Processed data:")
for user in result:
    print(f"  {user['name']}: {user['score']} ({user['grade']})")

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================

print("\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)
print(
    """
1. ImmutableList NEVER changes - operations return NEW lists
2. Thread-safe by design
3. Easy to reason about (no hidden mutations)
4. map() - transform each element
5. filter() - keep matching elements
6. reduce() - combine all elements
7. flat_map() - map then flatten
8. Chain operations naturally
9. append() and prepend() return new lists
10. take() and drop() for slicing
11. reverse() and sort() return new lists
12. Original list always stays the same!
"""
)
