import math

import numpy as np

import utils

INPUT_URL = 'https://adventofcode.com/2020/day/3/input'


# I'm going to import numpy to make repeating right easier...

def get_map(filename, num_rights):
    with open(filename) as fh:
        map = []
        for line in fh:
            map.append([c == '#' for c in line.strip()])

        np_map = np.array(map)

        # Figure out how many times we need to repeat the map right to handle all moves
        total_right = np_map.shape[0] * num_rights
        num_repeats = math.ceil(total_right / np_map.shape[1])

        return np.tile(np_map, (1, num_repeats))


def traverse(map, rights, downs):
    current_pos = [0, 0]

    num_trees = 0

    while current_pos[0] < map.shape[0]:
        is_tree = map[current_pos[0], current_pos[1]]
        if is_tree:
            num_trees += 1

        current_pos[0] += downs
        current_pos[1] += rights
    return num_trees


def print_map(map):
    for r in map:
        for x in r:
            print('#' if x else '.', end='')
        print("")


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')
    map = get_map("cached_input.txt", 3)
    print_map(map)
    trees = traverse(map, 3, 1)
    print(f"Hit {trees} trees along the way")
