"""Week 5 - functions, docstrings and error handling."""
import numpy as np
import pytest

from tests._target import mod

w = mod("week05_functions_errors")


def test_age_group_counts_example_one():
    """Note: the Jan 2026 paper prints {23: 5, 33: 4, ...} as the expected
    output here, but that is a typo in the paper. Only three of the five
    ages (45, 35, 67) are >= 33, and the paper's own starter code returns 3.
    Trust the code, not the comment."""
    result = w.age_group_counts(np.array([23, 45, 31, 35, 67]))
    assert result == {23: 5, 33: 3, 43: 2, 53: 1, 63: 1}


def test_age_group_counts_example_two():
    result = w.age_group_counts(np.array([10, 22, 27, 34, 40, 55, 60]), n=15)
    assert result == {10: 7, 25: 5, 40: 3, 55: 2}


def test_age_group_counts_single_age():
    # min == max, so range() is empty and the dict comes back empty too.
    assert w.age_group_counts(np.array([40, 40])) == {}


def test_mean_systolic_bp_skips_junk():
    readings = [95, 92, "error", 102, 105, 99, "corrupted"]
    assert w.mean_systolic_bp(readings) == pytest.approx(98.6)


def test_mean_systolic_bp_returns_float():
    assert isinstance(w.mean_systolic_bp([100, 110]), float)


def test_mean_systolic_bp_excludes_bools():
    # True would sneak in as 1 and wreck the mean.
    assert w.mean_systolic_bp([100, True, 120]) == pytest.approx(110.0)


def test_mean_systolic_bp_raises_when_nothing_numeric():
    with pytest.raises(ValueError):
        w.mean_systolic_bp(["error", "corrupted"])


def test_mean_systolic_bp_raises_on_empty():
    with pytest.raises(ValueError):
        w.mean_systolic_bp([])


def test_summarise():
    result = w.summarise([1, 2, 3, 4])
    assert result == {"mean": 2.5, "median": 2.5, "sd": 1.1}


def test_summarise_respects_decimals():
    assert w.summarise([1, 2, 3, 4], decimals=3)["sd"] == pytest.approx(1.118, abs=1e-3)


def test_flag_outliers():
    values = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 200])
    flags = w.flag_outliers(values)
    assert flags.dtype == bool
    assert flags.tolist() == [False] * 9 + [True]


def test_flag_outliers_none_when_tight():
    assert not w.flag_outliers(np.array([5, 5, 5, 5])).any()


def test_convert_glucose_to_mmol():
    assert w.convert_glucose(126) == pytest.approx(7.0, abs=0.05)


def test_convert_glucose_to_mgdl():
    assert w.convert_glucose(7.0, to_unit="mg/dL") == pytest.approx(126.1, abs=0.05)


def test_convert_glucose_rejects_bad_unit():
    with pytest.raises(ValueError):
        w.convert_glucose(100, to_unit="mmol")


def test_safe_divide():
    assert w.safe_divide(10, 4) == 2.5
    assert w.safe_divide(10, 0) is None
    assert w.safe_divide(10, 0, default=0) == 0
