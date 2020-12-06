//
// Created by Ian Hales on 05/12/2020.
//
#include <string>
#include <vector>
#include <fstream>
#include <iostream>

using SumPair = std::pair<unsigned, unsigned>;
using ReportVector = std::vector<unsigned>;

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
            } else if (sum > target) {
                break;
            }
        }
    }
    return nullptr;
}

void task1(ReportVector const &sortedReport, const unsigned target) {
    auto pairPtr = findSumPair(sortedReport, target);

    if (!pairPtr) {
        std::cerr << "Couldn't find any pair of numbers that summed to the target of " << target << std::endl;
        return;
    }

    auto prod = pairPtr->first * pairPtr->second;

    std::cout << pairPtr->first << " + " << pairPtr->second << " == " << target << std::endl;
    std::cout << pairPtr->first << " * " << pairPtr->second << " = " << prod << std::endl;
}


int main() {
    auto file_path = "../../day1/cached_input.txt";
    unsigned target = 2020;

    auto report = ReportVector();
    readExpenseReport(file_path, report);
    std::sort(std::begin(report), std::end(report), std::greater<>());

    task1(report, target);

    return 0;
}

