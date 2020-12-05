import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent))
import utils

INPUT_URL = 'https://adventofcode.com/2020/day/4/input'

REQUIRED_FIELDS = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid"
]


def parse_passports(raw_data):
    cur_lines = []

    passports = []

    def parse(lines):
        flattened = " ".join(lines)
        pieces = flattened.split(" ")
        return dict(p.split(":") for p in pieces)

    for line in raw_data.split("\n"):
        if line.strip() == "" and len(cur_lines) > 0:
            passports.append(parse(cur_lines))
            cur_lines = []
            continue
        cur_lines.append(line)

    return passports


def is_valid(pport):
    return all(f in pport for f in REQUIRED_FIELDS)


def task_1(data):
    pports = parse_passports(data)
    valid = [p for p in pports if is_valid(p)]
    print(f"Valid passports: {len(valid)}")


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')

    print("Task 1:")
    task_1(input_data)

    print("")
