"""Derived features: NEWS2, time to antibiotics, and clinical bands.

NEWS2 is the National Early Warning Score 2 - the score UK hospitals
actually use to spot deteriorating patients. Each vital sign contributes
0-3 points and the total drives the escalation response. Building it here
is the same skill as Week 3's decision tree, applied to a real instrument,
and it gives the modelling week a predictor worth regressing on.

The thresholds below follow the published RCP NEWS2 chart, with one
simplification: the oxygen scale for patients with hypercapnic respiratory
failure (Scale 2) is not implemented, and supplemental oxygen contributes
no points because the synthetic data does not record it. Say so in writing
if you report this - stating a simplification is worth more than hoping
nobody checks.
"""
import numpy as np
import pandas as pd

ESCALATION = {
    "low": "Ward-based response, routine monitoring",
    "low-medium": "Registered nurse review",
    "medium": "Urgent review by a clinician with acute competencies",
    "high": "Emergency assessment by a critical care team",
}


def score_respiratory_rate(rate):
    """NEWS2 points for respiratory rate (breaths/min)."""
    if rate <= 8:
        return 3
    if rate <= 11:
        return 1
    if rate <= 20:
        return 0
    if rate <= 24:
        return 2
    return 3


def score_spo2(spo2):
    """NEWS2 points for oxygen saturation, Scale 1 (percent)."""
    if spo2 <= 91:
        return 3
    if spo2 <= 93:
        return 2
    if spo2 <= 95:
        return 1
    return 0


def score_temperature(temperature):
    """NEWS2 points for temperature (degrees Celsius)."""
    if temperature <= 35.0:
        return 3
    if temperature <= 36.0:
        return 1
    if temperature <= 38.0:
        return 0
    if temperature <= 39.0:
        return 1
    return 2


def score_systolic_bp(systolic):
    """NEWS2 points for systolic blood pressure (mmHg)."""
    if systolic <= 90:
        return 3
    if systolic <= 100:
        return 2
    if systolic <= 110:
        return 1
    if systolic <= 219:
        return 0
    return 3


def score_heart_rate(rate):
    """NEWS2 points for heart rate (beats/min)."""
    if rate <= 40:
        return 3
    if rate <= 50:
        return 1
    if rate <= 90:
        return 0
    if rate <= 110:
        return 1
    if rate <= 130:
        return 2
    return 3


def score_consciousness(level):
    """NEWS2 points for level of consciousness - 3 unless fully alert."""
    return 0 if level == "Alert" else 3


def add_news2(df):
    """Add the six NEWS2 sub-scores and their total.

    :param df: DataFrame with the triage vital-sign columns
    :return: new DataFrame with news2_* columns and news2_total
    """
    out = df.copy()
    components = {
        "news2_resp": ("respiratory_rate", score_respiratory_rate),
        "news2_spo2": ("spo2", score_spo2),
        "news2_temp": ("temperature", score_temperature),
        "news2_systolic": ("systolic_bp", score_systolic_bp),
        "news2_pulse": ("heart_rate", score_heart_rate),
        "news2_consciousness": ("consciousness", score_consciousness),
    }
    for name, (column, scorer) in components.items():
        out[name] = out[column].apply(scorer)

    out["news2_total"] = out[list(components)].sum(axis=1)
    # A single sub-score of 3 triggers escalation on its own, whatever the
    # total - that is in the chart and easy to miss.
    out["news2_red_score"] = (out[list(components)] == 3).any(axis=1)
    return out


def news2_risk_band(total, red_score=False):
    """Map a NEWS2 total to its clinical risk band.

    :param total: the NEWS2 total
    :param red_score: True if any single parameter scored 3
    :return: one of "low", "low-medium", "medium", "high"
    """
    if total >= 7:
        return "high"
    if total >= 5 or red_score:
        return "medium"
    if total >= 1:
        return "low-medium"
    return "low"


def add_news2_band(df):
    """Add the NEWS2 risk band and the escalation it implies."""
    out = add_news2(df) if "news2_total" not in df.columns else df.copy()
    out["news2_band"] = [
        news2_risk_band(total, red)
        for total, red in zip(out["news2_total"], out["news2_red_score"])
    ]
    out["escalation"] = out["news2_band"].map(ESCALATION)
    return out


def add_time_to_antibiotics(df):
    """Add minutes from arrival to antibiotics.

    Sepsis guidance targets antibiotics within an hour of recognition, so
    `antibiotics_within_hour` is the audit measure. Patients who never
    received antibiotics get NaN minutes and False - not zero, which would
    read as instant treatment and flatter the service badly.

    :param df: DataFrame with arrival_datetime and antibiotics_datetime
    :return: new DataFrame with minutes_to_antibiotics and
             antibiotics_within_hour
    """
    out = df.copy()
    delta = out["antibiotics_datetime"] - out["arrival_datetime"]
    out["minutes_to_antibiotics"] = delta.dt.total_seconds() / 60
    out["antibiotics_given"] = out["antibiotics_datetime"].notna()
    out["antibiotics_within_hour"] = out["minutes_to_antibiotics"] <= 60
    return out


AGE_BANDS = {
    "16-39": (16, 39),
    "40-59": (40, 59),
    "60-74": (60, 74),
    "75+": (75, 120),
}


def add_age_band(df, bands=AGE_BANDS):
    """Add an `age_band` column using inclusive (low, high) pairs."""
    out = df.copy()
    lows = [low for low, _ in bands.values()]
    edges = [lows[0] - 1] + [high for _, high in bands.values()]
    out["age_band"] = pd.cut(out["age"], bins=edges, labels=list(bands))
    return out


def build_analysis_frame(df):
    """Apply every derived feature in one call.

    :param df: the merged frame from capstone.data.load_all()
    :return: DataFrame with NEWS2, bands, timings and age bands
    """
    return add_age_band(add_time_to_antibiotics(add_news2_band(add_news2(df))))
