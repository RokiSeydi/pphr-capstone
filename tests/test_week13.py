"""Week 13 - derived features and logistic regression."""
import numpy as np
import pandas as pd
import pytest

from tests._target import mod

w = mod("week13_modelling")

STAFF_PREDICTORS = ["doctors", "nurses_and_health_visitors", "managers"]


@pytest.fixture
def modelling_frame(waiting, staffing):
    merged = waiting.merge(staffing, on="organisation_code", how="inner")
    return w.add_one_year_wait(merged)


def test_add_one_year_wait_is_binary(waiting):
    result = w.add_one_year_wait(waiting)
    assert set(result["one_year_wait"].unique()) <= {0, 1}
    assert result["one_year_wait"].dtype.kind in "iu", "statsmodels wants ints"


def test_add_one_year_wait_logic():
    df = pd.DataFrame({
        "over_52_and_up_to_65_weeks": [0, 5, 0, np.nan],
        "over_65_and_up_to_78_weeks": [0, 0, 0, np.nan],
        "over_78_and_up_to_104_weeks": [0, 0, 2, np.nan],
        "over_104_weeks": [0, 0, 0, np.nan],
    })
    assert w.add_one_year_wait(df)["one_year_wait"].tolist() == [0, 1, 1, 0]


def test_add_one_year_wait_does_not_mutate(waiting):
    w.add_one_year_wait(waiting)
    assert "one_year_wait" not in waiting.columns


def test_add_one_year_wait_has_both_classes(waiting):
    counts = w.add_one_year_wait(waiting)["one_year_wait"].value_counts()
    assert counts.get(0, 0) > 0 and counts.get(1, 0) > 0, (
        "a model needs both outcomes present"
    )


def test_fit_logistic_returns_a_fitted_model(modelling_frame):
    result = w.fit_logistic(modelling_frame, "one_year_wait", STAFF_PREDICTORS)
    assert hasattr(result, "params")
    assert hasattr(result, "pvalues")


def test_fit_logistic_includes_an_intercept(modelling_frame):
    result = w.fit_logistic(modelling_frame, "one_year_wait", STAFF_PREDICTORS)
    assert "const" in result.params.index, "use sm.add_constant"
    assert len(result.params) == len(STAFF_PREDICTORS) + 1


def test_fit_logistic_recovers_a_known_association():
    """On data where the outcome really does depend on x, the coefficient
    must come back positive. This is the check that the model is wired up
    the right way round."""
    rng = np.random.default_rng(0)
    x = rng.normal(size=600)
    p = 1 / (1 + np.exp(-(0.4 + 1.8 * x)))
    df = pd.DataFrame({"x": x, "y": (rng.uniform(size=600) < p).astype(int)})
    result = w.fit_logistic(df, "y", ["x"])
    assert result.params["x"] > 1.0
    assert result.pvalues["x"] < 0.001


def test_fit_logistic_drops_missing_rows():
    df = pd.DataFrame({
        "y": [0, 1, 0, 1, 0, 1, 0, 1],
        "x": [1.0, 2.0, np.nan, 4.0, 5.0, 6.0, 7.0, 8.0],
    })
    result = w.fit_logistic(df, "y", ["x"])
    assert int(result.nobs) == 7


def test_odds_ratios_shape(modelling_frame):
    result = w.fit_logistic(modelling_frame, "one_year_wait", STAFF_PREDICTORS)
    table = w.odds_ratios(result)
    assert list(table.columns) == [
        "odds_ratio", "ci_lower", "ci_upper", "p_value"
    ]
    assert (table["odds_ratio"] > 0).all(), "odds ratios are exponentiated"
    assert (table["ci_lower"] <= table["odds_ratio"]).all()
    assert (table["odds_ratio"] <= table["ci_upper"]).all()


def test_significant_predictors_excludes_intercept():
    rng = np.random.default_rng(1)
    x = rng.normal(size=500)
    noise = rng.normal(size=500)
    p = 1 / (1 + np.exp(-(0.2 + 2.0 * x)))
    df = pd.DataFrame({
        "x": x, "noise": noise,
        "y": (rng.uniform(size=500) < p).astype(int),
    })
    result = w.fit_logistic(df, "y", ["x", "noise"])
    significant = w.significant_predictors(result)
    assert "const" not in significant
    assert "x" in significant
    assert "noise" not in significant


def test_add_bmi_converts_centimetres(health):
    result = w.add_bmi(health)
    assert "bmi" in result.columns
    # A plausible adult BMI range - forgetting the cm-to-m step gives ~0.002.
    assert result["bmi"].between(10, 70).all()


def test_add_bmi_known_value():
    df = pd.DataFrame({"Weight (kg)": [70.0], "Height (cm)": [175.0]})
    assert w.add_bmi(df)["bmi"].iloc[0] == pytest.approx(22.9, abs=0.05)


def test_add_pulse_pressure(health):
    result = w.add_pulse_pressure(health)
    assert "pulse_pressure" in result.columns
    expected = health["Systolic (mmHg)"] - health["Diastolic (mmHg)"]
    assert result["pulse_pressure"].tolist() == expected.tolist()


def test_add_pulse_pressure_does_not_mutate(health):
    w.add_pulse_pressure(health)
    assert "pulse_pressure" not in health.columns
