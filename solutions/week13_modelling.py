"""Week 13 reference solutions - derived features and logistic regression."""
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
    out = df.copy()
    over_a_year = out[columns].fillna(0).sum(axis=1)
    # Cast to int: statsmodels wants a numeric endog, not a bool.
    out["one_year_wait"] = (over_a_year > 0).astype(int)
    return out


def fit_logistic(df, outcome, predictors):
    model_data = df[[outcome] + list(predictors)].dropna()
    y = model_data[outcome]
    X = sm.add_constant(model_data[list(predictors)])
    return sm.GLM(y, X, family=sm.families.Binomial()).fit()


def odds_ratios(result, alpha=0.05):
    conf = result.conf_int(alpha=alpha)
    table = pd.DataFrame({
        "odds_ratio": np.exp(result.params),
        "ci_lower": np.exp(conf[0]),
        "ci_upper": np.exp(conf[1]),
        "p_value": result.pvalues,
    })
    return table


def significant_predictors(result, alpha=0.05):
    pvalues = result.pvalues.drop("const", errors="ignore")
    return pvalues[pvalues < alpha].sort_values().index.tolist()


def add_bmi(df, weight_column="Weight (kg)", height_column="Height (cm)"):
    out = df.copy()
    height_m = out[height_column] / 100  # the column is centimetres
    out["bmi"] = (out[weight_column] / height_m ** 2).round(1)
    return out


def add_pulse_pressure(df, systolic="Systolic (mmHg)",
                       diastolic="Diastolic (mmHg)"):
    out = df.copy()
    out["pulse_pressure"] = out[systolic] - out[diastolic]
    return out
