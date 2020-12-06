//
// Created by Ian Hales on 06/12/2020.
//
#include <string>
#include "day1.hpp"


int main() {
    const std::string filePath = "../../day1/cached_input.txt";
    const unsigned target = 2020;
    AdventOfCode2020::Day1::run(filePath, target);
    return 0;
}