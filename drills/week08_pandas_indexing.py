"""Week 4 - Selecting data out of a DataFrame.

Exam archetype: Q4 (5 marks) - return the same cell three different ways.
The marks are for knowing that .loc, .iloc, .at and boolean masks are
distinct tools, so each function here is deliberately restricted to one.
"""
import pandas as pd


def referral_source():
    """Return the starter DataFrame used throughout this week.

    Columns: org_code (str), Total (int), GP (int)
        RCF 1103  865
        RBS  821  394
        RTK 2898 2538
        RF4 4272 2981
        RFF  931  629
        R1H 6154 4121

    :return: pandas DataFrame with a default RangeIndex
    """
    raise NotImplementedError


def cell_by_label(df, row_index, column):
    """Return a single cell using label-based indexing (.loc).

    :param df: DataFrame
    :param row_index: index label of the row
    :param column: column name
    :return: the scalar value in that cell
    """
    raise NotImplementedError


def cell_by_position(df, row_position, column_position):
    """Return a single cell using integer-position indexing (.iloc).

    :param df: DataFrame
    :param row_position: zero-based row number
    :param column_position: zero-based column number
    :return: the scalar value in that cell
    """
    raise NotImplementedError


def cell_by_mask(df, key_column, key_value, value_column):
    """Return a single cell by filtering rows with a boolean mask.

    Build a mask on `key_column`, select `value_column`, then pull the one
    remaining value out as a scalar (not a one-element Series).

    :param df: DataFrame
    :param key_column: column to filter on, e.g. "org_code"
    :param key_value: value to match, e.g. "RBS"
    :param value_column: column to read, e.g. "Total"
    :return: the scalar value
    """
    raise NotImplementedError


def gp_share(df):
    """Add a `gp_share` column: GP referrals as a proportion of Total.

    Return a new DataFrame; do not mutate the input.

    :param df: DataFrame with Total and GP columns
    :return: new DataFrame with the extra column
    """
    raise NotImplementedError


def busiest_organisations(df, n):
    """Return the `n` org_codes with the largest Total, highest first.

    :param df: DataFrame with org_code and Total columns
    :return: list of org_code strings
    """
    raise NotImplementedError


# --- Typing up a table from an image (Sep 2025 Q6, 5 marks) -----------------
# The paper shows a screenshot of a table and asks you to rebuild it as a
# DataFrame, then select one cell from it. Set a meaningful index while you
# build it and the selection becomes a one-liner.

CVD_RISK_TABLE = {
    "Vegan": {"Women": 0.74, "Men": 0.81},
    "Vegetarian": {"Women": 0.82, "Men": 0.88},
    "Omnivore": {"Women": 1.00, "Men": 1.00},
}


def cvd_risk_frame(table=CVD_RISK_TABLE):
    """Build a DataFrame of CVD risk by diet and sex.

    Rows are the diets ("Vegan", "Vegetarian", "Omnivore") in that order,
    columns are "Women" and "Men", and the index is named "diet".

    :param table: nested dict of diet -> {sex: risk}
    :return: DataFrame indexed by diet
    """
    raise NotImplementedError


def risk_for(df, diet, sex):
    """Select one risk value from the table by diet and sex.

    :param df: DataFrame from cvd_risk_frame
    :param diet: row label, e.g. "Vegan"
    :param sex: column label, e.g. "Women"
    :return: the scalar risk value
    """
    raise NotImplementedError
