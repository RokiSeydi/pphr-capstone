"""Week 5 reference solutions - functions, docstrings and error handling."""
import numbers

import numpy as np


def age_group_counts(ages, n=10):
    # Returns {23: 5, 33: 3, 43: 2, 53: 1, 63: 1} for the paper's first
    # example - the paper prints 33: 4, which is a typo in the paper.
    min_age = int(ages.min())
    max_age = int(ages.max())
    age_groups = {}
    # range stops before max_age, so the oldest age is never a band floor.
    for floor in range(min_age, max_age, n):
        age_groups[floor] = int(np.sum(ages >= floor))
    return age_groups


def mean_systolic_bp(readings):
    # bool is a subclass of int, so exclude it explicitly: True would
    # otherwise be averaged in as 1.
    valid = [
        value for value in readings
        if isinstance(value, numbers.Number) and not isinstance(value, bool)
    ]
    if not valid:
        raise ValueError("no numeric readings to average")
    return float(sum(valid) / len(valid))


def summarise(values, decimals=1):
    array = np.asarray(values, dtype=float)
    return {
        "mean": round(float(np.mean(array)), decimals),
        "median": round(float(np.median(array)), decimals),
        "sd": round(float(np.std(array)), decimals),
    }


def flag_outliers(values, n_sd=2):
    array = np.asarray(values, dtype=float)
    deviation = np.abs(array - array.mean())
    return deviation > n_sd * array.std()


MG_DL_PER_MMOL_L = 18.0182


def convert_glucose(value, to_unit="mmol/L"):
    if to_unit == "mmol/L":
        return round(value / MG_DL_PER_MMOL_L, 1)
    if to_unit == "mg/dL":
        return round(value * MG_DL_PER_MMOL_L, 1)
    raise ValueError(f"to_unit must be 'mmol/L' or 'mg/dL', got {to_unit!r}")


def safe_divide(numerator, denominator, default=None):
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return default
