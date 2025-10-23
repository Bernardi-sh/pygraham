cmake_minimum_required(VERSION 3.15)
project(pygraham_fast)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find pybind11
find_package(pybind11 CONFIG)

if(NOT pybind11_FOUND)
    # Fallback: try to use pybind11 from pip
    execute_process(
        COMMAND python3 -c "import pybind11; print(pybind11.get_cmake_dir())"
        OUTPUT_VARIABLE pybind11_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    find_package(pybind11 CONFIG PATHS ${pybind11_DIR})
endif()

# Create the extension module
pybind11_add_module(_fast _fast.cpp)

# Optimization flags
if(MSVC)
    target_compile_options(_fast PRIVATE /O2)
else()
    target_compile_options(_fast PRIVATE -O3 -march=native)
endif()
