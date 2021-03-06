import pathlib
import sys
from functools import reduce
from operator import mul

INPUT_URL = 'https://adventofcode.com/2020/day/1/input'
TARGET = 2020

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils


# Notes:
#   * These could've been made a lot easier using Numpy and logical indexing, but where's the fun in that? :)
#   * I'm assuming positive, integer values in the input file. Let's not over-engineer too much...
#   * The input data code is unnecessary, could just read a text file, but I fancied doing it!


def parse_input_data(cache_file, url, cookie_file):
    """
    Calls the utility function to load either a cached data file or pull it from the AoC server, then splits it
    on newlines, strips the lines and extracts the integer values.

    :param cache_file:      The file in which the input data is stored
    :param url:             The URL to the AoC page
    :param cookie_file:     The path to the cookie file (only used if the cache file isn't found
    :return: The input data as a list of ints
    """
    raw_data = utils.load_input_data(cache_file, url, cookie_file)
    return [int(r.strip()) for r in raw_data.split("\n") if r.strip() != ""]


def find_2020_sum_pair(data):
    """
    Sort the data from largest to smallest.

    Iterate through the data. Take the biggest untested number. Then work backwards from the smallest number to find
    the right value. If the total exceeds the target (2020), then we know for sure that there is no small number in the\
    list capable of summing with the big number to reach 2020.

    """
    data = sorted(data, reverse=True)

    for idx, item in enumerate(data):
        test_idx = range(len(data) - 1, idx, -1)
        for rev_idx in test_idx:
            reverse_item = data[rev_idx]
            if item + reverse_item > TARGET:
                break

            if item + reverse_item == TARGET:
                return item, reverse_item

    return None, None


def find_2020_sum_triple(data):
    """
    Similar to the above, but this time hunting three values that sum to 2020.

    The basic algorithm is similar, use the big and small numbers to check if there's scope for another number to be
    added to the sum in order to make 2020.

    If big + small < 2020, then we'll check all the numbers in-between, starting small (because it's intuitively more
    likely the intermediate value is at the smaller end).

    :param data:
    :param data: List of integer inputs
    :return: The three values that sum to 2020.
    """
    data = sorted(data, reverse=True)

    for idx, item in enumerate(data):
        test_idx = range(len(data) - 1, idx + 1, -1)
        for rev_idx in test_idx:
            reverse_item = data[rev_idx]
            if item + reverse_item > TARGET:
                break

            for mid_item in data[rev_idx:idx:-1]:
                total = mid_item + item + reverse_item
                if total == TARGET:
                    return mid_item, item, reverse_item

                if total > TARGET:
                    break

    return None, None, None


def check(numbers, expected_len):
    """
    Test that we've got the correct length of numbers array and that the sum of those numbers is 2020, as expected.

    If these conditions are met, print the product of the numbers.

    :param numbers:         The list of suitable numbers from the search algo
    :param expected_len:    How many numbers we expect to be in that list
    :return:                None
    """
    assert len(numbers) == expected_len, f"Numbers list should be of length {expected_len}, was {len(numbers)}"
    assert sum(numbers) == TARGET, f"Numbers do not sum to {TARGET}, ({sum(numbers)})"

    prod = reduce(mul, numbers, 1)

    print(f"Found a valid set: {numbers}: {prod}")


if __name__ == "__main__":
    input_data = parse_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')

    print("Part 1:")
    numbers = find_2020_sum_pair(input_data)
    check(numbers, 2)

    print("")
    print("Part 2:")
    numbers = find_2020_sum_triple(input_data)
    check(numbers, 3)
