"""Summary tables for the capstone.

Every function returns a DataFrame or Series ready to display - the exam
asks for "a detailed report using a combination of code, text, figures and
tables", so the table is the deliverable, not a printed blob.
"""
import numpy as np
import pandas as pd

BAND_ORDER = ["low", "low-medium", "medium", "high"]
TRIAGE_ORDER = ["Immediate", "Very urgent", "Urgent", "Standard", "Non-urgent"]


def cohort_description(df):
    """One-row summary of the cohort, for the top of the report."""
    return pd.Series({
        "Attendances": len(df),
        "Distinct patients": df["patient_id"].nunique(),
        "Hospitals": df["hospital_id"].nunique(),
        "Median age": df["age"].median(),
        "Female (%)": round(100 * (df["sex"] == "Female").mean(), 1),
        "ICU admissions": int(df["icu_admission"].sum()),
        "ICU admission rate (%)": round(100 * df["icu_admission"].mean(), 1),
        "In-hospital deaths": int(df["died_in_hospital"].sum()),
    })


def outcomes_by_news2_band(df):
    """ICU admission, mortality and length of stay by NEWS2 band.

    The gradient across the bands is the headline result: if NEWS2 is doing
    its job, risk should rise monotonically.
    """
    grouped = df.groupby("news2_band", observed=False).agg(
        n=("attendance_id", "count"),
        icu_rate=("icu_admission", "mean"),
        mortality=("died_in_hospital", "mean"),
        median_los=("length_of_stay_days", "median"),
        median_news2=("news2_total", "median"),
    )
    grouped["icu_rate"] = (100 * grouped["icu_rate"]).round(1)
    grouped["mortality"] = (100 * grouped["mortality"]).round(1)
    return grouped.reindex(BAND_ORDER)


def antibiotics_audit(df):
    """Door-to-antibiotics performance by triage category.

    Two different denominators matter and are easy to confuse:
        within_hour_of_treated - of those given antibiotics, how many
            inside an hour (a timeliness measure)
        within_hour_of_all - of every attendance, how many got antibiotics
            inside an hour (a coverage-and-timeliness measure)

    Quoting the first alone makes a service look better than it is.
    """
    def summarise(group):
        treated = group[group["antibiotics_given"]]
        return pd.Series({
            "n": len(group),
            "treated": len(treated),
            "treated_pct": round(100 * len(treated) / len(group), 1),
            "median_minutes": round(treated["minutes_to_antibiotics"].median(), 1)
            if len(treated) else np.nan,
            "within_hour_of_treated": round(
                100 * treated["antibiotics_within_hour"].mean(), 1
            ) if len(treated) else np.nan,
            "within_hour_of_all": round(
                100 * group["antibiotics_within_hour"].mean(), 1
            ),
        })

    table = df.groupby("triage_category", observed=False).apply(
        summarise, include_groups=False
    )
    return table.reindex([t for t in TRIAGE_ORDER if t in table.index])


def news2_by_outcome_crosstab(df):
    """Counts of attendances by NEWS2 band and ICU admission.

    The Week 11 skill, on the capstone question.
    """
    table = pd.crosstab(df["news2_band"], df["icu_admission"])
    table.columns = ["Not admitted to ICU", "Admitted to ICU"]
    return table.reindex(BAND_ORDER, fill_value=0)


def hospital_variation(df):
    """Case mix and outcomes per hospital.

    Raw ICU rates differ for two reasons - sicker patients, or different
    thresholds for admitting them. Reporting median NEWS2 alongside the rate
    is what lets a reader tell those apart, and is the honest way to present
    a league table.
    """
    grouped = df.groupby(["hospital_id", "hospital_name", "region"],
                         observed=False).agg(
        attendances=("attendance_id", "count"),
        median_age=("age", "median"),
        median_news2=("news2_total", "median"),
        icu_rate=("icu_admission", "mean"),
        median_minutes_to_abx=("minutes_to_antibiotics", "median"),
    ).reset_index()
    grouped["icu_rate"] = (100 * grouped["icu_rate"]).round(1)
    return grouped.sort_values("icu_rate", ascending=False)


def missingness_by_triage(df):
    """Rate of missing lactate by triage category.

    The missing values are not missing at random - bloods are skipped more
    often for patients triaged as less unwell. A complete-case analysis
    would therefore drop a non-random slice of the cohort, which is worth a
    paragraph in any write-up.
    """
    table = df.groupby("triage_category", observed=False).agg(
        n=("attendance_id", "count"),
        lactate_missing_pct=("lactate", lambda s: round(100 * s.isna().mean(), 1)),
    )
    return table.reindex([t for t in TRIAGE_ORDER if t in table.index])
