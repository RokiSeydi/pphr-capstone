"""Capstone regression tests.

These do not test your drill answers - they guard the capstone package, so
you notice if a change to the feature code quietly breaks the analysis.
Unlike the drills, these should be green from day one.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from capstone import analysis, data, features, model


@pytest.fixture(scope="module")
def frame():
    return features.build_analysis_frame(data.load_all())


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


# --- joining ---------------------------------------------------------------

def test_load_all_is_one_row_per_attendance():
    merged = data.load_all()
    assert merged["attendance_id"].is_unique
    assert len(merged) == len(data.load_attendances())


def test_load_all_keeps_rows_with_missing_labs():
    merged = data.load_all()
    assert merged["lactate"].isna().any(), (
        "a left join should preserve attendances with no bloods"
    )


def test_hospital_lookup_resolves():
    merged = data.load_all()
    assert merged["hospital_name"].notna().all()


# --- NEWS2 -----------------------------------------------------------------

@pytest.mark.parametrize("rate,score", [
    (6, 3), (8, 3), (9, 1), (11, 1), (12, 0), (20, 0), (21, 2), (24, 2), (25, 3),
])
def test_score_respiratory_rate(rate, score):
    assert features.score_respiratory_rate(rate) == score


@pytest.mark.parametrize("spo2,score", [(90, 3), (91, 3), (92, 2), (93, 2),
                                        (94, 1), (95, 1), (96, 0), (100, 0)])
def test_score_spo2(spo2, score):
    assert features.score_spo2(spo2) == score


@pytest.mark.parametrize("systolic,score", [(80, 3), (90, 3), (95, 2), (100, 2),
                                            (105, 1), (110, 1), (120, 0),
                                            (219, 0), (230, 3)])
def test_score_systolic_bp(systolic, score):
    assert features.score_systolic_bp(systolic) == score


def test_score_consciousness():
    assert features.score_consciousness("Alert") == 0
    assert features.score_consciousness("Confusion") == 3


def test_news2_total_is_the_sum_of_its_parts(frame):
    parts = ["news2_resp", "news2_spo2", "news2_temp", "news2_systolic",
             "news2_pulse", "news2_consciousness"]
    assert (frame[parts].sum(axis=1) == frame["news2_total"]).all()


def test_news2_total_in_range(frame):
    assert frame["news2_total"].between(0, 18).all()


def test_news2_known_patient():
    """A fully normal set of observations must score zero."""
    df = pd.DataFrame([{
        "respiratory_rate": 16, "spo2": 98, "temperature": 37.0,
        "systolic_bp": 120, "diastolic_bp": 75, "heart_rate": 70,
        "consciousness": "Alert",
    }])
    assert features.add_news2(df)["news2_total"].iloc[0] == 0


def test_news2_septic_patient():
    """Tachypnoea 3, hypoxia 2, pyrexia 1, hypotension 3, tachycardia 2,
    confusion 3 - total 14."""
    df = pd.DataFrame([{
        "respiratory_rate": 28, "spo2": 92, "temperature": 38.5,
        "systolic_bp": 88, "diastolic_bp": 55, "heart_rate": 125,
        "consciousness": "Confusion",
    }])
    result = features.add_news2(df)
    assert result["news2_total"].iloc[0] == 14
    assert bool(result["news2_red_score"].iloc[0]) is True


@pytest.mark.parametrize("total,red,band", [
    (0, False, "low"), (1, False, "low-medium"), (4, False, "low-medium"),
    (5, False, "medium"), (6, False, "medium"), (7, False, "high"),
    (12, False, "high"),
    # A single parameter scoring 3 escalates regardless of the total.
    (3, True, "medium"),
])
def test_news2_risk_band(total, red, band):
    assert features.news2_risk_band(total, red) == band


def test_news2_band_present(frame):
    assert set(frame["news2_band"]) <= set(analysis.BAND_ORDER)
    assert frame["escalation"].notna().all()


# --- timings ---------------------------------------------------------------

def test_time_to_antibiotics_is_positive(frame):
    minutes = frame["minutes_to_antibiotics"].dropna()
    assert (minutes > 0).all(), "antibiotics cannot precede arrival"


def test_untreated_patients_have_no_time(frame):
    untreated = frame[~frame["antibiotics_given"]]
    assert untreated["minutes_to_antibiotics"].isna().all()
    assert not untreated["antibiotics_within_hour"].any(), (
        "never treated must not count as treated within the hour"
    )


def test_within_hour_matches_minutes(frame):
    treated = frame[frame["antibiotics_given"]]
    expected = treated["minutes_to_antibiotics"] <= 60
    assert treated["antibiotics_within_hour"].tolist() == expected.tolist()


# --- summary tables --------------------------------------------------------

def test_outcomes_by_news2_band_is_ordered(frame):
    table = analysis.outcomes_by_news2_band(frame)
    assert list(table.index) == analysis.BAND_ORDER
    assert table["n"].sum() == len(frame)


def test_icu_rate_rises_with_news2_band(frame):
    """The headline finding: if this stops holding, something is wrong with
    either the score or the join."""
    rates = analysis.outcomes_by_news2_band(frame)["icu_rate"]
    assert rates["high"] > rates["medium"] > rates["low-medium"]


def test_crosstab_totals(frame):
    table = analysis.news2_by_outcome_crosstab(frame)
    assert table.to_numpy().sum() == len(frame)
    assert list(table.columns) == ["Not admitted to ICU", "Admitted to ICU"]


def test_antibiotics_audit_denominators(frame):
    table = analysis.antibiotics_audit(frame)
    assert table["n"].sum() == len(frame)
    # Of-treated can only be the kinder number of the two.
    valid = table.dropna(subset=["within_hour_of_treated"])
    assert (valid["within_hour_of_treated"] >= valid["within_hour_of_all"]).all()


def test_hospital_variation_covers_every_hospital(frame):
    table = analysis.hospital_variation(frame)
    assert len(table) == frame["hospital_id"].nunique()
    assert table["attendances"].sum() == len(frame)


def test_missingness_is_not_at_random(frame):
    """Bloods are skipped more often for patients triaged as less unwell, so
    a complete-case analysis drops a non-random slice of the cohort."""
    table = analysis.missingness_by_triage(frame)
    least_unwell = table.loc["Non-urgent", "lactate_missing_pct"]
    most_unwell = table.loc["Very urgent", "lactate_missing_pct"]
    assert least_unwell > most_unwell


# --- model -----------------------------------------------------------------

def test_fit_icu_model_has_intercept(frame):
    result = model.fit_icu_model(frame)
    assert "const" in result.params.index


def test_fit_icu_model_recovers_true_coefficients(frame):
    """The data was generated from a known model, so the fitted confidence
    intervals should cover the true coefficients. This is the check that the
    whole pipeline - join, score, model - is wired up correctly."""
    result = model.fit_icu_model(frame)
    comparison = model.compare_with_truth(result)
    assert comparison["ci_covers_truth"].all(), (
        f"coefficients not recovered:\n{comparison}"
    )


def test_news2_is_a_significant_predictor(frame):
    result = model.fit_icu_model(frame)
    table = model.odds_ratio_table(result)
    assert table.loc["news2_total", "significant"]
    assert table.loc["news2_total", "odds_ratio"] > 1


def test_odds_ratio_table_intervals_bracket_the_estimate(frame):
    table = model.odds_ratio_table(model.fit_icu_model(frame))
    assert (table["ci_lower"] <= table["odds_ratio"]).all()
    assert (table["odds_ratio"] <= table["ci_upper"]).all()


def test_model_summary_text_reports_rows_dropped(frame):
    text = model.model_summary_text(model.fit_icu_model(frame), frame)
    assert "dropped" in text
    assert str(len(frame)) in text


# --- figures ---------------------------------------------------------------

def test_every_figure_is_labelled(frame):
    from capstone import plots
    table = analysis.outcomes_by_news2_band(frame)
    axes = [
        plots.plot_icu_rate_by_news2_band(table),
        plots.plot_news2_distribution(frame),
        plots.plot_time_to_antibiotics(frame),
        plots.plot_lactate_vs_news2(frame),
        plots.plot_hospital_variation(analysis.hospital_variation(frame)),
    ]
    for ax in axes:
        assert isinstance(ax, plt.Axes)
        assert ax.get_xlabel().strip()
        assert ax.get_ylabel().strip()
        assert ax.get_title().strip()
