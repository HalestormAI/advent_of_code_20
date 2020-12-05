import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils

INPUT_URL = 'https://adventofcode.com/2020/day/5/input'


def bsp_to_int(encoding):
    """
    The binary space partitioning algorithm basically boils down to accumulating
    the binary value of each element of the string.

    e.g. 100 would be 1*4 + 0*2 + 0*1 := 4

    :param encoding: Binary encoded list representing the coordinate
    :return:         The integer representation of that string.
    """
    pos = 0
    for i, e in enumerate(encoding):
        # Optimisation - we don't need to do anything if e == 0
        if e == 0:
            continue
        pos += 2 ** (len(encoding) - 1 - i) * e
    return pos


def encode_pass_str(pass_str):
    """
    Take the boarding pass string, split it into the row and column indices, then encode
    to 1s and 0s,

    Although row and col use different letters to define the BSP input, they boil
    down to binary strings. We'll convert them to a homogenous format for the BSP
    decoder.

    :param pass_str: A boarding pass string in the format [BF]{7}[LR]{3}
    :return:         The binary encoded strings for row and col
    """
    row_enc = [0 if s == 'F' else 1 for s in pass_str[:-3]]
    col_enc = [0 if s == 'L' else 1 for s in pass_str[-3:]]
    return row_enc, col_enc


def coord_to_id(row, col):
    """
    Generate the seat ID from the row and column coords.

    :param row: Integer to define the row number
    :param col: Integer to define the column number
    :return: The seat ID.
    """
    return row * 8 + col


def parse_pass_to_id(pass_str):
    """
    Glue the pieces above together. Take a single boarding pass string, encode it
    to a list of 1s and 0s for both rows and cols, then convert that to an integer
    and use to generate the seat ID.

    :param pass_str: A boarding pass string in the format [BF]{7}[LR]{3}
    :return:         The ID of the seat (row * 8 + col)
    """
    row_enc, col_enc = encode_pass_str(pass_str)
    row_num = bsp_to_int(row_enc)
    col_num = bsp_to_int(col_enc)
    seat_id = coord_to_id(row_num, col_num)
    return seat_id


def task_1(input_data):
    """
    Split the input data on newlines, strip it and then parse it.
    By doing this in a list comprehension, we get a list of all IDs, then it's a simple
    case of calling `max` on the list.

    :param input_data:  The raw input string from the task data
    :return:            The missing seat ID.
    """
    seat_ids = [parse_pass_to_id(l.strip()) for l in input_data.split("\n") if l.strip() != ""]
    max_id = max(seat_ids)
    return max_id


def task_2(input_data):
    """
    Here, we'll take advantage of the fact that our (missing) seat ID is definitely
    in between two existing IDs. If we sort all the seat IDs, the difference between
    any consecutive pair of IDs should be exactly 1. If it's larger, it's our seat.

    :param input_data:  The raw input string from the task data
    :return:            The missing seat ID.
    """
    seat_ids = [parse_pass_to_id(l.strip()) for l in input_data.split("\n") if l.strip() != ""]
    seat_ids.sort()

    # We'll find the gap by looking at the differences between all consecutive seat
    # ids. If the diff is > 1, it's probably our seat
    id_diffs = (seat_ids[i + 1] - seat_ids[i] for i in range(len(seat_ids) - 1))
    missing_idxs = [i for i, d in enumerate(id_diffs) if d > 1]

    assert len(missing_idxs) == 1, "There should be exactly one empty seat!"

    # By now, we've found the index to the seat ID before the missing one, in the
    # sorted list. The missing one should be `seat[idx] + 1`
    return seat_ids[missing_idxs[0]] + 1


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')

    print("Task 1:")
    max_id = task_1(input_data)
    print(f"The highest ID is {max_id}")

    print("Task 2:")
    my_seat = task_2(input_data)
    print(f"My seat ID is {my_seat}")
