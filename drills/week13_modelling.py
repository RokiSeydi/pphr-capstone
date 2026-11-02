"""Week 13 - Derived features and logistic regression.

Exam archetypes:
    Jan 2026 Q12 (15 marks) - build a binary outcome, fit a logistic
        regression with statsmodels, and discuss the results.
    Sep 2025 Q12 (15 marks) - derive a clinically meaningful new feature,
        plot it against two other variables, and justify it.

The exam asks for `sm.GLM(..., family=sm.families.Binomial())`, not
`sm.Logit`. Both fit a logistic regression; use the one the paper names.
Remember `sm.add_constant` - without the intercept the coefficients are
wrong and the discussion marks go with them.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm

LONG_WAIT_COLUMNS = [
    "over_52_and_up_to_65_weeks",
    "over_65_and_up_to_78_weeks",
    "over_78_and_up_to_104_weeks",
    "over_104_weeks",
]


def add_one_year_wait(df, columns=LONG_WAIT_COLUMNS):
    """Add a binary `one_year_wait` column.

    It is 1 when the organisation has anyone waiting more than 52 weeks -
    that is, when the sum across `columns` is greater than zero - and 0
    otherwise. Missing values count as zero.

    Return ints, not bools: statsmodels wants a numeric endogenous variable.

    :param df: waiting-list DataFrame
    :param columns: the over-52-week band columns
    :return: new DataFrame with the extra column
    """
    raise NotImplementedError


def fit_logistic(df, outcome, predictors):
    """Fit a logistic regression with statsmodels GLM.

    Steps:
        1. Drop rows with missing values in the outcome or any predictor.
        2. Add an intercept with sm.add_constant.
        3. Fit sm.GLM(y, X, family=sm.families.Binomial()).

    :param df: DataFrame holding outcome and predictors
    :param outcome: name of the binary outcome column
    :param predictors: list of predictor column names
    :return: the fitted statsmodels results object
    """
    raise NotImplementedError


def odds_ratios(result, alpha=0.05):
    """Turn a fitted result into a readable odds-ratio table.

    Exponentiate the coefficients and the confidence-interval bounds.

    :param result: fitted statsmodels results object
    :param alpha: significance level for the confidence interval
    :return: DataFrame indexed by predictor with columns
             odds_ratio, ci_lower, ci_upper, p_value
    """
    raise NotImplementedError


def significant_predictors(result, alpha=0.05):
    """List the predictors significant at `alpha`, excluding the intercept.

    :param result: fitted statsmodels results object
    :param alpha: significance threshold
    :return: list of predictor names, most significant first
    """
    raise NotImplementedError


def add_bmi(df, weight_column="Weight (kg)", height_column="Height (cm)"):
    """Add a `bmi` column: weight in kg over height in metres squared.

    The height column is in centimetres, so convert it first - this is the
    trap in the derived-feature question.

    :param df: DataFrame with weight and height columns
    :param weight_column: name of the weight column (kg)
    :param height_column: name of the height column (cm)
    :return: new DataFrame with a `bmi` column, rounded to 1 dp
    """
    raise NotImplementedError


def add_pulse_pressure(df, systolic="Systolic (mmHg)", diastolic="Diastolic (mmHg)"):
    """Add a `pulse_pressure` column: systolic minus diastolic.

    A good answer to "derive a clinically meaningful feature" - a wide
    pulse pressure is associated with arterial stiffness and cardiovascular
    risk, so it is defensible in the discussion as well as easy to compute.

    :param df: DataFrame with blood pressure columns
    :param systolic: name of the systolic column
    :param diastolic: name of the diastolic column
    :return: new DataFrame with a `pulse_pressure` column
    """
    raise NotImplementedError
