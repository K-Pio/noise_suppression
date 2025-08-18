cmake_minimum_required(VERSION 3.15)
project(acoustic_cpp LANGUAGES CXX)

unset(PythonInterp_FOUND CACHE)
unset(PYTHON_EXECUTABLE CACHE)
unset(PYTHON_VERSION_STRING CACHE)

cmake_policy(SET CMP0148 NEW)

# Wymuś nowoczesne wykrywanie Pythona
find_package(Python REQUIRED COMPONENTS Interpreter Development)



# 1) Znajdź Python i pybind11 (najprościej: pybind11 jako submodule lub z pakietu)
# Opcja A: FetchContent (bez instalacji systemowej)
include(FetchContent)

set(PYBIND11_NEWPOLICY ON)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v2.11.1
)
FetchContent_MakeAvailable(pybind11)

message(STATUS "Python executable: ${Python_EXECUTABLE}")
message(STATUS "Python version: ${Python_VERSION}")

# 2) Ustaw standard C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 3) Zbuduj moduł rozszerzeń dla Pythona
pybind11_add_module(acoustics_c
  cpp/bindings.cpp
  cpp/acoustics.cpp
)

# 4) (opcjonalnie) flage ostrzeżeń
if(MSVC)
  target_compile_options(acoustics_c PRIVATE /W4 /permissive-)
else()
  target_compile_options(acoustics_c PRIVATE -Wall -Wextra -Wpedantic)
endif()
