"""Week 12 - matplotlib figures.

Half the marks on a plotting question are for labelling and interpretation,
so these tests check the labels as strictly as the data.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from tests._target import mod

w = mod("week12_plotting")
io = mod("week09_pandas_io")


@pytest.fixture
def prepared(waiting):
    out = waiting.copy()
    out["prop_within_18_weeks"] = (
        out["up_to_18_weeks"] / out["total_waiting_list"].replace(0, np.nan)
    )
    return out


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def test_scatter_returns_axes(prepared):
    ax = w.scatter_waiting_vs_target(prepared)
    assert isinstance(ax, plt.Axes)


def test_scatter_plots_every_point(prepared):
    ax = w.scatter_waiting_vs_target(prepared)
    plotted = sum(c.get_offsets().shape[0] for c in ax.collections)
    assert plotted == len(prepared)


def test_scatter_is_labelled(prepared):
    ax = w.scatter_waiting_vs_target(prepared)
    assert ax.get_xlabel().strip(), "the x axis needs a label"
    assert ax.get_ylabel().strip(), "the y axis needs a label"
    assert ax.get_title().strip(), "the plot needs a title"


def test_scatter_uses_the_right_variables(prepared):
    ax = w.scatter_waiting_vs_target(prepared)
    offsets = np.vstack([c.get_offsets() for c in ax.collections])
    # y is a proportion, x is a count - a swap would be obvious here.
    assert np.nanmax(offsets[:, 1]) <= 1.0
    assert np.nanmax(offsets[:, 0]) > 100


def test_scatter_draws_on_a_given_axes(prepared):
    _, ax = plt.subplots()
    assert w.scatter_waiting_vs_target(prepared, ax=ax) is ax


def test_histogram_is_labelled(prepared):
    ax = w.histogram_of_waiting_lists(prepared)
    assert ax.get_xlabel().strip()
    assert ax.get_ylabel().strip()
    assert ax.get_title().strip()


def test_histogram_bin_count(prepared):
    ax = w.histogram_of_waiting_lists(prepared, bins=12)
    assert len(ax.patches) == 12


def test_histogram_bars_sum_to_n(prepared):
    ax = w.histogram_of_waiting_lists(prepared, bins=20)
    heights = sum(patch.get_height() for patch in ax.patches)
    assert heights == prepared["total_waiting_list"].dropna().shape[0]


def test_bar_mean_by_group(prepared):
    ax = w.bar_mean_by_group(prepared, "organisation_type", "total_waiting_list")
    assert len(ax.patches) == prepared["organisation_type"].nunique()
    assert ax.get_xlabel().strip()
    assert ax.get_ylabel().strip()


def test_bar_mean_by_group_heights():
    df = pd.DataFrame({"g": ["a", "a", "b"], "v": [10.0, 20.0, 100.0]})
    ax = w.bar_mean_by_group(df, "g", "v")
    heights = sorted(patch.get_height() for patch in ax.patches)
    assert heights == pytest.approx([15.0, 100.0])


def test_stacked_wait_bands(prepared):
    codes = prepared["organisation_code"].head(4).tolist()
    ax = w.stacked_wait_bands(prepared, codes)
    assert ax.get_legend() is not None, "a stacked plot needs a legend"
    # One bar per organisation per band.
    assert len(ax.patches) == len(codes) * len(w.WAIT_BANDS)


def test_stacked_wait_bands_totals(prepared):
    codes = prepared["organisation_code"].head(3).tolist()
    ax = w.stacked_wait_bands(prepared, codes)
    drawn = sum(patch.get_height() for patch in ax.patches)
    expected = prepared.loc[
        prepared["organisation_code"].isin(codes), w.WAIT_BANDS
    ].fillna(0).to_numpy().sum()
    assert drawn == pytest.approx(expected)
