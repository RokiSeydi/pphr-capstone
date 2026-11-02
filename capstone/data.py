"""Loading and joining the five capstone tables.

    attendances  one row per ED attendance, with free-text complaint
    observations one row per attendance: vital signs at triage
    labs         one row per attendance: bloods (lactate, WCC, CRP, creatinine)
    outcomes     one row per attendance: antibiotics time, ICU, LOS, death
    hospitals    one row per hospital: name, region, bed count

Keeping them separate is the point - the exam always makes you join.
"""
import pandas as pd

from capstone import paths


def load_attendances(path=paths.ATTENDANCES_CSV):
    """Load ED attendances, parsing the arrival timestamp."""
    return pd.read_csv(path, parse_dates=["arrival_datetime"])


def load_observations(path=paths.OBSERVATIONS_CSV):
    """Load triage vital signs."""
    return pd.read_csv(path)


def load_labs(path=paths.LABS_CSV):
    """Load blood results. Lactate and CRP have genuine missing values."""
    return pd.read_csv(path)


def load_outcomes(path=paths.OUTCOMES_CSV):
    """Load outcomes, parsing the antibiotics timestamp.

    A blank antibiotics time means none were given, and becomes NaT.
    """
    return pd.read_csv(path, parse_dates=["antibiotics_datetime"])


def load_hospitals(path=paths.HOSPITALS_CSV):
    """Load the hospital lookup table."""
    return pd.read_csv(path)


def load_all():
    """Join every table into one analysis frame, one row per attendance.

    Attendances are the spine: a left join keeps an attendance even when its
    bloods are missing, which is what you want - dropping those rows would
    quietly bias the analysis towards the patients who were investigated
    most thoroughly.

    :return: merged DataFrame, one row per attendance
    """
    frame = load_attendances()
    for table in (load_observations(), load_labs(), load_outcomes()):
        frame = frame.merge(table, on="attendance_id", how="left")
    frame = frame.merge(load_hospitals(), on="hospital_id", how="left")

    assert len(frame) == len(load_attendances()), "the join changed the row count"
    return frame


def missing_summary(df):
    """Count and rate of missing values, for columns that have any.

    :param df: any DataFrame
    :return: DataFrame indexed by column with n_missing and pct_missing
    """
    counts = df.isna().sum()
    counts = counts[counts > 0].sort_values(ascending=False)
    return pd.DataFrame({
        "n_missing": counts,
        "pct_missing": (100 * counts / len(df)).round(1),
    })
