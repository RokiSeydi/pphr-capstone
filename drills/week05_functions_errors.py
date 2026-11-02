"""Week 5 - Functions, docstrings, debugging and error handling.

Exam archetypes:
    Jan 2026 Q5  (5 marks)  - document a working "mystery function".
    Sep 2025 Q7  (5 marks)  - a function raises an error; fix it and improve
        both the docstring and the code.
    Sep 2025 Q9  (10 marks) - write a function from a spec; extra marks are
        explicitly offered for basic error handling.

That last point is worth taking seriously: a bare `try`/`except` around the
risky line, raising a clear message, is cheap and reliably picks up marks.
"""
import numpy as np


def age_group_counts(ages, n=10):
    """Count how many ages fall at or above each band floor.

    This is the Jan 2026 mystery function. Walk from the youngest age to the
    oldest in steps of `n`; for each step, count the ages greater than or
    equal to that floor.

    Example:
        age_group_counts(np.array([23, 45, 31, 35, 67]))
        -> {23: 5, 33: 3, 43: 2, 53: 1, 63: 1}

    (The Jan 2026 paper prints 33: 4 here, but that is a typo in the paper -
    only 45, 35 and 67 are >= 33. Its own starter code returns 3. If the
    stated output and the given code disagree in an exam, say so in a
    comment and go with the code.)

        age_group_counts(np.array([10, 22, 27, 34, 40, 55, 60]), n=15)
        -> {10: 7, 25: 5, 40: 3, 55: 2}

    Note the upper bound: the loop uses range(min, max, n), so the oldest
    age never itself becomes a band floor.

    :param ages: numpy array of integer ages
    :param n: band width in years
    :return: dict mapping band floor -> count of ages at or above it
    """
    raise NotImplementedError


def mean_systolic_bp(readings):
    """Mean of systolic BP readings, ignoring any non-numeric entries.

    This is the broken exam function, repaired. The original did
    `total += reading` over a list containing the strings "error" and
    "corrupted", so it raised TypeError on the first one.

    Requirements:
        - skip values that are not numbers (bools do not count as numbers)
        - return the mean of what remains, as a float
        - raise ValueError, with a message, when nothing numeric is left

    :param readings: list of readings, possibly containing junk values
    :return: mean of the valid readings, as a float
    :raises ValueError: if the list contains no numeric readings
    """
    raise NotImplementedError


def summarise(values, decimals=1):
    """Return mean, median and standard deviation, each rounded.

    Use numpy. Keys must be exactly "mean", "median", "sd".

    :param values: numpy array or list of numbers
    :param decimals: how many decimal places to round to
    :return: dict with keys mean, median, sd
    """
    raise NotImplementedError


def flag_outliers(values, n_sd=2):
    """Return a boolean array marking values more than `n_sd` SDs from the mean.

    :param values: numpy array of numbers
    :param n_sd: how many standard deviations counts as an outlier
    :return: numpy boolean array, same shape as values
    """
    raise NotImplementedError


def convert_glucose(value, to_unit="mmol/L"):
    """Convert blood glucose between mg/dL and mmol/L.

    1 mmol/L = 18.0182 mg/dL. Round the result to 1 decimal place.

    :param value: the numeric reading
    :param to_unit: "mmol/L" (input is mg/dL) or "mg/dL" (input is mmol/L)
    :return: converted value, rounded to 1 dp
    :raises ValueError: if to_unit is neither of the two accepted strings
    """
    raise NotImplementedError


def safe_divide(numerator, denominator, default=None):
    """Divide, returning `default` instead of raising when denominator is 0.

    :param numerator: the number to divide
    :param denominator: the number to divide by
    :param default: what to return when denominator is zero
    :return: the quotient, or `default`
    """
    raise NotImplementedError
