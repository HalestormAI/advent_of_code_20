import math
import pathlib
import sys
from functools import reduce
from operator import mul

import numpy as np

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils

INPUT_URL = 'https://adventofcode.com/2020/day/3/input'


# I'm going to import numpy to make repeating right easier...

def get_map(raw_data, num_rights):
    """
    For each line in the map text file, load it into a boolean array, then convert to
    numpy, to allow us to tile it easily (this isn't required for the algo, but saves
    some boilerplate).

    We work out how many times to replicate the map right by taking the number of right
    moves to make on a single row, then multiplying that by the number of rows. We then
    ceil-divide that to get the number of copies of the map we need right-wards.

    :param raw_data:    The raw text data from the input file
    :param num_rights:  The largest number of right-moves we need per row.
    :return:            The map, sufficiently wide for the required moves, as a boolean np array.
    """
    map = []
    for line in raw_data.split("\n"):
        if line.strip() != "":
            map.append([c == '#' for c in line.strip()])

    np_map = np.array(map)

    # Figure out how many times we need to repeat the map right to handle all moves
    total_right = np_map.shape[0] * num_rights
    num_repeats = math.ceil(total_right / np_map.shape[1])

    return np.tile(np_map, (1, num_repeats))


def traverse(map, rights, downs):
    """
    Traverse a map, created using `get_map`, by repeating through the move and advancing a
    position pointer accordingly. We stop when we've passed beyond the last row of the map.

    As we hit a tree, we increment a counter, which is retuened at the end.

    :param map:     Boolean numpy map from `get_map`
    :param rights:  The number of right-cells to move in a single step
    :param downs:   The number of down-cells to move in a single step
    :return:        The number of trees we hit along the way.
    """
    current_pos = [0, 0]

    num_trees = 0

    while current_pos[0] < map.shape[0]:
        is_tree = map[current_pos[0], current_pos[1]]
        if is_tree:
            num_trees += 1

        current_pos[0] += downs
        current_pos[1] += rights
    return num_trees


def task_1(data):
    """
    Navigate the map with the given move of (3, 1)
    :param data: The raw data from the input file
    :return: None
    """
    map = get_map(data, 3)
    trees = traverse(map, 3, 1)
    print(f"Hit {trees} trees along the way")


def task_2(data, routes):
    """
    Navigate the map with the set of moved provided for task 2.
    :param data: The raw data from the input file
    :return: None
    """
    max_right = max(r[0] for r in routes)
    map = get_map(data, max_right)

    route_trees = [traverse(map, r[0], r[1]) for r in routes]
    prod = reduce(mul, route_trees, 1)
    print(f"Hit {prod} trees along the way over all paths")


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')

    print("Task 1:")
    task_1(input_data)

    print("")
    print("Task 2:")
    routes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    ]
    task_2(input_data, routes)
