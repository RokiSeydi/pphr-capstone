"""Week 7 - classes and inheritance."""
import pytest

from tests._target import mod

w = mod("week07_classes")


@pytest.mark.parametrize("fasting,post,expected", [
    (95, 130, "Normal"),
    (110, 160, "Prediabetes"),
    (128, 175, "Diabetes"),
    (92, 205, "Diabetes"),
])
def test_assess_glycaemia_exam_cases(fasting, post, expected):
    profile = w.GlucoseProfile("Test", fasting, post)
    assert profile.assess_glycaemia() == expected


def test_assess_glycaemia_boundaries():
    # 126 fasting is diabetes; 125 with a normal post-meal is prediabetes.
    assert w.GlucoseProfile("A", 126, 100).assess_glycaemia() == "Diabetes"
    assert w.GlucoseProfile("B", 125, 139).assess_glycaemia() == "Prediabetes"
    assert w.GlucoseProfile("C", 99, 139).assess_glycaemia() == "Normal"
    assert w.GlucoseProfile("D", 100, 139).assess_glycaemia() == "Prediabetes"


def test_assess_glycaemia_checks_diabetes_first():
    # Fasting is normal but post-meal is diabetic - order of checks matters.
    assert w.GlucoseProfile("E", 92, 205).assess_glycaemia() == "Diabetes"


def test_glucose_profile_repr():
    text = repr(w.GlucoseProfile("Alice", 95, 130))
    assert "Alice" in text and "95" in text and "130" in text


def test_waiting_list_proportion():
    assert w.WaitingList("RCF", 200, 184).proportion_within_target() == 0.92


def test_waiting_list_proportion_zero_total():
    assert w.WaitingList("RXX", 0, 0).proportion_within_target() is None


def test_waiting_list_meets_standard():
    assert w.WaitingList("A", 100, 92).meets_standard() is True
    assert w.WaitingList("B", 100, 91).meets_standard() is False


def test_waiting_list_empty_meets_standard():
    assert w.WaitingList("C", 0, 0).meets_standard() is True


def test_ambulance_list_uses_stricter_default():
    # 93% passes the 92% general standard but fails the 95% ambulance one.
    assert w.WaitingList("A", 100, 93).meets_standard() is True
    assert w.AmbulanceWaitingList("A", 100, 93).meets_standard() is False
    assert w.AmbulanceWaitingList("A", 100, 95).meets_standard() is True


def test_ambulance_list_is_a_waiting_list():
    assert issubclass(w.AmbulanceWaitingList, w.WaitingList)


def test_ambulance_list_respects_explicit_threshold():
    assert w.AmbulanceWaitingList("A", 100, 93).meets_standard(0.90) is True


def test_low_risk_patient():
    assert w.low_risk_patient().assess_risk() == "Low Risk"


def test_moderate_risk_patient():
    assert w.moderate_risk_patient().assess_risk() == "Moderate Risk"


def test_high_risk_patient():
    assert w.high_risk_patient().assess_risk() == "High Risk"


def test_risk_patients_are_profiles():
    for factory in (w.low_risk_patient, w.moderate_risk_patient,
                    w.high_risk_patient):
        assert isinstance(factory(), w.CardioRiskProfile)
