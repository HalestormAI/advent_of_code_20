//
// Created by Ian Hales on 06/12/2020.
//
#include "gtest/gtest.h"
#include "day1.hpp"

const auto EXAMPLE_REPORT = AdventOfCode2020::Day1::ReportVector{1721, 979, 366, 299, 675, 1456};
const auto EXAMPLE_REPORT_NO_PAIR = AdventOfCode2020::Day1::ReportVector{1721, 979, 366, 675, 1456};

TEST (FullTask1Integration, ExampleValidData) {
    ASSERT_EQ(514579, AdventOfCode2020::Day1::task1(EXAMPLE_REPORT, 2020));
}

TEST (FullTask1Integration, ExampleInvalidData) {
    EXPECT_ANY_THROW(AdventOfCode2020::Day1::task1(EXAMPLE_REPORT_NO_PAIR, 2020));
}

TEST (FindSumPair, ValidExampleCase) {
    const auto goodOutput = AdventOfCode2020::Day1::findSumPair(EXAMPLE_REPORT, 2020);
    ASSERT_EQ(1721, goodOutput->first);
    ASSERT_EQ(299, goodOutput->second);
}

TEST (FindSumPair, InvalidExampleCase) {
    ASSERT_EQ(nullptr, AdventOfCode2020::Day1::findSumPair(EXAMPLE_REPORT_NO_PAIR, 2020));
}