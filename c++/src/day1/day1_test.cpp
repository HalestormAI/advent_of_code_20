//
// Created by Ian Hales on 06/12/2020.
//
#include "gtest/gtest.h"
#include "day1.hpp"

const auto EXAMPLE_REPORT = AdventOfCode2020::Day1::ReportVector{1721, 979, 366, 299, 675, 1456};
const auto EXAMPLE_REPORT_NO_PAIR = AdventOfCode2020::Day1::ReportVector{1721, 979, 366, 675, 1456};
const auto EXAMPLE_REPORT_NO_TRIPLE = AdventOfCode2020::Day1::ReportVector{1721, 979, 299, 675, 1456};

const auto SORTED_EXAMPLE_REPORT = AdventOfCode2020::Day1::ReportVector{1721, 1456, 979, 675, 366, 299};
const auto SORTED_EXAMPLE_REPORT_NO_PAIR = AdventOfCode2020::Day1::ReportVector{1721, 1456, 979, 675, 366};
const auto SORTED_EXAMPLE_REPORT_NO_TRIPLE = AdventOfCode2020::Day1::ReportVector{1721, 1456, 979, 675, 299};

TEST (Task1_Integration, ExampleValidData) {
    ASSERT_EQ(514579, AdventOfCode2020::Day1::task1(EXAMPLE_REPORT, 2020));
}

TEST (Task1_Integration, ExampleInvalidData) {
    EXPECT_ANY_THROW(AdventOfCode2020::Day1::task1(EXAMPLE_REPORT_NO_PAIR, 2020));
}

TEST (Task1_FindSumPair, ValidExampleCase) {
    const auto goodOutput = AdventOfCode2020::Day1::findSumPair(SORTED_EXAMPLE_REPORT, 2020);
    ASSERT_EQ(1721, goodOutput->first);
    ASSERT_EQ(299, goodOutput->second);
}

TEST (Task1_FindSumPair, InvalidExampleCase) {
    ASSERT_EQ(nullptr, AdventOfCode2020::Day1::findSumPair(SORTED_EXAMPLE_REPORT_NO_PAIR, 2020));
}

TEST (Task2_Integration, ExampleValidData) {
    ASSERT_EQ(241861950, AdventOfCode2020::Day1::task2(EXAMPLE_REPORT, 2020));
}

TEST (Task2_Integration, ExampleInvalidData) {
    EXPECT_ANY_THROW(AdventOfCode2020::Day1::task2(SORTED_EXAMPLE_REPORT_NO_TRIPLE, 2020));
}

TEST (Task2_FindSumTriple, ValidExampleCase) {
    const auto goodOutput = AdventOfCode2020::Day1::findSumTriple(SORTED_EXAMPLE_REPORT, 2020);
    ASSERT_EQ(979, std::get<0>(*goodOutput));
    ASSERT_EQ(675, std::get<1>(*goodOutput));
    ASSERT_EQ(366, std::get<2>(*goodOutput));
}

TEST (Task2_FindSumTriple, InvalidExampleCase) {
    ASSERT_EQ(nullptr, AdventOfCode2020::Day1::findSumTriple(SORTED_EXAMPLE_REPORT_NO_TRIPLE, 2020));
}