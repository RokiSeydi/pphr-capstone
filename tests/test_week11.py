"""Week 11 - merging and cross-tabulating."""
import numpy as np
import pandas as pd
import pytest

from tests._target import mod

w = mod("week11_merge_crosstab")


def test_merge_on_id():
    left = pd.DataFrame({"id": [1, 2, 3], "a": ["x", "y", "z"]})
    right = pd.DataFrame({"id": [2, 3, 4], "b": [20, 30, 40]})
    merged = w.merge_on_id(left, right, "id")
    assert len(merged) == 2
    assert merged["id"].tolist() == [2, 3]


def test_merge_on_id_left_join():
    left = pd.DataFrame({"id": [1, 2], "a": ["x", "y"]})
    right = pd.DataFrame({"id": [2], "b": [20]})
    merged = w.merge_on_id(left, right, "id", how="left")
    assert len(merged) == 2
    assert np.isnan(merged.loc[0, "b"])


def test_merge_on_id_missing_key():
    left = pd.DataFrame({"id": [1]})
    right = pd.DataFrame({"other": [1]})
    with pytest.raises(KeyError):
        w.merge_on_id(left, right, "id")


def test_merge_waiting_and_staffing(waiting, staffing):
    merged = w.merge_waiting_and_staffing(waiting, staffing)
    assert len(merged) == 145
    assert "doctors" in merged.columns
    assert "total_waiting_list" in merged.columns
    assert merged["organisation_code"].is_unique


def test_bin_column_is_left_inclusive():
    series = pd.Series([0, 499, 500, 999])
    result = w.bin_column(series, [0, 500, 1000], ["<500", "500-999"])
    assert result.tolist() == ["<500", "<500", "500-999", "500-999"]


def test_bin_column_out_of_range_is_nan():
    result = w.bin_column(pd.Series([2000]), [0, 500, 1000], ["a", "b"])
    assert result.isna().all()


ROW_EDGES = [0, 500, 1500, 3000, np.inf]
ROW_LABELS = ["0-499", "500-1499", "1500-2999", "3000+"]
COL_EDGES = [0, 250, 750, np.inf]
COL_LABELS = ["<250", "250-749", "750+"]


def test_summary_crosstab_shape(waiting, staffing):
    merged = w.merge_waiting_and_staffing(waiting, staffing)
    table = w.summary_crosstab(
        merged, "over_18_and_up_to_26_weeks", "doctors",
        ROW_EDGES, ROW_LABELS, COL_EDGES, COL_LABELS,
    )
    assert list(table.index) == ROW_LABELS
    assert list(table.columns) == COL_LABELS


def test_summary_crosstab_counts_are_integers(waiting, staffing):
    merged = w.merge_waiting_and_staffing(waiting, staffing)
    table = w.summary_crosstab(
        merged, "over_18_and_up_to_26_weeks", "doctors",
        ROW_EDGES, ROW_LABELS, COL_EDGES, COL_LABELS,
    )
    assert table.to_numpy().dtype.kind in "iu"
    assert (table.to_numpy() >= 0).all()


def test_summary_crosstab_total_matches_binned_rows():
    df = pd.DataFrame({
        "wait": [10, 600, 600, 2000],
        "docs": [100, 100, 500, 900],
    })
    table = w.summary_crosstab(
        df, "wait", "docs", ROW_EDGES, ROW_LABELS, COL_EDGES, COL_LABELS,
    )
    assert table.to_numpy().sum() == 4
    assert table.loc["500-1499", "<250"] == 1
    assert table.loc["500-1499", "250-749"] == 1
    assert table.loc["1500-2999", "750+"] == 1


def test_summary_crosstab_keeps_empty_bands():
    df = pd.DataFrame({"wait": [10], "docs": [100]})
    table = w.summary_crosstab(
        df, "wait", "docs", ROW_EDGES, ROW_LABELS, COL_EDGES, COL_LABELS,
    )
    assert table.shape == (4, 3)
    assert table.loc["3000+", "750+"] == 0


def test_compare_group_proportion(diet, health):
    result = w.compare_group_proportion(
        health, diet, "ID", "Gender", "Diet", "Vegan"
    )
    assert set(result.index) == {"Female", "Male"}
    assert ((result >= 0) & (result <= 1)).all()
