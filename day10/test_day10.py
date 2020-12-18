import pathlib
import sys

import pytest

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils

from day10 import (
    get_difference_frequency,
    InvalidJoltageException
)

SHORT_EXAMPLE_INPUT = """16
10
15
5
1
11
7
19
6
12
4"""

LONG_EXAMPLE_INPUT = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""


@pytest.mark.parametrize(
    "raw_data, expected_freq_1, expected_freq_3",
    [
        (SHORT_EXAMPLE_INPUT, 7, 5),
        (LONG_EXAMPLE_INPUT, 22, 10)
    ]
)
def test_get_diff_freq(raw_data, expected_freq_1, expected_freq_3):
    data = list(utils.parse_int_data(raw_data))
    freq = get_difference_frequency(data)
    assert freq[1] == expected_freq_1
    assert freq[3] == expected_freq_3


@pytest.mark.parametrize(
    "data",
    [
        [1, 5, 6, 8],
        [5, 6, 6, 8],
        [1, 1, 6, 8]

    ]
)
def test_get_diff_freq_invalid(data):
    with pytest.raises(InvalidJoltageException):
        get_difference_frequency(data)
