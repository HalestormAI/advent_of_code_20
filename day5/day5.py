import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils

INPUT_URL = 'https://adventofcode.com/2020/day/5/input'


def bsp_to_int(encoding):
    pos = 0
    for i, e in enumerate(encoding):
        # Optimisation - we don't need to do anything if e == 0
        if e == 0:
            continue
        pos += 2 ** (len(encoding) - 1 - i) * e
    return pos


def encode_pass_str(pass_str):
    row_enc = [0 if s == 'F' else 1 for s in pass_str[:-3]]
    col_enc = [0 if s == 'L' else 1 for s in pass_str[-3:]]
    return row_enc, col_enc


def coord_to_id(row, col):
    return row * 8 + col


def parse_pass_to_id(pass_str):
    row_enc, col_enc = encode_pass_str(pass_str)
    row_num = bsp_to_int(row_enc)
    col_num = bsp_to_int(col_enc)
    seat_id = coord_to_id(row_num, col_num)
    return seat_id


def task_1(input_data):
    seat_ids = [parse_pass_to_id(l.strip()) for l in input_data.split("\n") if l.strip() != ""]
    max_id = max(seat_ids)
    return max_id


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')

    print("Task 1:")
    max_id = task_1(input_data)
    print(f"The highest ID is {max_id}")
