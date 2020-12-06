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
        ReportVector copyAndSort(const ReportVector &report) {
            auto sortedReport = ReportVector(report.size());
            std::partial_sort_copy(std::begin(report),
                                   std::end(report),
                                   std::begin(sortedReport),
                                   std::end(sortedReport),
                                   std::greater<>());
            return sortedReport;
        }

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

        std::unique_ptr<SumTuple> findSumTriple(ReportVector const &sortedReport, const unsigned target) {
            ReportVector::const_iterator fwdIter;
            ReportVector::const_reverse_iterator bwdIter;
            ReportVector::const_reverse_iterator interIter;

            for (fwdIter = std::begin(sortedReport); fwdIter != std::end(sortedReport); ++fwdIter) {
                for (bwdIter = std::rbegin(sortedReport); bwdIter.base() != fwdIter + 1; ++bwdIter) {
                    if (*fwdIter + *bwdIter > target) {
                        break;
                    }

                    for (interIter = ReportVector::const_reverse_iterator(bwdIter);
                         interIter.base() != fwdIter; ++interIter) {
                        auto sum = *fwdIter + *bwdIter + *interIter;
                        if (sum == target) {
                            return std::unique_ptr<SumTuple>(new SumTuple{*fwdIter, *interIter, *bwdIter});
                        }
                        if (sum > target) {
                            break;
                        }
                    }
                }
            }
            return nullptr;
        }

        unsigned task1(ReportVector const &report, const unsigned target) {
            // Copy and sort rather than sorting in-place (so we don't affect task 2).
            auto pairPtr = findSumPair(copyAndSort(report), target);

            if (!pairPtr) {
                throw std::runtime_error("Couldn't find any pair of numbers that summed to the target");
            }

            auto prod = pairPtr->first * pairPtr->second;

            std::cout << pairPtr->first << " + " << pairPtr->second << " == " << target << std::endl;
            std::cout << pairPtr->first << " * " << pairPtr->second << " = " << prod << std::endl;
            return prod;
        }

        unsigned task2(ReportVector const &report, const unsigned target) {
            // Copy and sort rather than sorting in-place (so we don't affect task 2).
            auto tripletPtr = findSumTriple(copyAndSort(report), target);

            if (!tripletPtr) {
                throw std::runtime_error("Couldn't find any triplet of numbers that summed to the target");
            }

            const auto v0 = std::get<0>(*tripletPtr);
            const auto v1 = std::get<1>(*tripletPtr);
            const auto v2 = std::get<2>(*tripletPtr);
            const auto prod = v0 * v1 * v2;

            std::cout << v0 << " + " << v1 << " + " << v2 << "  == " << target << std::endl;
            std::cout << v0 << " * " << v1 << " * " << v2 << "  == " << prod << std::endl;
            return prod;
        }

        void run(const std::string filePath, const unsigned target) {
            auto report = ReportVector();
            readExpenseReport(filePath, report);
            std::cout << "Task 1: " << std::endl;
            task1(report, target);

            std::cout << "\nTask 2: " << std::endl;
            task2(report, target);
        }
    }
}