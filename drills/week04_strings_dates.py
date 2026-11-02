"""Week 4 - Strings, f-strings and dates.

Exam archetypes:
    Sep 2025 Q2 (5 marks) - has the patient met a 30-day symptom criterion?
    Sep 2025 Q3 (5 marks) - loop over a dict printing a formatted sentence.

Date questions are easy marks that are easy to drop: get `days` from a
timedelta, and remember that comparisons need `date` against `date`, never
`date` against `datetime`.
"""
from datetime import date, datetime, timedelta


def days_between(start, end):
    """Return the whole number of days from `start` to `end`.

    Accept either date or datetime objects, in any mix, and normalise to
    dates before subtracting.

    :param start: the earlier date/datetime
    :param end: the later date/datetime
    :return: int days (negative if end precedes start)
    """
    raise NotImplementedError


def meets_duration_criterion(symptom_onset, assessment_date, min_days=30):
    """Decide whether symptoms have persisted long enough to diagnose.

    A schizophrenia diagnosis needs symptoms for at least `min_days`.

    :param symptom_onset: date symptoms began
    :param assessment_date: date of assessment ("today" in the exam)
    :param min_days: minimum persistence in days
    :return: tuple (met: bool, days_elapsed: int)
    """
    raise NotImplementedError


def diagnosis_message(patient_id, symptom_onset, assessment_date, min_days=30):
    """Return the sentence the exam asks you to print.

    When the criterion is met:
        "P-001: symptoms have persisted 58 days - diagnosis may be considered."
    When it is not:
        "P-001: symptoms have persisted 12 days - diagnosis cannot yet be considered."

    Build it with an f-string. Note "days" is always plural here.

    :param patient_id: patient identifier
    :param symptom_onset: date symptoms began
    :param assessment_date: date of assessment
    :param min_days: minimum persistence in days
    :return: the formatted string
    """
    raise NotImplementedError


def parse_iso_dates(date_strings):
    """Convert "YYYY-MM-DD" strings to date objects, skipping unparseable ones.

    :param date_strings: list of strings
    :return: list of date objects, same order, bad values dropped
    """
    raise NotImplementedError


def weekday_names(dates):
    """Return the weekday name for each date, e.g. "Monday".

    :param dates: list of date or datetime objects
    :return: list of weekday name strings
    """
    raise NotImplementedError


def format_cause_of_death(records):
    """Format a dict of {name: year} into the exam's sentences.

    Each line reads:
        "King George VI died from a heart-related illness in 1952"

    :param records: dict mapping name (str) -> year (int)
    :return: list of formatted strings, in the dict's insertion order
    """
    raise NotImplementedError


def follow_up_date(index_date, weeks):
    """Return the date `weeks` weeks after `index_date`.

    :param index_date: starting date
    :param weeks: number of weeks to add
    :return: a date object
    """
    raise NotImplementedError
