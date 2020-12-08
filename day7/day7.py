import pathlib
import re
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils

INPUT_URL = 'https://adventofcode.com/2020/day/7/input'


def extract_count_and_tag(item):
    if "no other bags" in item.strip():
        return 0, tuple()

    m = re.match(r'^(\d*) *(\w+) (\w+) bags*[.,]*$', item.strip())

    if m is None:
        return None

    count, adj_1, adj_2 = m.groups()
    count = None if count == "" else int(count)

    return count, (adj_1, adj_2)


def naive_parser(line):
    outermost_bag_str, contents_str = [l.strip() for l in line.split("contain")]

    _, outermost_tag = extract_count_and_tag(outermost_bag_str)

    contents = [extract_count_and_tag(x) for x in contents_str.split(",")]
    if contents is None:
        contents = []

    return outermost_tag, contents


def find_containers(data, key):
    """
    Data is a lookup table of outer bags to their contents (weighted edges).

    We'll search the LUT to find the bags that can contain `key`, then recursively
    search through the LUT until there are no containers for the current key.

    As we pass through a container, we'll add it to the set of discovered containers.

    :param data: The LUT of bags to contents
    :param key: The bag to search for
    :return: A set containing all the containers that we pass through while lookign for key.
    """

    containers = set()

    for outer, contents in data.items():
        content_bag_types = [x[1] for x in contents]
        if key in content_bag_types:
            containers.add(outer)

    for c in containers:
        containers = containers.union(find_containers(data, c))
    return containers


def task_1(data):
    tgt = ("shiny", "gold")

    edges = dict(naive_parser(line) for line in data.split("\n") if line.strip() != "")
    path = find_containers(edges, tgt)

    print(f"There are {len(path)} bags that can contain a {' '.join(tgt)} bag.")


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')

    print("Task 1")
    task_1(input_data)
