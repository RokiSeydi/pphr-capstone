"""Week 4 reference solutions - strings, f-strings and dates."""
from datetime import date, datetime, timedelta


def _as_date(value):
    """Normalise a date or datetime to a date, so the two can be compared."""
    return value.date() if isinstance(value, datetime) else value


def days_between(start, end):
    return (_as_date(end) - _as_date(start)).days


def meets_duration_criterion(symptom_onset, assessment_date, min_days=30):
    elapsed = days_between(symptom_onset, assessment_date)
    return elapsed >= min_days, elapsed


def diagnosis_message(patient_id, symptom_onset, assessment_date, min_days=30):
    met, elapsed = meets_duration_criterion(
        symptom_onset, assessment_date, min_days=min_days
    )
    verdict = "may be considered" if met else "cannot yet be considered"
    return (
        f"{patient_id}: symptoms have persisted {elapsed} days - "
        f"diagnosis {verdict}."
    )


def parse_iso_dates(date_strings):
    parsed = []
    for value in date_strings:
        try:
            parsed.append(datetime.strptime(value, "%Y-%m-%d").date())
        except (ValueError, TypeError):
            continue  # drop anything that is not a valid ISO date
    return parsed


def weekday_names(dates):
    return [_as_date(value).strftime("%A") for value in dates]


def format_cause_of_death(records):
    return [
        f"{name} died from a heart-related illness in {year}"
        for name, year in records.items()
    ]


def follow_up_date(index_date, weeks):
    return _as_date(index_date) + timedelta(weeks=weeks)
