"""Week 8 - selecting data out of a DataFrame."""
import pandas as pd
import pytest

from tests._target import mod

w = mod("week08_pandas_indexing")


@pytest.fixture
def df():
    return w.referral_source()


def test_referral_source_shape(df):
    assert list(df.columns) == ["org_code", "Total", "GP"]
    assert len(df) == 6


def test_referral_source_values(df):
    assert df.loc[1, "org_code"] == "RBS"
    assert df.loc[1, "Total"] == 821


def test_cell_by_label(df):
    assert w.cell_by_label(df, 1, "Total") == 821


def test_cell_by_position(df):
    assert w.cell_by_position(df, 1, 1) == 821


def test_cell_by_mask(df):
    assert w.cell_by_mask(df, "org_code", "RBS", "Total") == 821


def test_three_methods_agree(df):
    """The exam asks for the same cell three ways - they must all match."""
    assert (
        w.cell_by_label(df, 1, "Total")
        == w.cell_by_position(df, 1, 1)
        == w.cell_by_mask(df, "org_code", "RBS", "Total")
        == 821
    )


def test_cell_by_mask_returns_a_scalar(df):
    result = w.cell_by_mask(df, "org_code", "RBS", "Total")
    assert not isinstance(result, pd.Series), "pull the value out of the Series"


def test_gp_share(df):
    result = w.gp_share(df)
    assert "gp_share" in result.columns
    assert result.loc[0, "gp_share"] == pytest.approx(865 / 1103)


def test_gp_share_does_not_mutate(df):
    w.gp_share(df)
    assert "gp_share" not in df.columns


def test_busiest_organisations(df):
    assert w.busiest_organisations(df, 3) == ["R1H", "RF4", "RTK"]


def test_busiest_organisations_one(df):
    assert w.busiest_organisations(df, 1) == ["R1H"]


def test_cvd_risk_frame():
    frame = w.cvd_risk_frame()
    assert list(frame.index) == ["Vegan", "Vegetarian", "Omnivore"]
    assert list(frame.columns) == ["Women", "Men"]
    assert frame.index.name == "diet"


def test_risk_for():
    frame = w.cvd_risk_frame()
    assert w.risk_for(frame, "Vegan", "Women") == pytest.approx(0.74)
    assert w.risk_for(frame, "Omnivore", "Men") == pytest.approx(1.00)
