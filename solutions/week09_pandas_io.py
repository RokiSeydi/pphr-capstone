"""Week 9 reference solutions - reading files, sorting, describing."""
import zipfile

import numpy as np
import pandas as pd

from capstone.paths import STAFFING_CSV, STATINS_ZIP, WAITING_LISTS_CSV


def load_waiting_lists(path=WAITING_LISTS_CSV):
    return pd.read_csv(path)


def load_staffing(path=STAFFING_CSV):
    return pd.read_csv(path)


def load_zipped_csv(path=STATINS_ZIP):
    # pandas handles a single-member archive directly - no shell needed.
    return pd.read_csv(path, compression="zip", low_memory=False)


def list_zip_contents(path=STATINS_ZIP):
    with zipfile.ZipFile(path) as archive:
        return archive.namelist()


def top_organisations(df, n=3, column="total_waiting_list"):
    return df.sort_values(column, ascending=False).head(n)


def proportion_within_18_weeks(df):
    out = df.copy()
    # Replace 0 with NaN first so the division yields NaN, not inf.
    out["prop_within_18_weeks"] = (
        out["up_to_18_weeks"] / out["total_waiting_list"].replace(0, np.nan)
    )
    return out


def missing_value_report(df):
    counts = df.isna().sum()
    return counts[counts > 0].sort_values(ascending=False)


def prescription_summary(df, bnf_description):
    if not isinstance(bnf_description, str) or not bnf_description.strip():
        raise ValueError("bnf_description must be a non-empty string")

    column = "BNF_DESCRIPTION"
    if column not in df.columns:
        raise ValueError(f"expected a {column!r} column, got {list(df.columns)}")

    subset = df[df[column] == bnf_description]
    if subset.empty:
        raise ValueError(f"{bnf_description!r} does not appear in the data")

    return {
        "bnf_description": bnf_description,
        "n_practices": int(subset["PRACTICE_CODE"].nunique()),
        "total_quantity": float(subset["QUANTITY"].sum()),
    }
