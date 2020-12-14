from collections import deque
from copy import deepcopy

import pytest

from day9 import (
    NumberList,
    parse_data,
    task_1,
    task_2
)

EXAMPLE_DATA = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

EXAMPLE_LUT_5 = deque([
    deque([55, 50, 60, 82], maxlen=4),
    deque([55, 35, 45, 67], maxlen=4),
    deque([50, 35, 40, 62], maxlen=4),
    deque([60, 45, 40, 72], maxlen=4),
    deque([82, 67, 62, 72], maxlen=4)
], maxlen=5)


@pytest.fixture
def example_lut_5():
    return deepcopy(EXAMPLE_LUT_5)


@pytest.mark.parametrize(
    "size,expected",
    [
        (2, [[55], [55]]),
        (3, [[55, 50], [55, 35], [50, 35]]),
        (4, [[55, 50, 60], [55, 35, 45], [50, 35, 40], [60, 45, 40]]),
        (5, EXAMPLE_LUT_5),
    ]
)
def test_sum_lut_initialisation(size, expected):
    data = parse_data(EXAMPLE_DATA)
    nn = NumberList(data, size)
    for i, line_num in enumerate(nn.sums):
        for j, sum_val in enumerate(line_num):
            assert expected[i][j] == sum_val


@pytest.mark.parametrize(
    "n, expected",
    [
        (40, [[35, 45, 67, 60], [35, 40, 62, 55], [45, 40, 72, 65], [67, 62, 72, 87], [60, 55, 65, 87]]),
        (47, [[35, 45, 67, 67], [35, 40, 62, 62], [45, 40, 72, 72], [67, 62, 72, 94], [67, 62, 72, 94]])
    ]
)
def test_add_number(example_lut_5, n, expected):
    data = parse_data(EXAMPLE_DATA)
    nn = NumberList(data, 5)
    nn.sums = example_lut_5

    nn._add_number(n)
    for i, line_num in enumerate(nn.sums):
        for j, sum_val in enumerate(line_num):
            assert expected[i][j] == sum_val


@pytest.mark.parametrize(
    "n, expected",
    [
        (35, True),
        (55, True),
        (-1, False),
        (238, False),
        ('a', False),
    ]
)
def test_has_sum(example_lut_5, n, expected):
    data = parse_data(EXAMPLE_DATA)
    nn = NumberList(data, 5)
    nn.sums = example_lut_5
    assert nn._has_sum(n) is expected


@pytest.mark.parametrize(
    "min_num, max_num, x, expected",
    [
        (35, 45, 100, False),
        (35, 45, 20, False),
        (35, 45, 79, True),
        (35, 45, 80, True),
        (35, 45, 81, True),
        (35, 45, 82, True)
    ]
)
def test_is_possible_limits(min_num, max_num, x, expected):
    data = parse_data(EXAMPLE_DATA)
    nn = NumberList(data, 5)
    nn.current_min = min_num
    nn.current_max = max_num
    assert nn._is_possible_with_limits(x) is expected


def test_task1_example_case(capsys):
    example_target = 127
    example_preamble = 5

    tgt = task_1(EXAMPLE_DATA, example_preamble)
    captured = capsys.readouterr()

    assert captured.out.strip() == f"No pair of numbers can sum to {example_target} [numbers too large]"
    assert tgt == example_target


def test_task2_example_case(capsys):
    example_input = 127
    example_target = 62
    output = task_2(EXAMPLE_DATA, example_input)
    assert output == example_target
