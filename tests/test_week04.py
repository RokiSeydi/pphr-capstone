"""Week 4 - strings, f-strings and dates."""
from datetime import date, datetime

import pytest

from tests._target import mod

w = mod("week04_strings_dates")

ONSET = date(2025, 8, 5)
ASSESSED = date(2025, 9, 2)


def test_days_between():
    assert w.days_between(ONSET, ASSESSED) == 28


def test_days_between_accepts_datetimes():
    assert w.days_between(datetime(2025, 8, 5, 23, 59), ASSESSED) == 28


def test_days_between_is_signed():
    assert w.days_between(ASSESSED, ONSET) == -28


def test_meets_duration_criterion_not_yet():
    # The exam's own numbers: 5 Aug to 2 Sep is 28 days, short of 30.
    met, elapsed = w.meets_duration_criterion(ONSET, ASSESSED)
    assert met is False
    assert elapsed == 28


def test_meets_duration_criterion_met():
    met, elapsed = w.meets_duration_criterion(ONSET, date(2025, 9, 10))
    assert met is True
    assert elapsed == 36


def test_meets_duration_criterion_exact_boundary():
    met, _ = w.meets_duration_criterion(ONSET, date(2025, 9, 4))
    assert met is True, "30 days exactly should meet an 'at least 30 days' rule"


def test_diagnosis_message_not_met():
    message = w.diagnosis_message("P-001", ONSET, ASSESSED)
    assert message == (
        "P-001: symptoms have persisted 28 days - "
        "diagnosis cannot yet be considered."
    )


def test_diagnosis_message_met():
    message = w.diagnosis_message("P-002", ONSET, date(2025, 9, 10))
    assert message == (
        "P-002: symptoms have persisted 36 days - "
        "diagnosis may be considered."
    )


def test_parse_iso_dates():
    assert w.parse_iso_dates(["2025-08-05", "2025-01-01"]) == [
        date(2025, 8, 5), date(2025, 1, 1)
    ]


def test_parse_iso_dates_skips_junk():
    assert w.parse_iso_dates(["2025-08-05", "not a date", "", "05/08/2025"]) == [
        date(2025, 8, 5)
    ]


def test_weekday_names():
    assert w.weekday_names([date(2025, 9, 1), date(2025, 9, 2)]) == [
        "Monday", "Tuesday"
    ]


def test_format_cause_of_death():
    records = {"King George VI": 1952, "Carrie Fisher": 2016}
    assert w.format_cause_of_death(records) == [
        "King George VI died from a heart-related illness in 1952",
        "Carrie Fisher died from a heart-related illness in 2016",
    ]


def test_follow_up_date():
    assert w.follow_up_date(date(2025, 9, 2), 6) == date(2025, 10, 14)
