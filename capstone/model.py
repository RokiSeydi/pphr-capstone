"""Logistic regression for ICU admission.

The synthetic data is generated from a known model - ICU admission really
does depend on NEWS2, lactate, age and consciousness, with the coefficients
in scripts/make_capstone_data.py. So this module is self-checking: if your
fitted coefficients do not land near the true ones, the modelling code is
wrong, not the data. That is a luxury you will never have with real data
and worth exploiting while revising.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm

DEFAULT_PREDICTORS = ["news2_total", "lactate", "age"]

# The data-generating coefficients, for comparison. Keep these in step with
# scripts/make_capstone_data.py if you change the generator.
#
# The intercept needs care. The generator writes the linear predictor with
# age centred on 64:
#
#     -4.0 + 0.185*news2 + 0.44*lactate + 0.021*(age - 64)
#
# fit_icu_model regresses on raw age, so the intercept it estimates is the
# log-odds at age 0, not at age 64. Shifting the parameterisation moves the
# intercept by 0.021 * 64 and leaves every slope alone. Comparing the fitted
# intercept against -4.0 would look like a failure and be nothing of the
# kind - a good illustration of why an intercept is only interpretable once
# you know where the predictors are centred.
AGE_CENTRE = 64
TRUE_COEFFICIENTS = {
    "const": -4.0 - 0.021 * AGE_CENTRE,
    "news2_total": 0.185,
    "lactate": 0.44,
    "age": 0.021,
}


def fit_icu_model(df, predictors=DEFAULT_PREDICTORS, outcome="icu_admission"):
    """Fit a logistic regression for ICU admission.

    Uses GLM with a binomial family, as both past papers specify, and drops
    incomplete rows. Note what that costs: lactate is missing for about one
    attendance in seven, and not at random, so the fitted model describes
    the investigated subgroup rather than the whole cohort. Report the
    number of rows dropped.

    :param df: analysis frame
    :param predictors: list of predictor columns
    :param outcome: the binary outcome column
    :return: fitted statsmodels results object
    """
    model_data = df[[outcome] + list(predictors)].dropna()
    y = model_data[outcome].astype(int)
    X = sm.add_constant(model_data[list(predictors)].astype(float))
    return sm.GLM(y, X, family=sm.families.Binomial()).fit()


def odds_ratio_table(result, alpha=0.05):
    """Odds ratios with confidence intervals and p-values.

    Coefficients from a logistic regression are log-odds, which nobody can
    interpret directly. Exponentiating gives an odds ratio: 1.20 means a
    one-unit rise in the predictor multiplies the odds by 1.2.

    :param result: fitted results object
    :param alpha: significance level for the interval
    :return: DataFrame indexed by predictor
    """
    conf = result.conf_int(alpha=alpha)
    table = pd.DataFrame({
        "coefficient": result.params.round(4),
        "odds_ratio": np.exp(result.params).round(3),
        "ci_lower": np.exp(conf[0]).round(3),
        "ci_upper": np.exp(conf[1]).round(3),
        "p_value": result.pvalues.round(4),
    })
    table["significant"] = table["p_value"] < alpha
    return table


def compare_with_truth(result, truth=TRUE_COEFFICIENTS):
    """Put fitted coefficients next to the ones that generated the data.

    :param result: fitted results object
    :param truth: dict of the true coefficients
    :return: DataFrame with fitted, true, and whether the CI covers the truth
    """
    conf = result.conf_int()
    rows = []
    for name, true_value in truth.items():
        if name not in result.params.index:
            continue
        lower, upper = conf.loc[name, 0], conf.loc[name, 1]
        rows.append({
            "predictor": name,
            "fitted": round(result.params[name], 4),
            "true": true_value,
            "ci_lower": round(lower, 4),
            "ci_upper": round(upper, 4),
            "ci_covers_truth": bool(lower <= true_value <= upper),
        })
    return pd.DataFrame(rows).set_index("predictor")


def model_summary_text(result, df):
    """A few sentences interpreting the fit, as the exam's discussion marks want.

    :param result: fitted results object
    :param df: the frame the model was fitted from
    :return: a string
    """
    table = odds_ratio_table(result)
    dropped = len(df) - int(result.nobs)
    significant = table.drop("const", errors="ignore")
    significant = significant[significant["significant"]]

    lines = [
        f"Fitted on {int(result.nobs)} of {len(df)} attendances "
        f"({dropped} dropped for missing predictors).",
    ]
    if significant.empty:
        lines.append("No predictor reached significance at the 5% level.")
    else:
        for name, row in significant.iterrows():
            direction = "increased" if row["odds_ratio"] > 1 else "decreased"
            lines.append(
                f"Each one-unit rise in {name} {direction} the odds of ICU "
                f"admission by a factor of {row['odds_ratio']:.2f} "
                f"(95% CI {row['ci_lower']:.2f} to {row['ci_upper']:.2f}, "
                f"p = {row['p_value']:.4f})."
            )
    lines.append(
        "These are associations in cross-sectional data, not causal effects: "
        "NEWS2 is measured at triage and ICU admission is a clinical decision "
        "partly informed by the same observations, so the model describes how "
        "the service responded rather than what the physiology caused."
    )
    return " ".join(lines)
