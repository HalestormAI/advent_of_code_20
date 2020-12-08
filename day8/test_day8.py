import pytest

from day8 import (
    HandHeld,
    Task2HandHeld,
    InstructionAlreadyRunException
)

EXAMPLE_DATA = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


def test_instruction_parser():
    hh = HandHeld()
    assert len(hh.instructions) == 0

    hh.parse_instructions(EXAMPLE_DATA)
    assert len(hh.instructions) == 9

    def test_input(actual, expected):
        actual_fn, actual_arg = actual
        expected_fn, expected_arg = expected
        assert actual_fn == expected_fn
        assert actual_arg == expected_arg

    expected = [
        (hh.nop, 0),
        (hh.acc, 1),
        (hh.jmp, 4),
        (hh.acc, 3),
        (hh.jmp, -3),
        (hh.acc, -99),
        (hh.acc, 1),
        (hh.jmp, -4),
        (hh.acc, 6),
    ]

    for i, instruction in enumerate(hh.instructions):
        test_input(instruction, expected[i])


def test_instruction_reuse_exception():
    hh = HandHeld()
    hh.parse_instructions(EXAMPLE_DATA)

    with pytest.raises(InstructionAlreadyRunException) as excinfo:
        hh.startup()
        assert excinfo.value.accumulator_value == 5


def test_instruction_reuse_safe():
    hh = Task2HandHeld()
    hh.parse_instructions(EXAMPLE_DATA)
    hh.startup()

    assert hh.accumulator == 8
