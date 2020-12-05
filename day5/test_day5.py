import pytest

from day5 import (
    bsp_to_int,
    encode_pass_str,
    coord_to_id,
    parse_pass_to_id
)


@pytest.mark.parametrize(
    'encoding, true_value',
    (
            ([1, 0, 0, 0, 1, 1, 0], 70),
            ([0, 0, 0, 1, 1, 1, 0], 14),
            ([1, 1, 0, 0, 1, 1, 0], 102),
            ([1, 1, 1], 7),
            ([1, 0, 0], 4)
    )
)
def test_bsp_to_int(encoding, true_value):
    val = bsp_to_int(encoding)
    assert val == true_value


@pytest.mark.parametrize(
    'row, col, true_value',
    (
            (70, 7, 567),
            (14, 7, 119),
            (102, 4, 820.)
    )
)
def test_coord_to_id(row, col, true_value):
    val = coord_to_id(row, col)
    assert val == true_value


@pytest.mark.parametrize(
    'boarding_pass, true_row_enc, true_col_enc',
    (
            ("BFFFBBFRRR", [1, 0, 0, 0, 1, 1, 0], [1, 1, 1]),
            ("FFFBBBFRRR", [0, 0, 0, 1, 1, 1, 0], [1, 1, 1]),
            ("BBFFBBFRLL", [1, 1, 0, 0, 1, 1, 0], [1, 0, 0])
    )
)
def test_pass_encoder(boarding_pass, true_row_enc, true_col_enc):
    r, c = encode_pass_str(boarding_pass)
    assert r == true_row_enc
    assert c == true_col_enc


# And now an integration test of the above...


@pytest.mark.parametrize(
    'boarding_pass, expected_id',
    (
            ("BFFFBBFRRR", 567),
            ("FFFBBBFRRR", 119),
            ("BBFFBBFRLL", 820)
    )
)
def test_pass_encoder(boarding_pass, expected_id):
    seat_id = parse_pass_to_id(boarding_pass)
    assert seat_id == expected_id
