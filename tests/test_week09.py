"""Week 9 - reading files, sorting, describing."""
import numpy as np
import pandas as pd
import pytest

from tests._target import mod

w = mod("week09_pandas_io")


def test_load_waiting_lists():
    df = w.load_waiting_lists()
    assert len(df) == 145
    assert "total_waiting_list" in df.columns
    assert "organisation_code" in df.columns


def test_load_staffing():
    df = w.load_staffing()
    assert len(df) == 145
    assert "doctors" in df.columns


def test_list_zip_contents():
    members = w.list_zip_contents()
    assert any(name.lower().endswith(".csv") for name in members)


def test_load_zipped_csv():
    df = w.load_zipped_csv()
    assert len(df) > 0
    assert "PRACTICE_CODE" in df.columns
    assert "BNF_DESCRIPTION" in df.columns


def test_top_organisations(waiting):
    top = w.top_organisations(waiting, n=3)
    assert len(top) == 3
    values = top["total_waiting_list"].tolist()
    assert values == sorted(values, reverse=True)
    assert values[0] == waiting["total_waiting_list"].max()


def test_top_organisations_keeps_all_columns(waiting):
    assert list(w.top_organisations(waiting, n=3).columns) == list(waiting.columns)


def test_top_organisations_other_column(waiting):
    top = w.top_organisations(waiting, n=5, column="up_to_18_weeks")
    assert top["up_to_18_weeks"].iloc[0] == waiting["up_to_18_weeks"].max()


def test_proportion_within_18_weeks(waiting):
    result = w.proportion_within_18_weeks(waiting)
    assert "prop_within_18_weeks" in result.columns
    valid = result["prop_within_18_weeks"].dropna()
    assert ((valid >= 0) & (valid <= 1)).all()


def test_proportion_within_18_weeks_handles_zero_total():
    df = pd.DataFrame({"total_waiting_list": [0, 100], "up_to_18_weeks": [0, 90]})
    result = w.proportion_within_18_weeks(df)
    assert np.isnan(result["prop_within_18_weeks"].iloc[0])
    assert result["prop_within_18_weeks"].iloc[1] == pytest.approx(0.9)


def test_proportion_does_not_mutate(waiting):
    before = list(waiting.columns)
    w.proportion_within_18_weeks(waiting)
    assert list(waiting.columns) == before


def test_missing_value_report():
    df = pd.DataFrame({"a": [1, None, 3], "b": [1, 2, 3], "c": [None, None, 1]})
    report = w.missing_value_report(df)
    assert "b" not in report.index
    assert report.index.tolist() == ["c", "a"]
    assert report["c"] == 2


def test_prescription_summary(statins):
    description = statins["BNF_DESCRIPTION"].iloc[0]
    result = w.prescription_summary(statins, description)
    assert result["bnf_description"] == description
    assert result["n_practices"] >= 1
    assert result["total_quantity"] > 0


def test_prescription_summary_rejects_unknown(statins):
    with pytest.raises(ValueError):
        w.prescription_summary(statins, "Not A Real Medicine 500mg")


def test_prescription_summary_rejects_empty(statins):
    with pytest.raises(ValueError):
        w.prescription_summary(statins, "")
