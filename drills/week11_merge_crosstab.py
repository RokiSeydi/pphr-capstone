"""Week 11 - Merging tables and cross-tabulating.

Exam archetypes:
    Sep 2025 Q4  (10 marks) - merge two CSVs on an id, then compare a
        proportion between groups.
    Jan 2026 Q11 (15 marks) - merge, bin two columns, and produce a
        counts table with binned rows and binned columns.

Q11 is the single biggest question on the Jan paper. The marks are in the
joining key, the bin edges, and the table shape - build it in those three
steps rather than reaching for one clever call.
"""
import numpy as np
import pandas as pd


def merge_on_id(left, right, key, how="inner"):
    """Merge two DataFrames on a shared key column.

    Check first that the key exists on both sides and raise a clear error
    if not - in the exam the two files sometimes name it differently.

    :param left: first DataFrame
    :param right: second DataFrame
    :param key: the column to join on
    :param how: join type, default "inner"
    :return: merged DataFrame
    :raises KeyError: if `key` is missing from either side
    """
    raise NotImplementedError


def merge_waiting_and_staffing(waiting, staffing):
    """Join the waiting-list and staffing tables.

    Both share `organisation_code`. Use an inner join so every row has
    both waiting-list and staffing figures.

    :param waiting: waiting-list DataFrame
    :param staffing: staffing DataFrame
    :return: merged DataFrame
    """
    raise NotImplementedError


def bin_column(series, edges, labels):
    """Cut a numeric Series into labelled bands.

    Bands are left-inclusive and right-exclusive, so edges [0, 500, 1000]
    with labels ["<500", "500-999"] puts exactly 500 in the second band.

    :param series: numeric Series
    :param edges: list of bin edges, ascending
    :param labels: list of labels, one shorter than edges
    :return: categorical Series of labels
    """
    raise NotImplementedError


def summary_crosstab(df, row_column, column_column, row_edges, row_labels,
                     column_edges, column_labels):
    """Count rows falling into each (row band, column band) pair.

    This builds the Jan 2026 Q11 table: bands of patients waiting 18-26
    weeks down the side, bands of doctor counts across the top, and a count
    of organisations in each cell.

    Every band must appear in the result even when its count is zero.

    :param df: merged DataFrame
    :param row_column: numeric column to band down the rows
    :param column_column: numeric column to band across the columns
    :param row_edges: bin edges for the rows
    :param row_labels: labels for the row bands
    :param column_edges: bin edges for the columns
    :param column_labels: labels for the column bands
    :return: DataFrame of counts, rows and columns in label order
    """
    raise NotImplementedError


def compare_group_proportion(left, right, key, group_column, flag_column, flag_value):
    """Merge two tables, then compare a proportion across groups.

    This answers the Sep 2025 Q4 question - "are more women vegans than
    men?" - end to end.

    :param left: DataFrame with the grouping column
    :param right: DataFrame with the flag column
    :param key: column to merge on
    :param group_column: e.g. "Gender"
    :param flag_column: e.g. "Diet"
    :param flag_value: e.g. "Vegan"
    :return: Series indexed by group giving the proportion with that value
    """
    raise NotImplementedError
