import pytest

from day7 import (
    extract_count_and_tag,
    naive_parser,
    find_containers,
    find_internal_bags
)

EXAMPLE_DATA = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

EXAMPLE_DATA_TASK_2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""


@pytest.mark.parametrize(
    "line, expected_count, expected_tag, expected_none",
    [
        ("light red bags", None, ("light", "red"), False),
        ("dark orange bags", None, ("dark", "orange"), False),
        ("bright white bags", None, ("bright", "white"), False),
        ("muted yellow bags", None, ("muted", "yellow"), False),
        ("shiny gold bags", None, ("shiny", "gold"), False),
        ("dark olive bags", None, ("dark", "olive"), False),
        ("vibrant plum bags", None, ("vibrant", "plum"), False),
        ("faded blue bags", None, ("faded", "blue"), False),
        ("dotted black bag", None, ("dotted", "black"), False),
        ("3 bright white bags", 3, ("bright", "white"), False),
        ("1 shiny gold bag.", 1, ("shiny", "gold"), False),
        ("2 shiny gold bags", 2, ("shiny", "gold"), False),
        ("1 dark olive bag,", 1, ("dark", "olive"), False),
        ("3 faded blue bags", 3, ("faded", "blue"), False),
        ("5 faded blue bags", 5, ("faded", "blue"), False),
        ("1 bright white bag", 1, ("bright", "white"), False),
        ("2 muted yellow bags", 2, ("muted", "yellow"), False),
        ("4 muted yellow bags.", 4, ("muted", "yellow"), False),
        ("9 faded blue bags.", 9, ("faded", "blue"), False),
        ("2 vibrant plum bags.", 2, ("vibrant", "plum"), False),
        ("4 dotted black bags.", 4, ("dotted", "black"), False),
        ("6 dotted black bags.", 6, ("dotted", "black"), False),
        ("no other bags.", None, None, True),
        ("Oh Christmas Tree, Oh Christmas tree, look at all these bags.", None, None, True)
    ]
)
def test_extract_count_and_tag(line, expected_count, expected_tag, expected_none):
    output = extract_count_and_tag(line)

    if expected_none:
        assert output is None
    else:
        assert output[0] == expected_count
        assert output[1] == expected_tag


@pytest.mark.parametrize(
    "line, expected_outermost_tag, expected_contents",
    [
        (
                "light red bags contain 1 bright white bag, 2 muted yellow bags.",
                ("light", "red"),
                [(1, ("bright", "white")), (2, ("muted", "yellow"))]
        ),
        (
                "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
                ("dark", "orange"),
                [(3, ("bright", "white")), (4, ("muted", "yellow"))]
        ),
        (
                "bright white bags contain 1 shiny gold bag.",
                ("bright", "white"),
                [(1, ("shiny", "gold"))]
        ),
        (
                "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
                ("muted", "yellow"),
                [(2, ("shiny", "gold")), (9, ("faded", "blue"))]),
        (
                "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
                ("shiny", "gold"),
                [(1, ("dark", "olive")), (2, ("vibrant", "plum"))]),
        (
                "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
                ("dark", "olive"),
                [(3, ("faded", "blue")), (4, ("dotted", "black"))]),
        (
                "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
                ("vibrant", "plum"),
                [(5, ("faded", "blue")), (6, ("dotted", "black"))]),
        (
                "faded blue bags contain no other bags.",
                ("faded", "blue"),
                [None]
        ),
        (
                "dotted black bags contain no other bags",
                ("dotted", "black"),
                [None]
        )
    ]
)
def test_naive_parser(line, expected_outermost_tag, expected_contents):
    outermost_tag, contents = naive_parser(line)

    assert outermost_tag == expected_outermost_tag
    assert contents == expected_contents


def test_find_container_set_example():
    tgt = ("shiny", "gold")

    edges = dict(naive_parser(line) for line in EXAMPLE_DATA.split("\n") if line.strip() != "")
    path = find_containers(edges, tgt)
    assert len(path) == 4


@pytest.mark.parametrize(
    "data, expected",
    [
        (EXAMPLE_DATA, 32),
        (EXAMPLE_DATA_TASK_2, 126)
    ]
)
def test_find_internal_bags_example(data, expected):
    tgt = ("shiny", "gold")

    edges = dict(naive_parser(line) for line in data.split("\n") if line.strip() != "")
    assert find_internal_bags(edges, tgt, -1) == expected
