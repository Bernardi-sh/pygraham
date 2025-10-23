"""
Travelling Salesman Problem: Before and After PyGraham

This example demonstrates the stylistic and performance advantages
of using PyGraham's functional programming features.
"""
import time
import random
from typing import List, Tuple
from itertools import permutations
import math

# Try to import PyGraham, fallback if not available
try:
    from pygraham import ImmutableList, pipe, curry, LazySequence
    HAS_PYGRAHAM = True
except ImportError:
    HAS_PYGRAHAM = False

# Sample cities as (x, y) coordinates
CITIES = [
    (0, 0),
    (1, 5),
    (5, 2),
    (7, 7),
    (8, 3),
    (4, 6),
    (3, 1),
    (6, 4),
]


def distance(city1: Tuple[float, float], city2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two cities."""
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)


# ============================================================================
# BEFORE: Vanilla Python (Imperative Style)
# ============================================================================

def calculate_route_distance_vanilla(cities: List[Tuple[float, float]],
                                     route: List[int]) -> float:
    """Calculate total distance of a route (vanilla Python)."""
    total = 0.0
    for i in range(len(route) - 1):
        total += distance(cities[route[i]], cities[route[i + 1]])
    # Return to start
    total += distance(cities[route[-1]], cities[route[0]])
    return total


def find_shortest_route_vanilla(cities: List[Tuple[float, float]]) -> Tuple[List[int], float]:
    """Find shortest route using brute force (vanilla Python)."""
    n = len(cities)
    indices = list(range(n))

    best_route = None
    best_distance = float('inf')

    # Generate all permutations
    for perm in permutations(indices):
        route = list(perm)
        dist = calculate_route_distance_vanilla(cities, route)
        if dist < best_distance:
            best_distance = dist
            best_route = route

    return best_route, best_distance


def tsp_with_filtering_vanilla(cities: List[Tuple[float, float]],
                               max_distance: float) -> List[Tuple[List[int], float]]:
    """Find all routes under a certain distance (vanilla Python)."""
    n = len(cities)
    indices = list(range(n))

    results = []
    for perm in permutations(indices):
        route = list(perm)
        dist = calculate_route_distance_vanilla(cities, route)
        if dist <= max_distance:
            results.append((route, dist))

    # Sort by distance
    results.sort(key=lambda x: x[1])
    return results


# ============================================================================
# AFTER: PyGraham (Functional Style)
# ============================================================================

if HAS_PYGRAHAM:
    @curry
    def calculate_route_distance_fp(cities: ImmutableList,
                                    route: ImmutableList) -> float:
        """Calculate total distance of a route (functional style)."""
        # Create pairs of consecutive cities
        pairs = list(zip(route, route.tail().append(route[0])))

        # Calculate distances and sum
        return (ImmutableList(pairs)
                .map(lambda pair: distance(cities[pair[0]], cities[pair[1]]))
                .reduce(lambda acc, d: acc + d, 0.0))


    def find_shortest_route_fp(cities: ImmutableList) -> Tuple[ImmutableList, float]:
        """Find shortest route using functional composition."""
        indices = ImmutableList(range(len(cities)))

        # Use lazy evaluation for efficiency
        result = (LazySequence.from_iterable(permutations(range(len(cities))))
                  .map(lambda perm: ImmutableList(perm))
                  .map(lambda route: (route, calculate_route_distance_fp(cities, route)))
                  .reduce(lambda best, current: current if current[1] < best[1] else best,
                          (None, float('inf'))))

        return result


    def tsp_with_filtering_fp(cities: ImmutableList,
                              max_distance: float) -> ImmutableList:
        """Find all routes under a certain distance (functional style)."""
        calc_distance = calculate_route_distance_fp(cities)

        return (LazySequence.from_iterable(permutations(range(len(cities))))
                .map(lambda perm: ImmutableList(perm))
                .map(lambda route: (route, calc_distance(route)))
                .filter(lambda item: item[1] <= max_distance)
                .to_list()
                )


# ============================================================================
# GREEDY NEAREST NEIGHBOR HEURISTIC
# ============================================================================

def nearest_neighbor_vanilla(cities: List[Tuple[float, float]],
                             start: int = 0) -> Tuple[List[int], float]:
    """Greedy nearest neighbor heuristic (vanilla)."""
    n = len(cities)
    unvisited = set(range(n))
    route = [start]
    unvisited.remove(start)
    total_distance = 0.0

    current = start
    while unvisited:
        nearest = min(unvisited, key=lambda city: distance(cities[current], cities[city]))
        total_distance += distance(cities[current], cities[nearest])
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    # Return to start
    total_distance += distance(cities[current], cities[start])
    return route, total_distance


if HAS_PYGRAHAM:
    def nearest_neighbor_fp(cities: ImmutableList, start: int = 0) -> Tuple[ImmutableList, float]:
        """Greedy nearest neighbor heuristic (functional)."""
        n = len(cities)

        def build_route(state):
            route, unvisited, current, total_dist = state

            if unvisited.is_empty():
                # Return to start
                final_dist = total_dist + distance(cities[current], cities[start])
                return route, final_dist

            # Find nearest unvisited city
            nearest = unvisited.reduce(
                lambda best, city: city if distance(cities[current], cities[city]) <
                                          distance(cities[current], cities[best]) else best,
                unvisited[0]
            )

            new_dist = total_dist + distance(cities[current], cities[nearest])

            return build_route((
                route.append(nearest),
                unvisited.filter(lambda c: c != nearest),
                nearest,
                new_dist
            ))

        initial_state = (
            ImmutableList.of(start),
            ImmutableList([i for i in range(n) if i != start]),
            start,
            0.0
        )

        return build_route(initial_state)


# ============================================================================
# BENCHMARKING
# ============================================================================

def benchmark_tsp(cities: List[Tuple[float, float]], num_runs: int = 5):
    """Benchmark both implementations."""
    print(f"\n{'='*70}")
    print(f"TSP Benchmark: {len(cities)} cities, {num_runs} runs")
    print(f"{'='*70}\n")

    # Vanilla Python
    print("VANILLA PYTHON (Imperative):")
    start_time = time.time()
    for _ in range(num_runs):
        route, dist = find_shortest_route_vanilla(cities)
    vanilla_time = (time.time() - start_time) / num_runs
    print(f"  Average time: {vanilla_time*1000:.2f}ms")
    print(f"  Best distance: {dist:.2f}")
    print(f"  Best route: {route}")

    if HAS_PYGRAHAM:
        # PyGraham
        print("\nPYGRAHAM (Functional):")
        cities_immutable = ImmutableList(cities)
        start_time = time.time()
        for _ in range(num_runs):
            route_fp, dist_fp = find_shortest_route_fp(cities_immutable)
        fp_time = (time.time() - start_time) / num_runs
        print(f"  Average time: {fp_time*1000:.2f}ms")
        print(f"  Best distance: {dist_fp:.2f}")
        print(f"  Best route: {list(route_fp)}")

        speedup = vanilla_time / fp_time
        print(f"\n  Speedup: {speedup:.2f}x {'faster' if speedup > 1 else 'slower'}")

    # Greedy heuristic comparison
    print("\n" + "-"*70)
    print("GREEDY NEAREST NEIGHBOR HEURISTIC:")

    start_time = time.time()
    for _ in range(num_runs * 100):  # More runs since it's faster
        route_greedy, dist_greedy = nearest_neighbor_vanilla(cities)
    greedy_vanilla_time = (time.time() - start_time) / (num_runs * 100)
    print(f"\n  Vanilla Python:")
    print(f"    Average time: {greedy_vanilla_time*1000:.4f}ms")
    print(f"    Distance: {dist_greedy:.2f}")
    print(f"    Route: {route_greedy}")

    if HAS_PYGRAHAM:
        start_time = time.time()
        for _ in range(num_runs * 100):
            route_greedy_fp, dist_greedy_fp = nearest_neighbor_fp(cities_immutable)
        greedy_fp_time = (time.time() - start_time) / (num_runs * 100)
        print(f"\n  PyGraham:")
        print(f"    Average time: {greedy_fp_time*1000:.4f}ms")
        print(f"    Distance: {dist_greedy_fp:.2f}")
        print(f"    Route: {list(route_greedy_fp)}")

        speedup = greedy_vanilla_time / greedy_fp_time
        print(f"\n    Speedup: {speedup:.2f}x {'faster' if speedup > 1 else 'slower'}")


def demonstrate_code_style():
    """Demonstrate stylistic advantages of PyGraham."""
    print(f"\n{'='*70}")
    print("CODE STYLE COMPARISON")
    print(f"{'='*70}\n")

    print("VANILLA PYTHON (Imperative, Mutable):")
    print("""
    results = []
    for perm in permutations(indices):
        route = list(perm)
        dist = calculate_distance(cities, route)
        if dist <= max_distance:
            results.append((route, dist))
    results.sort(key=lambda x: x[1])
    return results
    """)

    if HAS_PYGRAHAM:
        print("\nPYGRAHAM (Functional, Immutable):")
        print("""
    return (LazySequence.from_iterable(permutations(range(len(cities))))
            .map(lambda perm: ImmutableList(perm))
            .map(lambda route: (route, calculate_distance(cities, route)))
            .filter(lambda item: item[1] <= max_distance)
            .to_list())
        """)

        print("\nADVANTAGES:")
        print("  1. No mutable state - easier to reason about")
        print("  2. Composable operations - build complex logic from simple parts")
        print("  3. Lazy evaluation - only compute what's needed")
        print("  4. Declarative style - focus on WHAT, not HOW")
        print("  5. Easier to parallelize (immutable data)")


if __name__ == "__main__":
    # Small example for brute force
    small_cities = CITIES[:7]  # 7 cities = 5040 permutations

    # Run benchmarks
    benchmark_tsp(small_cities, num_runs=3)

    # Demonstrate code style
    demonstrate_code_style()

    print(f"\n{'='*70}\n")
