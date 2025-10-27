"""
Banking Transaction Processing: OOP vs Functional Programming

This example demonstrates a real-world scenario where functional programming
excels: processing a series of banking transactions with validation, error
handling, and state transformations.

Problem: Process user transactions (deposits, withdrawals, transfers) with:
- Validation at each step
- Error accumulation (don't stop at first error)
- Audit trail generation
- Balance calculations
- Transaction history

This is where OOP typically creates:
- Deep inheritance hierarchies
- Mutable shared state
- Complex error handling chains
- Tightly coupled components
- Difficult to test and reason about

Functional programming provides:
- Pure functions
- Immutable data
- Composable operations
- Declarative error handling
- Easy to test and understand
"""

import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime
from enum import Enum

try:
    from pygraham import (
        Either,
        Left,
        Right,
        Maybe,
        Just,
        Nothing,
        ImmutableList,
        ImmutableDict,
        pipe,
        curry,
    )

    HAS_PYGRAHAM = True
except ImportError:
    HAS_PYGRAHAM = False


# =============================================================================
# BEFORE: Object-Oriented Approach
# =============================================================================


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"


class BankAccount:
    """Traditional OOP approach with mutable state."""

    def __init__(self, account_id: str, balance: Decimal):
        self.account_id = account_id
        self.balance = balance
        self.transaction_history: List[Dict] = []
        self.errors: List[str] = []
        self.is_locked = False

    def deposit(self, amount: Decimal, description: str) -> bool:
        """Deposit money. Returns True if successful."""
        if self.is_locked:
            self.errors.append(f"Account {self.account_id} is locked")
            return False

        if amount <= 0:
            self.errors.append(f"Invalid deposit amount: {amount}")
            return False

        # Mutable state change!
        self.balance += amount
        self.transaction_history.append(
            {
                "type": TransactionType.DEPOSIT,
                "amount": amount,
                "description": description,
                "timestamp": datetime.now(),
                "balance_after": self.balance,
            }
        )
        return True

    def withdraw(self, amount: Decimal, description: str) -> bool:
        """Withdraw money. Returns True if successful."""
        if self.is_locked:
            self.errors.append(f"Account {self.account_id} is locked")
            return False

        if amount <= 0:
            self.errors.append(f"Invalid withdrawal amount: {amount}")
            return False

        if self.balance < amount:
            self.errors.append(
                f"Insufficient funds. Balance: {self.balance}, Requested: {amount}"
            )
            return False

        # Mutable state change!
        self.balance -= amount
        self.transaction_history.append(
            {
                "type": TransactionType.WITHDRAWAL,
                "amount": amount,
                "description": description,
                "timestamp": datetime.now(),
                "balance_after": self.balance,
            }
        )
        return True

    def get_balance(self) -> Decimal:
        return self.balance

    def get_errors(self) -> List[str]:
        return self.errors

    def lock_account(self):
        self.is_locked = True

    def unlock_account(self):
        self.is_locked = False


class TransactionProcessor:
    """OOP approach to process multiple transactions."""

    def __init__(self):
        self.accounts: Dict[str, BankAccount] = {}

    def create_account(self, account_id: str, initial_balance: Decimal):
        self.accounts[account_id] = BankAccount(account_id, initial_balance)

    def process_transaction(
        self, account_id: str, transaction_type: str, amount: Decimal, description: str
    ) -> Tuple[bool, Optional[str]]:
        """Process a single transaction."""
        if account_id not in self.accounts:
            return False, f"Account {account_id} not found"

        account = self.accounts[account_id]

        if transaction_type == "deposit":
            success = account.deposit(amount, description)
        elif transaction_type == "withdrawal":
            success = account.withdraw(amount, description)
        else:
            return False, f"Unknown transaction type: {transaction_type}"

        if not success:
            return False, account.get_errors()[-1] if account.errors else "Unknown error"

        return True, None

    def process_batch(self, transactions: List[Dict]) -> Dict:
        """Process multiple transactions."""
        successful = 0
        failed = 0
        errors = []

        for txn in transactions:
            account_id = txn.get("account_id")
            txn_type = txn.get("type")
            amount = txn.get("amount")
            description = txn.get("description", "")

            success, error = self.process_transaction(account_id, txn_type, amount, description)

            if success:
                successful += 1
            else:
                failed += 1
                errors.append({"transaction": txn, "error": error})

        return {
            "successful": successful,
            "failed": failed,
            "errors": errors,
            "accounts": {
                acc_id: {"balance": acc.get_balance(), "errors": acc.get_errors()}
                for acc_id, acc in self.accounts.items()
            },
        }


# =============================================================================
# AFTER: Functional Programming Approach with PyGraham
# =============================================================================

if HAS_PYGRAHAM:

    @dataclass(frozen=True)  # Immutable!
    class Account:
        """Immutable account representation."""

        account_id: str
        balance: Decimal
        transaction_history: ImmutableList = field(default_factory=lambda: ImmutableList())
        is_locked: bool = False

    @dataclass(frozen=True)
    class Transaction:
        """Immutable transaction representation."""

        account_id: str
        type: str
        amount: Decimal
        description: str
        timestamp: datetime = field(default_factory=datetime.now)

    @dataclass(frozen=True)
    class TransactionResult:
        """Immutable result of a transaction."""

        account: Account
        transaction: Transaction
        balance_after: Decimal

    # Pure functions - no side effects!

    def validate_amount(amount: Decimal) -> Either:
        """Validate transaction amount."""
        if amount <= 0:
            return Left(f"Invalid amount: {amount}")
        return Right(amount)

    def validate_account_unlocked(account: Account) -> Either:
        """Validate account is not locked."""
        if account.is_locked:
            return Left(f"Account {account.account_id} is locked")
        return Right(account)

    def validate_sufficient_funds(account: Account, amount: Decimal) -> Either:
        """Validate sufficient funds for withdrawal."""
        if account.balance < amount:
            return Left(
                f"Insufficient funds. Balance: {account.balance}, Requested: {amount}"
            )
        return Right((account, amount))

    @curry
    def apply_deposit(transaction: Transaction, account: Account) -> Either:
        """Apply a deposit transaction."""
        return (
            validate_account_unlocked(account)
            .flat_map(lambda acc: validate_amount(transaction.amount).map(lambda _: acc))
            .map(
                lambda acc: Account(
                    account_id=acc.account_id,
                    balance=acc.balance + transaction.amount,
                    transaction_history=acc.transaction_history.append(
                        ImmutableDict.of(
                            type=transaction.type,
                            amount=transaction.amount,
                            description=transaction.description,
                            timestamp=transaction.timestamp,
                            balance_after=acc.balance + transaction.amount,
                        )
                    ),
                    is_locked=acc.is_locked,
                )
            )
        )

    @curry
    def apply_withdrawal(transaction: Transaction, account: Account) -> Either:
        """Apply a withdrawal transaction."""
        return (
            validate_account_unlocked(account)
            .flat_map(lambda acc: validate_amount(transaction.amount).map(lambda _: acc))
            .flat_map(lambda acc: validate_sufficient_funds(acc, transaction.amount))
            .map(
                lambda result: Account(
                    account_id=result[0].account_id,
                    balance=result[0].balance - transaction.amount,
                    transaction_history=result[0].transaction_history.append(
                        ImmutableDict.of(
                            type=transaction.type,
                            amount=transaction.amount,
                            description=transaction.description,
                            timestamp=transaction.timestamp,
                            balance_after=result[0].balance - transaction.amount,
                        )
                    ),
                    is_locked=result[0].is_locked,
                )
            )
        )

    def apply_transaction(transaction: Transaction, account: Account) -> Either:
        """Apply any transaction type."""
        if transaction.type == "deposit":
            return apply_deposit(transaction, account)
        elif transaction.type == "withdrawal":
            return apply_withdrawal(transaction, account)
        else:
            return Left(f"Unknown transaction type: {transaction.type}")

    def process_transaction_fp(
        accounts: ImmutableDict, transaction: Transaction
    ) -> Either:
        """Process a single transaction functionally."""
        return (
            Maybe.of(accounts.get_or_else(transaction.account_id, None))
            .or_else(Just(Account(transaction.account_id, Decimal("0"))))
            .flat_map(
                lambda account: apply_transaction(transaction, account)
                .map(lambda updated_account: (transaction.account_id, updated_account))
                .fold(
                    lambda error: Just(Left({"transaction": transaction, "error": error})),
                    lambda result: Just(
                        Right(accounts.set(result[0], result[1]))
                    ),
                )
            )
            .get()
        )

    def process_batch_fp(
        initial_accounts: ImmutableDict, transactions: ImmutableList
    ) -> ImmutableDict:
        """Process batch of transactions functionally."""

        def fold_transaction(state, transaction):
            """Fold function to accumulate results."""
            accounts = state.get_or_else("accounts", ImmutableDict())
            successes = state.get_or_else("successes", ImmutableList())
            failures = state.get_or_else("failures", ImmutableList())

            result = process_transaction_fp(accounts, transaction)

            return result.fold(
                lambda error: ImmutableDict.of(
                    accounts=accounts, successes=successes, failures=failures.append(error)
                ),
                lambda new_accounts: ImmutableDict.of(
                    accounts=new_accounts,
                    successes=successes.append(transaction),
                    failures=failures,
                ),
            )

        initial_state = ImmutableDict.of(
            accounts=initial_accounts,
            successes=ImmutableList(),
            failures=ImmutableList(),
        )

        return transactions.reduce(fold_transaction, initial_state)


# =============================================================================
# BENCHMARK AND COMPARISON
# =============================================================================


def generate_test_transactions(count: int) -> List[Dict]:
    """Generate test transaction data."""
    transactions = []
    for i in range(count):
        if i % 3 == 0:
            transactions.append(
                {
                    "account_id": f"ACC{i % 10:03d}",
                    "type": "deposit",
                    "amount": Decimal(str(100 + i * 10)),
                    "description": f"Deposit {i}",
                }
            )
        elif i % 3 == 1:
            transactions.append(
                {
                    "account_id": f"ACC{i % 10:03d}",
                    "type": "withdrawal",
                    "amount": Decimal(str(50 + i * 5)),
                    "description": f"Withdrawal {i}",
                }
            )
        else:
            transactions.append(
                {
                    "account_id": f"ACC{i % 10:03d}",
                    "type": "deposit",
                    "amount": Decimal(str(200 + i * 15)),
                    "description": f"Deposit {i}",
                }
            )
    return transactions


def benchmark_oop_approach(transactions: List[Dict], num_runs: int = 100):
    """Benchmark OOP approach."""
    times = []

    for _ in range(num_runs):
        processor = TransactionProcessor()

        # Create accounts
        for i in range(10):
            processor.create_account(f"ACC{i:03d}", Decimal("1000"))

        start = time.time()
        result = processor.process_batch(transactions)
        elapsed = time.time() - start
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    return avg_time, result


def benchmark_fp_approach(transactions: List[Dict], num_runs: int = 100):
    """Benchmark FP approach."""
    times = []

    for _ in range(num_runs):
        # Create initial accounts
        accounts = ImmutableDict(
            {f"ACC{i:03d}": Account(f"ACC{i:03d}", Decimal("1000")) for i in range(10)}
        )

        # Convert transactions to immutable
        txns = ImmutableList(
            [
                Transaction(
                    account_id=t["account_id"],
                    type=t["type"],
                    amount=t["amount"],
                    description=t["description"],
                )
                for t in transactions
            ]
        )

        start = time.time()
        result = process_batch_fp(accounts, txns)
        elapsed = time.time() - start
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    return avg_time, result


def demonstrate_code_complexity():
    """Demonstrate code complexity differences."""
    print(f"\n{'='*80}")
    print("CODE COMPLEXITY COMPARISON")
    print(f"{'='*80}\n")

    print("OBJECT-ORIENTED APPROACH:")
    print("-" * 80)
    print(
        """
Problems:
1. MUTABLE STATE: balance and transaction_history change in place
   - Hard to track state changes
   - Race conditions in concurrent scenarios
   - Difficult to undo operations

2. ERROR HANDLING: Mixed boolean returns and error lists
   - Inconsistent error reporting
   - Errors accumulate in mutable list
   - Hard to compose operations

3. TIGHT COUPLING: Processor tightly coupled to Account class
   - Hard to test in isolation
   - Changes to Account affect Processor
   - Complex inheritance hierarchies emerge

4. IMPLICIT DEPENDENCIES: Methods depend on object state
   - Hidden preconditions (is_locked)
   - Order of operations matters
   - Side effects everywhere

Example of problems:
    account = BankAccount("ACC001", Decimal("1000"))
    account.withdraw(Decimal("500"), "Purchase")  # Success
    # Later...
    account.lock_account()  # Mutates state!
    account.withdraw(Decimal("200"), "Purchase")  # Now fails!
    # Hard to reason about what happened
    """
    )

    if HAS_PYGRAHAM:
        print("\nFUNCTIONAL APPROACH:")
        print("-" * 80)
        print(
            """
Advantages:
1. IMMUTABLE STATE: Account never changes
   - Clear state transitions
   - Thread-safe by default
   - Easy to undo (just use old version)

2. EXPLICIT ERROR HANDLING: Either monad makes errors explicit
   - Type system tracks possible failures
   - Errors flow through composition
   - Easy to compose operations

3. LOOSE COUPLING: Functions work on data
   - Each function is independent
   - Easy to test (just input → output)
   - No hidden state

4. PURE FUNCTIONS: No side effects
   - Same input → same output always
   - Easy to reason about
   - Composable and reusable

Example of clarity:
    account = Account("ACC001", Decimal("1000"))
    result = apply_withdrawal(transaction, account)
    # result is Either[Error, NewAccount]
    # Original account unchanged!
    # Clear success or failure
    # Can compose with other operations
    """
        )


def run_benchmarks():
    """Run all benchmarks."""
    print(f"\n{'='*80}")
    print("BANKING TRANSACTION PROCESSING BENCHMARK")
    print(f"{'='*80}\n")

    # Generate test data
    transactions = generate_test_transactions(100)
    print(f"Processing {len(transactions)} transactions across 10 accounts\n")

    # Benchmark OOP
    print("Object-Oriented Approach:")
    oop_time, oop_result = benchmark_oop_approach(transactions, num_runs=50)
    print(f"  Average time: {oop_time*1000:.3f}ms")
    print(f"  Successful: {oop_result['successful']}")
    print(f"  Failed: {oop_result['failed']}")
    print(f"  Errors: {len(oop_result['errors'])}")

    if HAS_PYGRAHAM:
        print("\nFunctional Programming Approach:")
        fp_time, fp_result = benchmark_fp_approach(transactions, num_runs=50)
        print(f"  Average time: {fp_time*1000:.3f}ms")
        print(f"  Successful: {len(fp_result['successes'])}")
        print(f"  Failed: {len(fp_result['failures'])}")

        speedup = oop_time / fp_time
        print(f"\n  Speedup: {speedup:.2f}x {'faster' if speedup > 1 else 'slower'}")

    # Demonstrate complexity
    demonstrate_code_complexity()

    print(f"\n{'='*80}")
    print("KEY TAKEAWAYS")
    print(f"{'='*80}")
    print(
        """
1. TESTABILITY: FP functions are trivial to test (no mocks needed)
2. CONCURRENCY: FP is thread-safe by default (immutable data)
3. DEBUGGING: FP makes it easy to reproduce bugs (pure functions)
4. REFACTORING: FP changes are local (no ripple effects)
5. REASONING: FP code reads like math (declarative vs imperative)
6. PERFORMANCE: FP can be faster (no defensive copying)
7. COMPOSITION: FP operations compose naturally (monads!)
    """
    )


if __name__ == "__main__":
    run_benchmarks()
