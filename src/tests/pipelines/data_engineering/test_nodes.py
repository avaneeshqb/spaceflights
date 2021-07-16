import math
import pytest
import string
from spaceflights.pipelines.data_engineering.nodes import (
    _is_true,
    _parse_money,
    _parse_percentage,
)


def test__is_true():
    assert _is_true("t")
    all_char = (
        list(string.ascii_lowercase)
        + list(string.ascii_uppercase)
        + list(string.digits)
    )
    char_non_t = [char for char in all_char if char != "t"]
    for char in char_non_t:
        assert not _is_true(char)


def test__parse_percentage():
    assert _parse_percentage("100%") == 1
    assert _parse_percentage("10%") == 0.1
    assert _parse_percentage("35.45%") == pytest.approx(0.3545)
    assert _parse_percentage("35.45") == pytest.approx(0.3545)
    assert math.isnan(_parse_percentage(10))
    with pytest.raises(ValueError):
        _parse_percentage("abs")


def test__parse_money():
    assert _parse_money("1,000") == 1000
    assert _parse_money("1,000$") == 1000
    assert _parse_money("10,000$") == 10000
    with pytest.raises(ValueError):
        _parse_money("abs")
    with pytest.raises(ValueError):
        _parse_money("100%")
