import mock
import pytest

from day6 import (
    GroupInputParser,
    calculate_sum_counts
)

RAW_INPUT = """abc

a
b
c

ab
ac

a
a
a
a

b
"""


@pytest.mark.parametrize(
    'raw_data, expected_complete',
    [(RAW_INPUT, 6)]
)
def test_input_parser_complete_calls(raw_data, expected_complete):
    parser = GroupInputParser()
    parser_spy = mock.Mock(wraps=parser)

    GroupInputParser.parse(parser_spy, raw_data)
    assert parser_spy._complete_group.call_count == expected_complete


@pytest.mark.parametrize(
    'raw_data, expected_groups',
    [
        (RAW_INPUT, ('abc', 'abc', 'abc', 'a', 'b')),
        ("a\n\n \n\n\nabc\nd\n\ndef", ('a', 'abcd', 'def'))
    ]
)
def test_parser_correct_groupings(raw_data, expected_groups):
    parser = GroupInputParser()
    groups = parser.parse(raw_data)
    assert len(groups) == len(expected_groups)

    for i, e in enumerate(expected_groups):
        assert set(e) == groups[i]


@pytest.mark.parametrize(
    'raw_data, expected_sum',
    [(RAW_INPUT, 11)]
)
def test_integration_sum_groups(raw_data, expected_sum):
    total = calculate_sum_counts(raw_data)
    assert total == expected_sum
