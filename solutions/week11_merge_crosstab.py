"""Week 11 reference solutions - merging and cross-tabulating."""
import numpy as np
import pandas as pd


def merge_on_id(left, right, key, how="inner"):
    missing = [
        side for side, frame in (("left", left), ("right", right))
        if key not in frame.columns
    ]
    if missing:
        raise KeyError(f"{key!r} missing from the {' and '.join(missing)} frame")
    return left.merge(right, on=key, how=how)


def merge_waiting_and_staffing(waiting, staffing):
    return merge_on_id(waiting, staffing, "organisation_code", how="inner")


def bin_column(series, edges, labels):
    # right=False gives left-inclusive bands, so a value equal to an edge
    # falls into the band that starts there.
    return pd.cut(series, bins=edges, labels=labels, right=False)


def summary_crosstab(df, row_column, column_column, row_edges, row_labels,
                     column_edges, column_labels):
    rows = bin_column(df[row_column], row_edges, row_labels)
    columns = bin_column(df[column_column], column_edges, column_labels)
    table = pd.crosstab(rows, columns)
    # Reindex so empty bands still appear, as the exam's table shows them.
    return table.reindex(index=row_labels, columns=column_labels, fill_value=0)


def compare_group_proportion(left, right, key, group_column, flag_column,
                             flag_value):
    merged = merge_on_id(left, right, key, how="inner")
    hit = merged[flag_column] == flag_value
    return hit.groupby(merged[group_column]).mean()
