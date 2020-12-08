import pathlib
import re
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils

INPUT_URL = 'https://adventofcode.com/2020/day/7/input'


def create_LUT(raw_data):
    """
    Using the parsers above, convert the list of key/content tuples to a lookup dictionary we
    can use for tree navigation.

    :param raw_data: The newline-delimited string containing all the data.
    :return: A LUT (dictionary) of (adj_1, adj_2) -> [(num, (adj_1, adj_2))]
    """
    return dict(naive_parser(line) for line in raw_data.split("\n") if line.strip() != "")


def extract_count_and_tag(item):
    """
    Given a set of words that describe a bag, extract the number of bags (if defined) and a
    tuple containing the pair of adjectives that describe it.

    If provided with "no other bags", will return None as a special case.

    If provided invalid input, will also return None.

    The number of bags is optional, and will return None if not provided.

    Assumes the input is form '...<adj> <adj> bags...' or '<integer> <adj> <adj> bags...'.

    Examples:
            "light red bags" -> (None, ('light', 'red')
            "2 muted yellow bags." -> (2, ('muted', 'yellow')
            "no other bags" -> None
            "this is invalid text" -> None

    :param item: The count/adjective/noun string
    :return: count: Integer, (adjective_1: str, adjective_2: str)
    """
    if "no other bags" in item.strip():
        return None

    m = re.match(r'^(\d*) *(\w+) (\w+) bags*[.,]*$', item.strip())

    if m is None:
        return None

    count, adj_1, adj_2 = m.groups()
    count = None if count == "" else int(count)

    return count, (adj_1, adj_2)


def naive_parser(line):
    """
    Blunt-force parser for the input strings, splits them on the word "contain" and cleans any
    extraneous whitespace off the end. This should give two tokens, one for the container bag and
    one for its contents.

    The container text is parsed using the `extract_count_and_tag` function above.

    We then split the contents string on ',' and parse the remaining tokens. If the bag contains
    no others, it will receive None for the contents, which will then return an empty list to the
    caller.

    :param line: The full bag description line from the input file.
    :return: The key for this bag, and the contents of it (as a list of (number, key) tuples).
    """
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
        if contents[0] is None:
            continue

        content_bag_types = [x[1] for x in contents]
        if key in content_bag_types:
            containers.add(outer)

    for c in containers:
        containers = containers.union(find_containers(data, c))
    return containers


def find_internal_bags(data, key, top_level=False):
    """
    Recursively navigate down through the graph from the target. For each new bag, retrieve the number
    of bags inside it (recursive call) and then multiply by the number of this bag in the container.

    Optional arg identifies the top-level call, which is used to remove the top-level container bag,
    which should not be counted.

    :param data: The LUT of bags to contents
    :param key: The bag to search for
    :param offset: Optional flag which is used to reduce the total count by 1, defaults to False.
    :return: The sum of bags contained within the bag identified by `key`
    """
    contains = [c for c in data[key] if c is not None]
    if len(contains) == 0:
        return 1

    sum = 1
    for count, in_key in contains:
        num = find_internal_bags(data, in_key)
        sum += count * num

    offset = -1 if top_level else 0
    return sum + offset


def task_1(data):
    """
    Get the LUT for the graph.

    Then perform a recursive path search through the graph to find the number of bags that can
    contain the target.

    :param data: The full piece of data as a newline delimited string.
    :return: None
    """
    tgt = ("shiny", "gold")

    lut = create_LUT(data)
    path = find_containers(lut, tgt)

    print(f"There are {len(path)} bags that can contain a {' '.join(tgt)} bag.")


def task_2(data):
    """
    Get the LUT for the graph.

    Then perform a recursive search through the graph, accumulating the number of bags contained
    within this one (and its children).

    :param data: The full piece of data as a newline delimited string.
    :return: None
    """
    tgt = ("shiny", "gold")

    lut = create_LUT(data)
    total = find_internal_bags(lut, tgt, True)

    print(f"You'll need {total} bags - good luck!.")


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')

    print("Task 1")
    task_1(input_data)

    print("Task 2")
    task_2(input_data)
