"""Week 9 - Reading files, sorting and describing.

Exam archetypes:
    Jan 2026 Q8 (5 marks)  - load a CSV, show the top 3 rows by a column.
    Sep 2025 Q8 (10 marks) - load a *zipped* CSV and analyse it.

On the zip: pandas reads one straight from the archive with
`pd.read_csv("file.zip")` when the archive holds a single CSV. The exam
forbids shell commands, so unzipping at the terminal would cost marks -
do it in Python, or let pandas do it for you.

Paths are parameters with defaults, never literals buried in the body;
the paper marks reproducibility explicitly.
"""
import zipfile

import pandas as pd

from capstone.paths import STAFFING_CSV, STATINS_ZIP, WAITING_LISTS_CSV


def load_waiting_lists(path=WAITING_LISTS_CSV):
    """Read the NHS waiting-list CSV into a DataFrame.

    :param path: path to nhs_waiting_lists.csv
    :return: DataFrame
    """
    raise NotImplementedError


def load_staffing(path=STAFFING_CSV):
    """Read the NHS staffing CSV into a DataFrame.

    :param path: path to nhs_staffing_info.csv
    :return: DataFrame
    """
    raise NotImplementedError


def load_zipped_csv(path=STATINS_ZIP):
    """Read a CSV that is inside a zip archive, without using the shell.

    :param path: path to the .zip file
    :return: DataFrame
    """
    raise NotImplementedError


def list_zip_contents(path=STATINS_ZIP):
    """List the file names inside a zip archive.

    Useful first step in the exam - you need to know what you have before
    you can read it.

    :param path: path to the .zip file
    :return: list of member names
    """
    raise NotImplementedError


def top_organisations(df, n=3, column="total_waiting_list"):
    """Return the `n` rows with the largest values in `column`.

    Sort descending and keep every column, so the result displays as a
    table in the exam report.

    :param df: waiting-list DataFrame
    :param n: how many rows to return
    :param column: column to rank by
    :return: DataFrame of n rows, largest first
    """
    raise NotImplementedError


def proportion_within_18_weeks(df):
    """Add a `prop_within_18_weeks` column to a copy of the DataFrame.

    It is up_to_18_weeks over total_waiting_list. Guard against division
    by zero - those rows should come out as NaN, not raise.

    :param df: waiting-list DataFrame
    :return: new DataFrame with the extra column
    """
    raise NotImplementedError


def missing_value_report(df):
    """Count missing values per column, keeping only columns that have any.

    :param df: any DataFrame
    :return: Series indexed by column name, sorted descending
    """
    raise NotImplementedError


def prescription_summary(df, bnf_description):
    """Summarise prescribing of one medication across practices.

    Returns how many distinct practices prescribed it and the total
    quantity across all of them. The exam offers extra marks for error
    handling, so validate the input rather than returning an empty result
    silently.

    :param df: the statins DataFrame
    :param bnf_description: one exact BNF_DESCRIPTION value
    :return: dict with keys "bnf_description", "n_practices", "total_quantity"
    :raises ValueError: if `bnf_description` appears nowhere in the data
    """
    raise NotImplementedError
