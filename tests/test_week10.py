"""Week 10 - grouping, binning, aggregation."""
import numpy as np
import pandas as pd
import pytest

from tests._target import mod

w = mod("week10_groupby")


def test_add_age_band_labels(health):
    result = w.add_age_band(health)
    assert "age_band" in result.columns
    assert set(result["age_band"].dropna().unique()) <= set(w.AGE_BANDS)


def test_add_age_band_boundaries():
    df = pd.DataFrame({"Age": [18, 34, 35, 54, 55, 69, 70, 95]})
    bands = w.add_age_band(df)["age_band"].tolist()
    assert bands == [
        "Young adults", "Young adults",
        "Mid-Life", "Mid-Life",
        "Late Career", "Late Career",
        "Seniors", "Seniors",
    ]


def test_add_age_band_outside_range_is_nan():
    df = pd.DataFrame({"Age": [5, 200]})
    assert w.add_age_band(df)["age_band"].isna().all()


def test_add_age_band_does_not_mutate(health):
    w.add_age_band(health)
    assert "age_band" not in health.columns


def test_mean_by_age_band_order(health):
    result = w.mean_by_age_band(health, ["Height (cm)", "Weight (kg)"])
    assert list(result.index) == list(w.AGE_BANDS)
    assert list(result.columns) == ["Height (cm)", "Weight (kg)"]


def test_mean_by_age_band_values():
    df = pd.DataFrame({"Age": [20, 30, 40, 50], "x": [1.0, 3.0, 10.0, 20.0]})
    result = w.mean_by_age_band(df, ["x"])
    assert result.loc["Young adults", "x"] == pytest.approx(2.0)
    assert result.loc["Mid-Life", "x"] == pytest.approx(15.0)


def test_mean_by_age_band_exam_columns(health):
    columns = [
        "Height (cm)", "Weight (kg)", "Systolic (mmHg)",
        "Diastolic (mmHg)", "Alcohol Consumption (units/week)",
    ]
    result = w.mean_by_age_band(health, columns)
    assert result.shape == (4, 5)
    assert result.notna().all().all()


def test_add_has_ambulance_staff(staffing):
    result = w.add_has_ambulance_staff(staffing)
    assert result["has_ambulance_staff"].dtype == bool
    expected = (staffing["ambulance_staff"].fillna(0) > 0)
    assert result["has_ambulance_staff"].tolist() == expected.tolist()


def test_add_has_ambulance_staff_treats_missing_as_none():
    df = pd.DataFrame({"ambulance_staff": [0, np.nan, 5]})
    assert w.add_has_ambulance_staff(df)["has_ambulance_staff"].tolist() == [
        False, False, True
    ]


def test_count_with_ambulance_staff(staffing):
    count = w.count_with_ambulance_staff(staffing)
    assert isinstance(count, int)
    assert count == int((staffing["ambulance_staff"].fillna(0) > 0).sum())
    assert 0 < count < len(staffing)


def test_mean_total_staff_by_ambulance_flag(staffing):
    columns = [
        "doctors", "nurses_and_health_visitors", "midwives",
        "ambulance_staff", "managers", "others",
    ]
    result = w.mean_total_staff_by_ambulance_flag(staffing, columns)
    assert list(result.index) == [False, True]
    assert result.notna().all()


def test_mean_total_staff_by_ambulance_flag_values():
    df = pd.DataFrame({
        "ambulance_staff": [0, 0, 10],
        "doctors": [10, 20, 100],
    })
    result = w.mean_total_staff_by_ambulance_flag(df, ["doctors", "ambulance_staff"])
    assert result[False] == pytest.approx(15.0)
    assert result[True] == pytest.approx(110.0)


def test_group_proportions():
    df = pd.DataFrame({
        "Gender": ["Female", "Female", "Female", "Male", "Male"],
        "Diet": ["Vegan", "Vegan", "Omnivore", "Vegan", "Omnivore"],
    })
    result = w.group_proportions(df, "Gender", "Diet", "Vegan")
    assert result["Female"] == pytest.approx(2 / 3)
    assert result["Male"] == pytest.approx(0.5)


def test_group_proportions_on_exam_data(diet, health):
    merged = health.merge(diet, on="ID")
    result = w.group_proportions(merged, "Gender", "Diet", "Vegan")
    assert set(result.index) == {"Female", "Male"}
    assert ((result >= 0) & (result <= 1)).all()
