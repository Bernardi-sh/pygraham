"""
File System Tree Traversal: OOP vs Functional Recursion

This example demonstrates a classic problem where functional recursion
shines: traversing and processing hierarchical data structures.

Problem: Process a file system tree to:
- Calculate total size of directories
- Find all files matching patterns
- Generate reports with indentation
- Filter and transform the tree structure
- Handle nested structures elegantly

This is where OOP typically creates:
- Complex visitor patterns
- Mutable accumulators
- Deep class hierarchies
- State management issues
- Hard to compose operations

Functional recursion provides:
- Elegant recursive solutions
- Immutable data structures
- Composable operations
- Pattern matching
- Natural fit for tree structures
"""

import os
import time
from typing import List, Dict, Optional, Tuple, Callable, Any
from dataclasses import dataclass, field
from pathlib import Path
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
        match,
        case,
        _,
    )

    HAS_PYGRAHAM = True
except ImportError:
    HAS_PYGRAHAM = False


# =============================================================================
# BEFORE: Object-Oriented Approach
# =============================================================================


class FileSystemNode:
    """Base class for file system nodes."""

    def __init__(self, name: str, size: int = 0):
        self.name = name
        self.size = size

    def get_size(self) -> int:
        """Get size of this node."""
        raise NotImplementedError

    def find_files(self, pattern: str) -> List[str]:
        """Find files matching pattern."""
        raise NotImplementedError

    def get_report(self, indent: int = 0) -> str:
        """Generate indented report."""
        raise NotImplementedError

    def apply_visitor(self, visitor: "Visitor") -> None:
        """Apply visitor pattern."""
        raise NotImplementedError


class File(FileSystemNode):
    """Represents a file."""

    def __init__(self, name: str, size: int):
        super().__init__(name, size)

    def get_size(self) -> int:
        return self.size

    def find_files(self, pattern: str) -> List[str]:
        if pattern in self.name:
            return [self.name]
        return []

    def get_report(self, indent: int = 0) -> str:
        return "  " * indent + f"- {self.name} ({self.size} bytes)\n"

    def apply_visitor(self, visitor: "Visitor") -> None:
        visitor.visit_file(self)


class Directory(FileSystemNode):
    """Represents a directory with children."""

    def __init__(self, name: str):
        super().__init__(name, 0)
        self.children: List[FileSystemNode] = []

    def add_child(self, child: FileSystemNode) -> None:
        """Add child node (mutates state!)."""
        self.children.append(child)

    def get_size(self) -> int:
        """Recursively calculate total size."""
        total = 0
        for child in self.children:
            total += child.get_size()
        return total

    def find_files(self, pattern: str) -> List[str]:
        """Recursively find files."""
        results = []
        for child in self.children:
            results.extend(child.find_files(pattern))
        return results

    def get_report(self, indent: int = 0) -> str:
        """Generate indented report."""
        report = "  " * indent + f"+ {self.name}/\n"
        for child in self.children:
            report += child.get_report(indent + 1)
        return report

    def apply_visitor(self, visitor: "Visitor") -> None:
        visitor.visit_directory_enter(self)
        for child in self.children:
            child.apply_visitor(visitor)
        visitor.visit_directory_exit(self)


class Visitor:
    """Visitor pattern for traversing tree."""

    def visit_file(self, file: File) -> None:
        pass

    def visit_directory_enter(self, directory: Directory) -> None:
        pass

    def visit_directory_exit(self, directory: Directory) -> None:
        pass


class SizeCalculatorVisitor(Visitor):
    """Visitor to calculate total size."""

    def __init__(self):
        self.total_size = 0

    def visit_file(self, file: File) -> None:
        self.total_size += file.size


class FileFinderVisitor(Visitor):
    """Visitor to find files matching pattern."""

    def __init__(self, pattern: str):
        self.pattern = pattern
        self.found_files: List[str] = []

    def visit_file(self, file: File) -> None:
        if self.pattern in file.name:
            self.found_files.append(file.name)


class TreeProcessor:
    """OOP approach to process file system trees."""

    def __init__(self, root: Directory):
        self.root = root

    def calculate_total_size(self) -> int:
        """Calculate total size using visitor pattern."""
        visitor = SizeCalculatorVisitor()
        self.root.apply_visitor(visitor)
        return visitor.total_size

    def find_files(self, pattern: str) -> List[str]:
        """Find files using visitor pattern."""
        visitor = FileFinderVisitor(pattern)
        self.root.apply_visitor(visitor)
        return visitor.found_files

    def get_report(self) -> str:
        """Generate tree report."""
        return self.root.get_report()

    def filter_large_files(self, min_size: int) -> Directory:
        """Filter files larger than min_size (complex!)."""
        return self._filter_recursive(self.root, min_size)

    def _filter_recursive(self, node: FileSystemNode, min_size: int) -> Optional[FileSystemNode]:
        """Recursive helper for filtering."""
        if isinstance(node, File):
            if node.size >= min_size:
                return File(node.name, node.size)
            return None
        elif isinstance(node, Directory):
            new_dir = Directory(node.name)
            for child in node.children:
                filtered_child = self._filter_recursive(child, min_size)
                if filtered_child:
                    new_dir.add_child(filtered_child)
            return new_dir if new_dir.children else None
        return None


# =============================================================================
# AFTER: Functional Recursive Approach with PyGraham
# =============================================================================

if HAS_PYGRAHAM:

    @dataclass(frozen=True)
    class FNode:
        """Immutable file system node (discriminated union)."""

        name: str
        type: str  # "file" or "directory"
        size: int = 0
        children: ImmutableList = field(default_factory=lambda: ImmutableList())

    # Pure factory functions
    def file(name: str, size: int) -> FNode:
        """Create an immutable file node."""
        return FNode(name=name, type="file", size=size, children=ImmutableList())

    def directory(name: str, children: ImmutableList) -> FNode:
        """Create an immutable directory node."""
        return FNode(name=name, type="directory", size=0, children=children)

    # Pure recursive functions

    def get_size(node: FNode) -> int:
        """
        Calculate size recursively (pure function).

        Base case: file returns its size
        Recursive case: directory sums children sizes
        """
        return match(
            node.type,
            case("file", lambda _: node.size),
            case("directory", lambda _: node.children.map(get_size).reduce(lambda a, b: a + b, 0)),
        )

    def find_files(pattern: str, node: FNode) -> ImmutableList:
        """
        Find all files matching pattern (pure recursive function).

        Base case: file matches or doesn't
        Recursive case: directory searches all children and flattens results
        """

        def search(n: FNode) -> ImmutableList:
            return match(
                n.type,
                case(
                    "file",
                    lambda _: ImmutableList.of(n.name) if pattern in n.name else ImmutableList(),
                ),
                case(
                    "directory",
                    lambda _: n.children.flat_map(search),  # Recursive call + flatten
                ),
            )

        return search(node)

    def generate_report(node: FNode, indent: int = 0) -> str:
        """
        Generate indented report recursively (pure function).

        Base case: file generates one line
        Recursive case: directory generates header + recursively formatted children
        """
        prefix = "  " * indent

        return match(
            node.type,
            case("file", lambda _: f"{prefix}- {node.name} ({node.size} bytes)\n"),
            case(
                "directory",
                lambda _: f"{prefix}+ {node.name}/\n"
                + node.children.map(lambda child: generate_report(child, indent + 1))
                .reduce(lambda a, b: a + b, ""),
            ),
        )

    def filter_by_size(min_size: int, node: FNode) -> Maybe:
        """
        Filter tree by minimum file size (pure recursive function).

        Returns Maybe to handle case where entire subtree is filtered out.
        Base case: file passes or fails filter
        Recursive case: directory recursively filters children
        """

        def do_filter(n: FNode) -> Maybe:
            return match(
                n.type,
                case(
                    "file",
                    lambda _: Just(n) if n.size >= min_size else Nothing(),
                ),
                case(
                    "directory",
                    lambda _: (
                        n.children.map(do_filter)  # Recursively filter children
                        .filter(lambda m: not m.is_nothing())  # Keep only Just values
                        .map(lambda m: m.get())  # Extract values from Maybe
                        .pipe(
                            lambda filtered_children: (
                                Just(directory(n.name, filtered_children))
                                if len(filtered_children) > 0
                                else Nothing()
                            )
                        )
                    ),
                ),
            )

        return do_filter(node)

    def map_files(fn: Callable[[FNode], FNode], node: FNode) -> FNode:
        """
        Map function over all files in tree (pure recursive function).

        Transforms files while preserving tree structure.
        Base case: apply function to file
        Recursive case: recursively map over children
        """
        return match(
            node.type,
            case("file", lambda _: fn(node)),
            case(
                "directory",
                lambda _: directory(node.name, node.children.map(lambda child: map_files(fn, child))),
            ),
        )

    def fold_tree(file_fn: Callable[[FNode], Any], dir_fn: Callable[[FNode, ImmutableList], Any], node: FNode) -> Any:
        """
        Fold (catamorphism) over tree structure.

        This is the most general recursive pattern - all other operations
        can be implemented using fold_tree.

        Base case: apply file_fn to file
        Recursive case: recursively fold children, then apply dir_fn
        """
        return match(
            node.type,
            case("file", lambda _: file_fn(node)),
            case(
                "directory",
                lambda _: dir_fn(
                    node,
                    node.children.map(lambda child: fold_tree(file_fn, dir_fn, child)),
                ),
            ),
        )

    # Advanced operations using fold_tree

    def count_files(node: FNode) -> int:
        """Count total number of files using fold."""
        return fold_tree(
            file_fn=lambda _: 1,  # Each file counts as 1
            dir_fn=lambda _, children_counts: children_counts.reduce(lambda a, b: a + b, 0),
            node=node,
        )

    def max_depth(node: FNode) -> int:
        """Calculate maximum depth of tree using fold."""
        return fold_tree(
            file_fn=lambda _: 0,  # Files have depth 0
            dir_fn=lambda _, children_depths: (
                1 + children_depths.reduce(lambda a, b: max(a, b), 0)
                if len(children_depths) > 0
                else 0
            ),
            node=node,
        )

    def collect_stats(node: FNode) -> ImmutableDict:
        """Collect comprehensive statistics using fold."""
        return fold_tree(
            file_fn=lambda f: ImmutableDict.of(
                total_size=f.size,
                file_count=1,
                dir_count=0,
                max_file_size=f.size,
            ),
            dir_fn=lambda d, children_stats: children_stats.reduce(
                lambda acc, stats: ImmutableDict.of(
                    total_size=acc.get_or_else("total_size", 0) + stats.get_or_else("total_size", 0),
                    file_count=acc.get_or_else("file_count", 0) + stats.get_or_else("file_count", 0),
                    dir_count=acc.get_or_else("dir_count", 0) + stats.get_or_else("dir_count", 0) + 1,
                    max_file_size=max(
                        acc.get_or_else("max_file_size", 0),
                        stats.get_or_else("max_file_size", 0),
                    ),
                ),
                ImmutableDict.of(total_size=0, file_count=0, dir_count=0, max_file_size=0),
            ),
            node=node,
        )


# =============================================================================
# BENCHMARK AND COMPARISON
# =============================================================================


def create_test_tree_oop(depth: int, branching: int) -> Directory:
    """Create test tree using OOP approach."""

    def create_recursive(name: str, current_depth: int) -> FileSystemNode:
        if current_depth == 0:
            return File(f"file_{name}.txt", 1024 * (hash(name) % 10 + 1))

        dir_node = Directory(f"dir_{name}")
        for i in range(branching):
            child = create_recursive(f"{name}_{i}", current_depth - 1)
            dir_node.add_child(child)
        return dir_node

    return create_recursive("root", depth)


def create_test_tree_fp(depth: int, branching: int) -> "FNode":
    """Create test tree using FP approach."""

    def create_recursive(name: str, current_depth: int) -> "FNode":
        if current_depth == 0:
            return file(f"file_{name}.txt", 1024 * (hash(name) % 10 + 1))

        children = ImmutableList(
            [create_recursive(f"{name}_{i}", current_depth - 1) for i in range(branching)]
        )
        return directory(f"dir_{name}", children)

    return create_recursive("root", depth)


def benchmark_oop_operations(root: Directory, num_runs: int = 100):
    """Benchmark OOP operations."""
    processor = TreeProcessor(root)

    # Calculate size
    start = time.time()
    for _ in range(num_runs):
        total_size = processor.calculate_total_size()
    size_time = (time.time() - start) / num_runs

    # Find files
    start = time.time()
    for _ in range(num_runs):
        files = processor.find_files("file_root_0")
    find_time = (time.time() - start) / num_runs

    # Generate report
    start = time.time()
    for _ in range(num_runs):
        report = processor.get_report()
    report_time = (time.time() - start) / num_runs

    # Filter
    start = time.time()
    for _ in range(num_runs):
        filtered = processor.filter_large_files(5000)
    filter_time = (time.time() - start) / num_runs

    return {
        "size_time": size_time * 1000,
        "find_time": find_time * 1000,
        "report_time": report_time * 1000,
        "filter_time": filter_time * 1000,
        "total_size": total_size,
        "files_found": len(files),
    }


def benchmark_fp_operations(root: "FNode", num_runs: int = 100):
    """Benchmark FP operations."""

    # Calculate size
    start = time.time()
    for _ in range(num_runs):
        total_size = get_size(root)
    size_time = (time.time() - start) / num_runs

    # Find files
    start = time.time()
    for _ in range(num_runs):
        files = find_files("file_root_0", root)
    find_time = (time.time() - start) / num_runs

    # Generate report
    start = time.time()
    for _ in range(num_runs):
        report = generate_report(root)
    report_time = (time.time() - start) / num_runs

    # Filter
    start = time.time()
    for _ in range(num_runs):
        filtered = filter_by_size(5000, root)
    filter_time = (time.time() - start) / num_runs

    # Additional FP operations
    start = time.time()
    for _ in range(num_runs):
        count = count_files(root)
        depth = max_depth(root)
        stats = collect_stats(root)
    advanced_time = (time.time() - start) / num_runs

    return {
        "size_time": size_time * 1000,
        "find_time": find_time * 1000,
        "report_time": report_time * 1000,
        "filter_time": filter_time * 1000,
        "advanced_time": advanced_time * 1000,
        "total_size": total_size,
        "files_found": len(files),
        "file_count": count,
        "max_depth": depth,
        "stats": stats,
    }


def demonstrate_code_elegance():
    """Demonstrate code elegance differences."""
    print(f"\n{'='*80}")
    print("CODE ELEGANCE COMPARISON")
    print(f"{'='*80}\n")

    print("OBJECT-ORIENTED APPROACH:")
    print("-" * 80)
    print(
        """
Problems:
1. MUTABLE STATE: Tree structure mutates with add_child()
   - Hard to track changes
   - Concurrent access issues
   - Difficult to implement undo

2. VISITOR PATTERN: Need separate visitor classes for each operation
   - Boilerplate code
   - Tight coupling between nodes and visitors
   - Hard to compose operations

3. INHERITANCE HIERARCHY: Base class with multiple subclasses
   - Rigid structure
   - Changes to base affect all subclasses
   - Hard to add new node types

4. IMPERATIVE STYLE: Loops and mutations everywhere
   - Hard to reason about
   - Side effects hidden
   - Complex state management

Example complexity:
    class Directory(FileSystemNode):
        def __init__(self, name: str):
            self.children = []  # Mutable!

        def add_child(self, child):
            self.children.append(child)  # Side effect!

        def get_size(self):
            total = 0
            for child in self.children:  # Imperative loop
                total += child.get_size()
            return total
    """
    )

    if HAS_PYGRAHAM:
        print("\nFUNCTIONAL RECURSIVE APPROACH:")
        print("-" * 80)
        print(
            """
Advantages:
1. IMMUTABLE DATA: Tree never changes after creation
   - Thread-safe by default
   - Easy to implement undo (keep old versions)
   - Clear data flow

2. PURE FUNCTIONS: Each operation is a simple recursive function
   - No boilerplate
   - Easy to compose
   - Testable in isolation

3. DISCRIMINATED UNION: Single dataclass with type field
   - Flexible structure
   - Easy to add operations (just add functions)
   - Pattern matching for type safety

4. DECLARATIVE STYLE: Express WHAT, not HOW
   - Easy to understand
   - No hidden state
   - Composable operations

Example elegance:
    @dataclass(frozen=True)
    class FNode:
        name: str
        type: str
        size: int = 0
        children: ImmutableList = field(default_factory=lambda: ImmutableList())

    def get_size(node: FNode) -> int:
        return match(node.type,
            case("file", lambda _: node.size),
            case("directory", lambda _:
                node.children.map(get_size).reduce(lambda a, b: a + b, 0)))

RECURSION PATTERNS:
    • Simple recursion: get_size, find_files, generate_report
    • Recursive filtering: filter_by_size with Maybe monad
    • Recursive mapping: map_files preserves structure
    • Catamorphism (fold): fold_tree as universal recursion pattern

    All operations follow same pattern:
    1. Base case: handle leaf nodes (files)
    2. Recursive case: process children, combine results
    """
        )


def run_benchmarks():
    """Run all benchmarks."""
    print(f"\n{'='*80}")
    print("FILE SYSTEM TREE TRAVERSAL BENCHMARK")
    print(f"{'='*80}\n")

    depth = 4
    branching = 3
    total_nodes = sum(branching**i for i in range(depth + 1))
    print(f"Tree structure: depth={depth}, branching={branching}")
    print(f"Total nodes: {total_nodes}\n")

    # Create test trees
    oop_tree = create_test_tree_oop(depth, branching)

    print("Object-Oriented Approach:")
    oop_results = benchmark_oop_operations(oop_tree, num_runs=100)
    print(f"  Calculate size: {oop_results['size_time']:.3f}ms")
    print(f"  Find files:     {oop_results['find_time']:.3f}ms")
    print(f"  Generate report: {oop_results['report_time']:.3f}ms")
    print(f"  Filter tree:    {oop_results['filter_time']:.3f}ms")
    print(f"  Total size:     {oop_results['total_size']} bytes")
    print(f"  Files found:    {oop_results['files_found']}")

    if HAS_PYGRAHAM:
        fp_tree = create_test_tree_fp(depth, branching)

        print("\nFunctional Recursive Approach:")
        fp_results = benchmark_fp_operations(fp_tree, num_runs=100)
        print(f"  Calculate size: {fp_results['size_time']:.3f}ms")
        print(f"  Find files:     {fp_results['find_time']:.3f}ms")
        print(f"  Generate report: {fp_results['report_time']:.3f}ms")
        print(f"  Filter tree:    {fp_results['filter_time']:.3f}ms")
        print(f"  Advanced ops:   {fp_results['advanced_time']:.3f}ms")
        print(f"  Total size:     {fp_results['total_size']} bytes")
        print(f"  Files found:    {fp_results['files_found']}")
        print(f"  File count:     {fp_results['file_count']}")
        print(f"  Max depth:      {fp_results['max_depth']}")

        print("\nPerformance Comparison:")
        print("-" * 80)
        size_speedup = oop_results["size_time"] / fp_results["size_time"]
        find_speedup = oop_results["find_time"] / fp_results["find_time"]
        report_speedup = oop_results["report_time"] / fp_results["report_time"]
        filter_speedup = oop_results["filter_time"] / fp_results["filter_time"]

        print(f"  Size calculation: {size_speedup:.2f}x {'faster' if size_speedup > 1 else 'slower'}")
        print(f"  File finding:     {find_speedup:.2f}x {'faster' if find_speedup > 1 else 'slower'}")
        print(f"  Report generation: {report_speedup:.2f}x {'faster' if report_speedup > 1 else 'slower'}")
        print(f"  Tree filtering:   {filter_speedup:.2f}x {'faster' if filter_speedup > 1 else 'slower'}")

    demonstrate_code_elegance()

    print(f"\n{'='*80}")
    print("KEY TAKEAWAYS")
    print(f"{'='*80}")
    print(
        """
1. NATURAL FIT: Recursion naturally models hierarchical structures
2. ELEGANCE: Recursive functions are shorter and clearer than visitor pattern
3. COMPOSABILITY: Pure recursive functions compose naturally
4. PATTERN: fold_tree is universal recursion pattern (catamorphism)
5. IMMUTABILITY: Tree transformations create new trees, preserving old ones
6. TYPE SAFETY: Pattern matching ensures all cases handled
7. NO BOILERPLATE: No need for visitor classes, just functions
    """
    )


if __name__ == "__main__":
    run_benchmarks()
