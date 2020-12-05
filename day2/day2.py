import pathlib
import re
import sys

INPUT_URL = 'https://adventofcode.com/2020/day/2/input'
TARGET = 2020

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils


def parse_input_data(cache_file, url, cookie_file):
    """
    Calls the utility function to load either a cached data file or pull it from the AoC server, then splits it
    on newlines, strips the lines and extracts the password rules.

    :param cache_file:      The file in which the input data is stored
    :param url:             The URL to the AoC page
    :param cookie_file:     The path to the cookie file (only used if the cache file isn't found
    :return: The input data as a list of rows, where each row is (min_val, max_val, required_letter, password)
    """

    raw_data = utils.load_input_data(cache_file, url, cookie_file)

    def extract_info(line):
        m = re.match(r'^(\d+)-(\d+)\s(\w+):\s([^\s]+)\s*$', line)
        if m is None:
            return None

        min_val = int(m.group(1))
        max_val = int(m.group(2))
        req_letter = m.group(3)
        password = m.group(4)

        return (min_val, max_val, req_letter, password)

    data = [extract_info(line) for line in raw_data.split("\n")]
    return [d for d in data if d is not None]


def check_pwd_validity_task_1(input_data):
    """
    Run through all the loaded password/rule combinations and return only those that are valid.

    This uses the task 1 validity rule, where `x-y z:` indicates the character `z` must appear between `x` and `y`
    times.

    :param input_data: The rows of parsed input data, where each row contains (min_val, max_val, req_letter, password).
    :return: The rows from above where the password meets the requirements.
    """

    def check_valid(row):
        min_val, max_val, req_letter, password = row
        num_letter = password.count(req_letter)
        return min_val <= num_letter <= max_val

    return [r for r in input_data if check_valid(r)]


def check_pwd_validity_task_2(input_data):
    """
    Run through all the loaded password/rule combinations and return only those that are valid.

    This uses the task 2 validity rule, where `x-y z:` indicates the character `z` must appear at either position `x`
    or `y`, but not both. `x` and `y` are 1-indexed, not 0-indexed.

    :param input_data: The rows of parsed input data, where each row contains (min_val, max_val, req_letter, password).
    :return: The rows from above where the password meets the requirements.
    """

    def check_valid(row):
        first_pos, second_pos, req_letter, password = row
        is_first_pos = password[first_pos - 1] == req_letter
        is_second_pos = password[second_pos - 1] == req_letter
        return (is_first_pos or is_second_pos) and not (is_first_pos and is_second_pos)

    return [r for r in input_data if check_valid(r)]


if __name__ == "__main__":
    input_data = parse_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')

    print("Task 1:")
    d = check_pwd_validity_task_1(input_data)
    print(f"Found {len(d)} valid passwords")

    print("Task 2:")
    d = check_pwd_validity_task_2(input_data)
    print(f"Found {len(d)} valid passwords")
