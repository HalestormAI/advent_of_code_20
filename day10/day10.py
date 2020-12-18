import pathlib
import sys
from collections import Counter, defaultdict

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils

INPUT_URL = 'https://adventofcode.com/2020/day/10/input'


class InvalidJoltageException(Exception):
    pass


def get_difference_frequency(data):
    data = sorted(data)

    difference_freq = Counter()

    last_val = 0
    for d in data:
        difference = d - last_val

        if difference > 3:
            raise InvalidJoltageException()

        last_val = d

        difference_freq[difference] += 1

    # Add the 3 Jolt difference for my device adapter
    difference_freq[3] += 1
    return difference_freq


def task_1(raw_data):
    data = list(utils.parse_int_data(raw_data))
    freqs = get_difference_frequency(data)
    prod_1x3 = freqs[1] * freqs[3]
    print("Joltage differences: ", freqs)
    print(f"Product of 1 and 3 differences: {prod_1x3}")
    return prod_1x3


def task_2(raw_data):
    data = list(utils.parse_int_data(raw_data))
    tgt = max(data) + 3
    data += [tgt]
    data.sort()

    scores = defaultdict(int)
    scores[0] = 1
    for d in data:
        scores[d] = scores[d - 3] + scores[d - 2] + scores[d - 1]

    print(f"Total number of valid arrangements is {scores[data[-1]]}")


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')
    print("Task 1:")
    task_1(input_data)

    print()
    print("Task 2:")
    task_2(input_data)
