import enum
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils

INPUT_URL = 'https://adventofcode.com/2020/day/6/input'


class GroupInputParser:
    class Mode(enum.Enum):
        UNION = 0
        INTERSECT = 1

    def __init__(self, mode):
        self.current_group = None
        self.groups = []
        self.mode = mode

    def parse(self, raw_data):
        lines = raw_data.split("\n")
        for line in lines:
            if line.strip() == "":
                self._complete_group()
                continue
            line_set = set(line.strip())

            if self.current_group is None:
                self.current_group = line_set
            elif self.mode == GroupInputParser.Mode.INTERSECT:
                self.current_group.intersection_update(line_set)
            else:
                self.current_group = self.current_group.union(line_set)

        self._complete_group()
        return self.groups

    def _complete_group(self):
        if self.current_group is not None and len(self.current_group) > 0:
            self.groups.append(self.current_group)
        self._reset_current()

    def _reset_current(self):
        self.current_group = None


def calculate_sum_counts(data, parse_mode):
    parser = GroupInputParser(parse_mode)
    groups = parser.parse(data)
    return sum(map(len, groups))


def task_1(data):
    total = calculate_sum_counts(data, GroupInputParser.Mode.UNION)
    print(f"The sum of all questions per group is {total}")


def task_2(data):
    total = calculate_sum_counts(data, GroupInputParser.Mode.INTERSECT)
    print(f"The sum of all questions per group is {total}")


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')

    print("Task 1:")
    task_1(input_data)

    print("")
    print("Task 2:")
    task_2(input_data)
