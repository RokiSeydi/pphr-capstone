"""Week 3 reference solutions - clinical decision logic."""

ADMIT_CARDIOLOGY = "Admit to cardiology unit"
ADMIT_OBSERVATION = "Admit for further observation"
DISCHARGE = "Discharge with follow-up advice"


def triage_chest_pain(chest_pain, ecg_abnormal, troponin_elevated):
    if chest_pain == "yes":
        if ecg_abnormal == "yes":
            return ADMIT_CARDIOLOGY
        if troponin_elevated == "yes":
            return ADMIT_OBSERVATION
        return DISCHARGE
    # No chest pain: an elevated troponin still warrants observation.
    if troponin_elevated == "yes":
        return ADMIT_OBSERVATION
    return DISCHARGE


def news2_respiratory_score(breaths_per_min):
    if breaths_per_min <= 8:
        return 3
    if breaths_per_min <= 11:
        return 1
    if breaths_per_min <= 20:
        return 0
    if breaths_per_min <= 24:
        return 2
    return 3


def bmi_category(weight_kg, height_m):
    if height_m <= 0:
        raise ValueError(f"height must be positive, got {height_m}")
    bmi = weight_kg / height_m ** 2
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def egfr_ckd_stage(egfr):
    if egfr >= 90:
        return "G1"
    if egfr >= 60:
        return "G2"
    if egfr >= 45:
        return "G3a"
    if egfr >= 30:
        return "G3b"
    if egfr >= 15:
        return "G4"
    return "G5"
