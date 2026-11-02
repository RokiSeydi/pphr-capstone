"""Week 3 - clinical decision logic."""
import pytest

from tests._target import mod

w = mod("week03_conditionals")

CARDIOLOGY = "Admit to cardiology unit"
OBSERVATION = "Admit for further observation"
DISCHARGE = "Discharge with follow-up advice"


@pytest.mark.parametrize("pain,ecg,trop,expected", [
    ("yes", "yes", "yes", CARDIOLOGY),
    ("yes", "yes", "no", CARDIOLOGY),
    ("yes", "no", "yes", OBSERVATION),
    ("yes", "no", "no", DISCHARGE),
    # The case the exam asks you to test explicitly:
    ("no", "no", "yes", OBSERVATION),
    ("no", "no", "no", DISCHARGE),
])
def test_triage_chest_pain(pain, ecg, trop, expected):
    assert w.triage_chest_pain(pain, ecg, trop) == expected


@pytest.mark.parametrize("rate,score", [
    (6, 3), (8, 3), (9, 1), (11, 1), (12, 0), (20, 0),
    (21, 2), (24, 2), (25, 3), (40, 3),
])
def test_news2_respiratory_score(rate, score):
    assert w.news2_respiratory_score(rate) == score


@pytest.mark.parametrize("weight,height,expected", [
    (45, 1.70, "Underweight"),
    (65, 1.70, "Normal"),
    (80, 1.70, "Overweight"),
    (95, 1.70, "Obese"),
])
def test_bmi_category(weight, height, expected):
    assert w.bmi_category(weight, height) == expected


def test_bmi_category_boundaries():
    # Exactly 25.0 is "Overweight", not "Normal".
    assert w.bmi_category(25.0, 1.0) == "Overweight"
    assert w.bmi_category(18.5, 1.0) == "Normal"
    assert w.bmi_category(30.0, 1.0) == "Obese"


def test_bmi_category_rejects_bad_height():
    with pytest.raises(ValueError):
        w.bmi_category(70, 0)


@pytest.mark.parametrize("egfr,stage", [
    (120, "G1"), (90, "G1"), (89, "G2"), (60, "G2"), (59, "G3a"),
    (45, "G3a"), (44, "G3b"), (30, "G3b"), (29, "G4"), (15, "G4"), (9, "G5"),
])
def test_egfr_ckd_stage(egfr, stage):
    assert w.egfr_ckd_stage(egfr) == stage
