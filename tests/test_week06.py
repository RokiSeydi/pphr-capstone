"""Week 6 - regex on clinical free text."""
import pandas as pd
import pytest

from tests._target import mod

w = mod("week06_regex")

MESSAGES = [
    "I've been waiting for 13 weeks for my appointment.",
    "I think I have waited around 19 weeks.",
    "My family have waited up to 16 weeks.",
    "Unfortunately, my last appointment was delayed by 24 weeks.",
    "I was told to wait for 8 weeks before my next check-up, but I waited 10 weeks.",
    "I don't remember how long I have been waiting.",
    "I only waited for 25 days.",
]


def test_extract_waiting_weeks_exam_data():
    # Both numbers from the two-mention message; nothing from days or vague.
    assert w.extract_waiting_weeks(MESSAGES) == [13, 19, 16, 24, 8, 10]


def test_extract_waiting_weeks_ignores_other_units():
    assert w.extract_waiting_weeks(["waited 25 days", "waited 3 months"]) == []


def test_extract_waiting_weeks_handles_singular():
    assert w.extract_waiting_weeks(["just 1 week so far"]) == [1]


def test_extract_waiting_weeks_empty():
    assert w.extract_waiting_weeks([]) == []


def test_extract_icd10_codes():
    text = "Diagnosed F20, later E11.9, and I21 noted."
    assert w.extract_icd10_codes(text) == ["F20", "E11.9", "I21"]


def test_extract_blood_pressure():
    assert w.extract_blood_pressure("BP was 140/90, later 128/82") == [
        (140, 90), (128, 82)
    ]


def test_extract_blood_pressure_none():
    assert w.extract_blood_pressure("no readings recorded") == []


def test_extract_hba1c():
    text = "HbA1c 58 mmol/mol, previously 62.5mmol/mol"
    assert w.extract_hba1c(text) == [58.0, 62.5]


def test_redact_nhs_numbers():
    assert w.redact_nhs_numbers("NHS 485 777 3456 on file") == (
        "NHS [NHS NUMBER] on file"
    )


def test_redact_nhs_numbers_formats():
    for written in ["4857773456", "485-777-3456", "485 777 3456"]:
        assert w.redact_nhs_numbers(written) == "[NHS NUMBER]"


@pytest.mark.parametrize("description,expected", [
    ("I am a vegan", True),
    ("I eat a plant-based diet", True),
    ("I don\u2019t eat any animal products", True),
    ("I'm committed to veganism.", True),
    ("I never eat animal products", True),
    ("I could not live without meat", False),
    ("I am a vegetarian", False),
    ("I am not vegan", False),
    ("I used to be vegan but now eat fish", False),
    ("I eat anything but vegan food", False),
    ("I am no longer vegan", False),
    ("VEGAN for ten years", True),
])
def test_classify_vegan(description, expected):
    assert w.classify_vegan(description) is expected


def test_classify_vegan_handles_non_string():
    assert w.classify_vegan(None) is False


def test_classification_agreement_on_exam_data(diet):
    result = w.classification_agreement(diet, "Diet_description", "Diet")
    assert result["n"] == len(diet)
    assert 0.0 <= result["accuracy"] <= 1.0
    assert result["agree"] + result["false_positives"] + result["false_negatives"] == result["n"]
    # The regex rule should do far better than guessing.
    assert result["accuracy"] > 0.8


def test_classification_agreement_reports_the_contradictory_labels(diet):
    """The exam data contains two descriptions that say the same thing and
    carry opposite labels, so perfect agreement is not achievable. A rule
    that claims 100% has almost certainly been fitted to the labels."""
    result = w.classification_agreement(diet, "Diet_description", "Diet")
    assert result["agree"] < result["n"], (
        "the labels are internally inconsistent - some disagreement is correct"
    )
