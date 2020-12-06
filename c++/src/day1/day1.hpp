//
// Created by Ian Hales on 06/12/2020.
//

#ifndef ADVENT_OF_CODE_2020_DAY1_HPP
#define ADVENT_OF_CODE_2020_DAY1_HPP

namespace AdventOfCode2020 {
    namespace Day1 {
        using SumPair = std::pair<unsigned, unsigned>;
        using ReportVector = std::vector<unsigned>;

        void run(const std::string filePath, const unsigned target);

        std::unique_ptr<SumPair> findSumPair(ReportVector const &sortedReport, const unsigned target);

        unsigned task1(ReportVector const &report, const unsigned target);
    }
}
#endif //ADVENT_OF_CODE_2020_DAY1_HPP
