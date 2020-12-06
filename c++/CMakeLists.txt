cmake_minimum_required(VERSION 3.17)

project(advent_of_code_2020)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(Day1 src/day1/main.cpp src/day1/day1.cpp)

find_package(GTest REQUIRED)
include(GoogleTest)

enable_testing()
add_executable(Day1Test src/day1/day1_test.cpp src/day1/day1.cpp)
target_link_libraries(Day1Test GTest::GTest GTest::Main)
gtest_add_tests(Day1Test "" AUTO)
