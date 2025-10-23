"""
Data Processing Pipeline: Before and After PyGraham

Demonstrates building complex data processing pipelines with PyGraham.
"""

import time
import random
from typing import List, Dict, Optional

try:
    from pygraham import (
        Maybe,
        Either,
        Left,
        Right,
        pipe,
        compose,
        ImmutableList,
        LazySequence,
        match,
        case,
        _,
    )

    HAS_PYGRAHAM = True
except ImportError:
    HAS_PYGRAHAM = False

# Sample data: user transactions
TRANSACTIONS = [
    {"id": 1, "user": "alice", "amount": 100.50, "status": "completed"},
    {"id": 2, "user": "bob", "amount": None, "status": "completed"},
    {"id": 3, "user": "charlie", "amount": 250.75, "status": "pending"},
    {"id": 4, "user": "alice", "amount": 50.25, "status": "completed"},
    {"id": 5, "user": "bob", "amount": 300.00, "status": "failed"},
    {"id": 6, "user": "dave", "amount": 175.80, "status": "completed"},
    {"id": 7, "user": "charlie", "amount": 80.50, "status": "completed"},
    {"id": 8, "user": "alice", "amount": None, "status": "completed"},
]


# ============================================================================
# BEFORE: Vanilla Python (Imperative)
# ============================================================================


def process_transactions_vanilla(transactions: List[Dict]) -> Dict[str, float]:
    """
    Process transactions: filter completed, handle None amounts, sum by user.
    Vanilla Python with explicit error handling.
    """
    result = {}

    for tx in transactions:
        # Check status
        if tx.get("status") != "completed":
            continue

        # Get amount with null check
        amount = tx.get("amount")
        if amount is None:
            continue

        # Validate amount
        if amount < 0:
            continue

        # Get user
        user = tx.get("user")
        if not user:
            continue

        # Add to result
        if user in result:
            result[user] += amount
        else:
            result[user] = amount

    return result


def complex_pipeline_vanilla(transactions: List[Dict], min_amount: float) -> List[Dict]:
    """
    Complex pipeline: filter, transform, validate, sort.
    """
    results = []

    for tx in transactions:
        # Filter by status
        if tx.get("status") != "completed":
            continue

        # Get and validate amount
        amount = tx.get("amount")
        if amount is None or amount < min_amount:
            continue

        # Get user
        user = tx.get("user")
        if not user:
            continue

        # Apply tax (20%)
        taxed_amount = amount * 0.8

        # Create result
        result = {
            "user": user,
            "original": amount,
            "after_tax": taxed_amount,
            "savings": amount - taxed_amount,
        }
        results.append(result)

    # Sort by after_tax amount descending
    results.sort(key=lambda x: x["after_tax"], reverse=True)

    return results


# ============================================================================
# AFTER: PyGraham (Functional)
# ============================================================================

if HAS_PYGRAHAM:

    def safe_get(d: Dict, key: str) -> Maybe:
        """Safely get a value from dict, wrapping in Maybe."""
        return Maybe.of(d.get(key))

    def validate_positive(x: float) -> Either:
        """Validate that a number is positive."""
        if x < 0:
            return Left(f"Negative value: {x}")
        return Right(x)

    def process_transaction_fp(tx: Dict) -> Maybe:
        """
        Process a single transaction using Maybe monad for clean error handling.
        """
        return (
            safe_get(tx, "status")
            .filter(lambda s: s == "completed")
            .flat_map(lambda _: safe_get(tx, "amount"))
            .filter(lambda a: a > 0)
            .flat_map(lambda amount: safe_get(tx, "user").map(lambda user: (user, amount)))
        )

    def process_transactions_fp(transactions: ImmutableList) -> Dict[str, float]:
        """
        Process transactions using functional composition.
        Much cleaner than vanilla Python!
        """
        return (
            transactions.map(process_transaction_fp)
            .filter(lambda m: m.is_just())
            .map(lambda m: m.get())
            .reduce(lambda acc, item: {**acc, item[0]: acc.get(item[0], 0) + item[1]}, {})
        )

    def apply_tax(amount: float) -> float:
        """Apply 20% tax."""
        return amount * 0.8

    def create_result(user: str, amount: float) -> Dict:
        """Create result dictionary."""
        after_tax = apply_tax(amount)
        return {
            "user": user,
            "original": amount,
            "after_tax": after_tax,
            "savings": amount - after_tax,
        }

    def complex_pipeline_fp(transactions: ImmutableList, min_amount: float) -> ImmutableList:
        """
        Complex pipeline using functional composition.
        Notice how readable and composable this is!
        """
        process_tx = pipe(
            lambda tx: process_transaction_fp(tx),
            lambda maybe: maybe.filter(lambda item: item[1] >= min_amount),
            lambda maybe: maybe.map(lambda item: create_result(item[0], item[1])),
        )

        return (
            transactions.map(process_tx)
            .filter(lambda m: m.is_just())
            .map(lambda m: m.get())
            .sort(key=lambda x: x["after_tax"], reverse=True)
        )


# ============================================================================
# PATTERN MATCHING EXAMPLE
# ============================================================================

if HAS_PYGRAHAM:

    def categorize_transaction(tx: Dict) -> str:
        """
        Categorize transaction using pattern matching.
        Much cleaner than if-elif-else chains!
        """
        amount = tx.get("amount", 0)
        status = tx.get("status", "unknown")

        return match(
            status,
            case(
                "completed",
                lambda _: match(
                    amount,
                    case(lambda a: a < 50, lambda _: "small"),
                    case(lambda a: 50 <= a < 200, lambda _: "medium"),
                    case(lambda a: a >= 200, lambda _: "large"),
                    case(_, lambda _: "invalid"),
                ),
            ),
            case("pending", lambda _: "awaiting"),
            case("failed", lambda _: "error"),
            case(_, lambda _: "unknown"),
        )


# ============================================================================
# ERROR HANDLING WITH EITHER
# ============================================================================

if HAS_PYGRAHAM:

    def divide_safe(a: float, b: float) -> Either:
        """Safe division using Either monad."""
        if b == 0:
            return Left("Division by zero")
        return Right(a / b)

    def calculate_average_transaction(user: str, transactions: ImmutableList) -> Either:
        """
        Calculate average transaction amount for a user.
        Uses Either for clean error handling.
        """
        user_txs = (
            transactions.filter(lambda tx: tx.get("user") == user)
            .map(lambda tx: tx.get("amount"))
            .filter(lambda a: a is not None)
        )

        if user_txs.is_empty():
            return Left(f"No transactions for user: {user}")

        total = user_txs.reduce(lambda acc, x: acc + x, 0.0)
        return divide_safe(total, len(user_txs))


# ============================================================================
# LAZY EVALUATION FOR BIG DATA
# ============================================================================

if HAS_PYGRAHAM:

    def process_large_dataset_fp(transactions: LazySequence) -> ImmutableList:
        """
        Process large dataset with lazy evaluation.
        Only computes what's needed!
        """
        return (
            transactions.filter(lambda tx: tx.get("status") == "completed")
            .map(lambda tx: (tx.get("user"), tx.get("amount")))
            .filter(lambda item: item[1] is not None and item[1] > 100)
            .take(10)  # Only take first 10, rest never computed!
            .to_list()
        )


# ============================================================================
# BENCHMARKS
# ============================================================================


def benchmark_processing():
    """Benchmark both implementations."""
    print(f"\n{'='*70}")
    print("DATA PROCESSING PIPELINE BENCHMARK")
    print(f"{'='*70}\n")

    num_runs = 10000

    # Vanilla Python
    print("VANILLA PYTHON:")
    start_time = time.time()
    for _ in range(num_runs):
        result_vanilla = process_transactions_vanilla(TRANSACTIONS)
    vanilla_time = (time.time() - start_time) / num_runs

    print(f"  Time: {vanilla_time*1000:.4f}ms")
    print(f"  Result: {result_vanilla}")

    if HAS_PYGRAHAM:
        # PyGraham
        print("\nPYGRAHAM:")
        transactions_immutable = ImmutableList(TRANSACTIONS)
        start_time = time.time()
        for _ in range(num_runs):
            result_fp = process_transactions_fp(transactions_immutable)
        fp_time = (time.time() - start_time) / num_runs

        print(f"  Time: {fp_time*1000:.4f}ms")
        print(f"  Result: {result_fp}")

        speedup = vanilla_time / fp_time
        print(f"\n  Speedup: {speedup:.2f}x {'faster' if speedup > 1 else 'slower'}")

    # Complex pipeline
    print("\n" + "-" * 70)
    print("COMPLEX PIPELINE:")

    min_amount = 50.0
    num_runs = 5000

    print("\nVANILLA PYTHON:")
    start_time = time.time()
    for _ in range(num_runs):
        result_vanilla = complex_pipeline_vanilla(TRANSACTIONS, min_amount)
    vanilla_time = (time.time() - start_time) / num_runs

    print(f"  Time: {vanilla_time*1000:.4f}ms")
    print(f"  Results: {len(result_vanilla)} transactions")

    if HAS_PYGRAHAM:
        print("\nPYGRAHAM:")
        start_time = time.time()
        for _ in range(num_runs):
            result_fp = complex_pipeline_fp(transactions_immutable, min_amount)
        fp_time = (time.time() - start_time) / num_runs

        print(f"  Time: {fp_time*1000:.4f}ms")
        print(f"  Results: {len(result_fp)} transactions")

        speedup = vanilla_time / fp_time
        print(f"\n  Speedup: {speedup:.2f}x {'faster' if speedup > 1 else 'slower'}")


def demonstrate_features():
    """Demonstrate PyGraham features."""
    if not HAS_PYGRAHAM:
        print("\nPyGraham not installed. Install with: pip install pygraham")
        return

    print(f"\n{'='*70}")
    print("PYGRAHAM FEATURES DEMONSTRATION")
    print(f"{'='*70}\n")

    # Pattern matching
    print("PATTERN MATCHING:")
    for tx in TRANSACTIONS[:4]:
        category = categorize_transaction(tx)
        print(f"  Transaction {tx['id']}: {category}")

    # Either monad for error handling
    print("\nEITHER MONAD (Error Handling):")
    transactions_immutable = ImmutableList(TRANSACTIONS)
    result = calculate_average_transaction("alice", transactions_immutable)
    print(f"  Alice's average: {result.fold(lambda l: f'Error: {l}', lambda r: f'${r:.2f}')}")

    result = calculate_average_transaction("unknown", transactions_immutable)
    print(f"  Unknown user: {result.fold(lambda l: f'Error: {l}', lambda r: f'${r:.2f}')}")

    # Lazy evaluation
    print("\nLAZY EVALUATION:")
    print("  Processing 1,000,000 transactions but only taking first 10...")
    large_dataset = LazySequence.from_iterable(TRANSACTIONS * 125000)  # Simulate 1M transactions
    start_time = time.time()
    result = process_large_dataset_fp(large_dataset)
    elapsed = (time.time() - start_time) * 1000
    print(f"  Time: {elapsed:.2f}ms (thanks to lazy evaluation!)")
    print(f"  Results: {len(result)} transactions")


if __name__ == "__main__":
    benchmark_processing()
    demonstrate_features()
    print(f"\n{'='*70}\n")
