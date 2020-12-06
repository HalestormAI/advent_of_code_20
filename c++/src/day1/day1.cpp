//
// Created by Ian Hales on 05/12/2020.
//
#include <string>
#include <vector>
#include <fstream>
#include <iostream>

#include "day1.hpp"

namespace AdventOfCode2020 {
    namespace Day1 {
        void readExpenseReport(const std::string filename, ReportVector &output) {
            std::ifstream infile(filename);

            int currentValue;
            while (infile >> currentValue) {
                output.push_back(currentValue);
            }
        }

        std::unique_ptr<SumPair> findSumPair(ReportVector const &sortedReport, const unsigned target) {
            ReportVector::const_iterator fwdIter;
            ReportVector::const_reverse_iterator bwdIter;

            for (fwdIter = std::begin(sortedReport); fwdIter != std::end(sortedReport); ++fwdIter) {
                for (bwdIter = std::rbegin(sortedReport); bwdIter.base() != fwdIter; ++bwdIter) {
                    auto sum = *fwdIter + *bwdIter;
                    if (sum == target) {
                        return std::unique_ptr<SumPair>(new SumPair(*fwdIter, *bwdIter));
                    }
                }
            }
            return nullptr;
        }

        unsigned task1(ReportVector const &report, const unsigned target) {
            // Copy and sort rather than sorting in-place (so we don't affect task 2).
            auto sortedReport = ReportVector();
            std::partial_sort_copy(std::begin(report),
                                   std::end(report),
                                   std::begin(sortedReport),
                                   std::end(sortedReport));

            auto pairPtr = findSumPair(report, target);

            if (!pairPtr) {
                throw std::runtime_error("Couldn't find any pair of numbers that summed to the target");
            }

            auto prod = pairPtr->first * pairPtr->second;

            std::cout << pairPtr->first << " + " << pairPtr->second << " == " << target << std::endl;
            std::cout << pairPtr->first << " * " << pairPtr->second << " = " << prod << std::endl;
            return prod;
        }

        void run(const std::string filePath, const unsigned target) {
            auto report = ReportVector();
            readExpenseReport(filePath, report);
            task1(report, target);
        }
    }
}