#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <cmath>
#include <unordered_map>

namespace py = pybind11;

// Fast map operation on vectors
template<typename T, typename F>
std::vector<T> fast_map(const std::vector<T>& vec, F func) {
    std::vector<T> result;
    result.reserve(vec.size());
    std::transform(vec.begin(), vec.end(), std::back_inserter(result), func);
    return result;
}

// Fast filter operation
template<typename T, typename F>
std::vector<T> fast_filter(const std::vector<T>& vec, F predicate) {
    std::vector<T> result;
    std::copy_if(vec.begin(), vec.end(), std::back_inserter(result), predicate);
    return result;
}

// Fast reduce operation
template<typename T, typename U, typename F>
U fast_reduce(const std::vector<T>& vec, U initial, F func) {
    return std::accumulate(vec.begin(), vec.end(), initial, func);
}

// Fast integer operations
std::vector<int64_t> fast_map_int(const std::vector<int64_t>& vec, py::function func) {
    std::vector<int64_t> result;
    result.reserve(vec.size());
    for (const auto& item : vec) {
        result.push_back(func(item).cast<int64_t>());
    }
    return result;
}

std::vector<double> fast_map_double(const std::vector<double>& vec, py::function func) {
    std::vector<double> result;
    result.reserve(vec.size());
    for (const auto& item : vec) {
        result.push_back(func(item).cast<double>());
    }
    return result;
}

std::vector<int64_t> fast_filter_int(const std::vector<int64_t>& vec, py::function predicate) {
    std::vector<int64_t> result;
    for (const auto& item : vec) {
        if (predicate(item).cast<bool>()) {
            result.push_back(item);
        }
    }
    return result;
}

std::vector<double> fast_filter_double(const std::vector<double>& vec, py::function predicate) {
    std::vector<double> result;
    for (const auto& item : vec) {
        if (predicate(item).cast<bool>()) {
            result.push_back(item);
        }
    }
    return result;
}

// Fast sum for numeric types
int64_t fast_sum_int(const std::vector<int64_t>& vec) {
    return std::accumulate(vec.begin(), vec.end(), int64_t(0));
}

double fast_sum_double(const std::vector<double>& vec) {
    return std::accumulate(vec.begin(), vec.end(), 0.0);
}

// Fast composition of functions (for performance benchmarking)
class FastPipeline {
private:
    std::vector<py::function> functions;

public:
    void add_function(py::function func) {
        functions.push_back(func);
    }

    py::object execute(py::object input) {
        py::object result = input;
        for (const auto& func : functions) {
            result = func(result);
        }
        return result;
    }
};

// Fast memoization for pure functions
class FastMemoizer {
private:
    std::unordered_map<std::string, py::object> cache;
    py::function func;

public:
    FastMemoizer(py::function f) : func(f) {}

    py::object call(const std::string& key) {
        auto it = cache.find(key);
        if (it != cache.end()) {
            return it->second;
        }
        py::object result = func(key);
        cache[key] = result;
        return result;
    }

    size_t cache_size() const {
        return cache.size();
    }

    void clear_cache() {
        cache.clear();
    }
};

// Fast combinatorial operations for TSP-like problems
double calculate_distance(const std::pair<double, double>& p1,
                         const std::pair<double, double>& p2) {
    double dx = p1.first - p2.first;
    double dy = p1.second - p2.second;
    return std::sqrt(dx * dx + dy * dy);
}

double calculate_path_length(const std::vector<std::pair<double, double>>& points,
                            const std::vector<int>& order) {
    double total = 0.0;
    for (size_t i = 0; i < order.size() - 1; ++i) {
        total += calculate_distance(points[order[i]], points[order[i + 1]]);
    }
    // Add distance back to start
    total += calculate_distance(points[order.back()], points[order[0]]);
    return total;
}

// Fast permutation generation for small TSP instances
std::vector<std::vector<int>> generate_permutations(int n) {
    std::vector<int> elements(n);
    std::iota(elements.begin(), elements.end(), 0);

    std::vector<std::vector<int>> result;
    do {
        result.push_back(elements);
    } while (std::next_permutation(elements.begin(), elements.end()));

    return result;
}

PYBIND11_MODULE(_fast, m) {
    m.doc() = "High-performance C++ extensions for PyGraham";

    m.def("fast_map_int", &fast_map_int, "Fast map for integer vectors");
    m.def("fast_map_double", &fast_map_double, "Fast map for double vectors");
    m.def("fast_filter_int", &fast_filter_int, "Fast filter for integer vectors");
    m.def("fast_filter_double", &fast_filter_double, "Fast filter for double vectors");
    m.def("fast_sum_int", &fast_sum_int, "Fast sum for integer vectors");
    m.def("fast_sum_double", &fast_sum_double, "Fast sum for double vectors");
    m.def("calculate_path_length", &calculate_path_length, "Calculate TSP path length");
    m.def("generate_permutations", &generate_permutations, "Generate all permutations");

    py::class_<FastPipeline>(m, "FastPipeline")
        .def(py::init<>())
        .def("add_function", &FastPipeline::add_function)
        .def("execute", &FastPipeline::execute);

    py::class_<FastMemoizer>(m, "FastMemoizer")
        .def(py::init<py::function>())
        .def("call", &FastMemoizer::call)
        .def("cache_size", &FastMemoizer::cache_size)
        .def("clear_cache", &FastMemoizer::clear_cache);
}
