import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils

INPUT_URL = 'https://adventofcode.com/2020/day/6/input'


class GroupInputParser:
    def __init__(self):
        self.current_group = None
        self.groups = []

    def parse(self, raw_data):
        self._reset_current()

        lines = raw_data.split("\n")
        for line in lines:
            if line.strip() == "":
                self._complete_group()
                continue
            line_set = set(line.strip())
            self.current_group = self.current_group.union(line_set)

        self._complete_group()
        return self.groups

    def _complete_group(self):
        if len(self.current_group) > 0:
            self.groups.append(self.current_group)
            self._reset_current()

    def _reset_current(self):
        self.current_group = set()


def calculate_sum_counts(data):
    parser = GroupInputParser()
    groups = parser.parse(data)
    return sum(map(len, groups))


def task_1(data):
    total = calculate_sum_counts(data)
    print(f"The sum of all questions per group is {total}")


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')

    print("Task 1:")
    task_1(input_data)
