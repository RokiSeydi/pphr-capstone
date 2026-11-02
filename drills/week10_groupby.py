"""Week 10 - Grouping, binning and aggregation.

Exam archetypes:
    Sep 2025 Q11 (10 marks) - cut ages into named bands, then report the
        mean of several columns for each band.
    Jan 2026 Q10 (10 marks) - derive a boolean flag, then compare group means
        with and without it.

pd.cut is the tool the markers are looking for. Watch the boundaries: the
bands in the exam are inclusive on both ends ("35 - 54 years"), so with
integer ages use right=True and set the edges accordingly.
"""
import numpy as np
import pandas as pd

AGE_BANDS = {
    "Young adults": (18, 34),
    "Mid-Life": (35, 54),
    "Late Career": (55, 69),
    "Seniors": (70, 120),
}


def add_age_band(df, age_column="Age", bands=AGE_BANDS):
    """Add an `age_band` categorical column using the bands given.

    Each band is an inclusive (low, high) pair. Ages outside every band
    become NaN. Return a new DataFrame.

    :param df: DataFrame containing the age column
    :param age_column: name of the age column
    :param bands: dict of label -> (low, high), inclusive both ends
    :return: new DataFrame with an `age_band` column
    """
    raise NotImplementedError


def mean_by_age_band(df, value_columns, age_column="Age", bands=AGE_BANDS):
    """Mean of each value column, for each age band.

    Keep the bands in the order given by `bands`, not alphabetical order.

    :param df: DataFrame
    :param value_columns: list of numeric column names to average
    :param age_column: name of the age column
    :param bands: dict of label -> (low, high)
    :return: DataFrame indexed by age band, one column per value column
    """
    raise NotImplementedError


def add_has_ambulance_staff(df, column="ambulance_staff"):
    """Add a boolean `has_ambulance_staff` column.

    True when the staff count is greater than zero. Missing values count
    as no ambulance staff.

    :param df: staffing DataFrame
    :param column: the ambulance staff count column
    :return: new DataFrame with the extra boolean column
    """
    raise NotImplementedError


def count_with_ambulance_staff(df, column="ambulance_staff"):
    """Count organisations that have any ambulance staff.

    :param df: staffing DataFrame
    :param column: the ambulance staff count column
    :return: int
    """
    raise NotImplementedError


def mean_total_staff_by_ambulance_flag(df, staff_columns, column="ambulance_staff"):
    """Compare mean total staff for organisations with and without ambulance staff.

    Total staff is the row-wise sum of `staff_columns`.

    :param df: staffing DataFrame
    :param staff_columns: list of columns that make up the total
    :param column: the ambulance staff count column
    :return: Series indexed by False, True giving the mean total staff
    """
    raise NotImplementedError


def group_proportions(df, group_column, flag_column, flag_value):
    """Proportion of each group whose flag_column equals flag_value.

    This answers "are more women vegans than men?" in one call:
        group_proportions(df, "Gender", "Diet", "Vegan")

    :param df: DataFrame
    :param group_column: column defining the groups
    :param flag_column: column to test
    :param flag_value: the value that counts as a hit
    :return: Series indexed by group giving the proportion, 0-1
    """
    raise NotImplementedError
