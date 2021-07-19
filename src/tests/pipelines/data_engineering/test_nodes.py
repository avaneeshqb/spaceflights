import math
import pandas as pd
import pytest
import string
from spaceflights.pipelines.data_engineering.nodes import (
    _is_true,
    _parse_money,
    _parse_percentage,
    preprocess_companies,
    preprocess_shuttles,
)


@pytest.mark.parametrize(
    "char_non_t", [char for char in list(string.printable) if char != "t"]
)
def test__is_true_non_t(char_non_t):
    assert not _is_true(char_non_t)


def test__is_true():
    assert _is_true("t")


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


@pytest.fixture()
def companies_raw():
    df = pd.DataFrame(
        {
            "iata_approved": ["t", "f", "t", "g"],
            "company_rating": ["100%", "30%", "10%", "80"],
        }
    )
    return df


def test_preprocess_companies(companies_raw):
    output = preprocess_companies(companies_raw)
    expected = pd.DataFrame(
        {
            "iata_approved": [True, False, True, False],
            "company_rating": [1, 0.3, 0.1, 0.8],
        }
    )
    pd.testing.assert_frame_equal(output, expected)


@pytest.fixture()
def shuttles_raw():
    df = pd.DataFrame(
        {
            "d_check_complete": ["t", "f", "t", "t"],
            "moon_clearance_complete": ["f", "f", "t", "t"],
            "price": ["$1345.0", "$1,650.0", "$6,720.0", "$1,351.0"],
        }
    )
    return df


def test_preprocess_shuttles(shuttles_raw):
    output = preprocess_shuttles(shuttles_raw)
    expected = pd.DataFrame(
        {
            "d_check_complete": [True, False, True, True],
            "moon_clearance_complete": [False, False, True, True],
            "price": [1345.0, 1650.0, 6720.0, 1351.0],
        }
    )
    pd.testing.assert_frame_equal(output, expected)
