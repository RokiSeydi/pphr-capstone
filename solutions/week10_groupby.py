"""Week 10 reference solutions - grouping, binning, aggregation."""
import numpy as np
import pandas as pd

AGE_BANDS = {
    "Young adults": (18, 34),
    "Mid-Life": (35, 54),
    "Late Career": (55, 69),
    "Seniors": (70, 120),
}


def _band_edges(bands):
    """Turn inclusive (low, high) pairs into pd.cut edges.

    The bands are inclusive at both ends, and pd.cut intervals are
    (left, right]. So the first edge sits just below the first low value
    and each later edge is the band's high value.
    """
    lows = [low for low, _ in bands.values()]
    highs = [high for _, high in bands.values()]
    return [lows[0] - 1] + highs


def add_age_band(df, age_column="Age", bands=AGE_BANDS):
    out = df.copy()
    out["age_band"] = pd.cut(
        out[age_column],
        bins=_band_edges(bands),
        labels=list(bands),
        right=True,
    )
    return out


def mean_by_age_band(df, value_columns, age_column="Age", bands=AGE_BANDS):
    banded = add_age_band(df, age_column=age_column, bands=bands)
    grouped = banded.groupby("age_band", observed=False)[value_columns].mean()
    return grouped.reindex(list(bands))


def add_has_ambulance_staff(df, column="ambulance_staff"):
    out = df.copy()
    out["has_ambulance_staff"] = out[column].fillna(0) > 0
    return out


def count_with_ambulance_staff(df, column="ambulance_staff"):
    return int((df[column].fillna(0) > 0).sum())


def mean_total_staff_by_ambulance_flag(df, staff_columns, column="ambulance_staff"):
    flagged = add_has_ambulance_staff(df, column=column)
    flagged["total_staff"] = flagged[staff_columns].sum(axis=1)
    means = flagged.groupby("has_ambulance_staff")["total_staff"].mean()
    return means.reindex([False, True])


def group_proportions(df, group_column, flag_column, flag_value):
    hit = df[flag_column] == flag_value
    return hit.groupby(df[group_column]).mean()
