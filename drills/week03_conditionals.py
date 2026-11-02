"""Week 3 - Conditionals and clinical decision logic.

Exam archetype: Q3 (10 marks) - turn a printed decision tree into code.
Expect to be handed a flow diagram and asked to reproduce it exactly.
"""


def triage_chest_pain(chest_pain, ecg_abnormal, troponin_elevated):
    """Apply the A&E chest-pain decision tree.

    The tree (see mocks/flow_diagram.png):
        - chest pain "yes" AND ECG abnormal "yes"  -> admit to cardiology
        - chest pain "yes" AND ECG normal, but troponin elevated
                                                   -> admit for observation
        - chest pain "yes", ECG normal, troponin normal
                                                   -> discharge with advice
        - no chest pain, but troponin elevated     -> admit for observation
        - no chest pain, troponin normal           -> discharge with advice

    :param chest_pain: "yes" or "no"
    :param ecg_abnormal: "yes" or "no"
    :param troponin_elevated: "yes" or "no"
    :return: one of "Admit to cardiology unit",
             "Admit for further observation",
             "Discharge with follow-up advice"
    """
    raise NotImplementedError


def news2_respiratory_score(breaths_per_min):
    """Return the NEWS2 sub-score for respiratory rate.

    Bands:
        <= 8        -> 3
        9 to 11     -> 1
        12 to 20    -> 0
        21 to 24    -> 2
        >= 25       -> 3

    :param breaths_per_min: respiratory rate
    :return: int score from 0 to 3
    """
    raise NotImplementedError


def bmi_category(weight_kg, height_m):
    """Classify BMI using WHO cut-offs.

        < 18.5          -> "Underweight"
        18.5 to < 25    -> "Normal"
        25 to < 30      -> "Overweight"
        >= 30           -> "Obese"

    :param weight_kg: weight in kilograms
    :param height_m: height in metres
    :return: category string
    :raises ValueError: if height_m is zero or negative
    """
    raise NotImplementedError


def egfr_ckd_stage(egfr):
    """Return the CKD stage for an eGFR value (mL/min/1.73m2).

        >= 90       -> "G1"
        60 to 89    -> "G2"
        45 to 59    -> "G3a"
        30 to 44    -> "G3b"
        15 to 29    -> "G4"
        < 15        -> "G5"

    :param egfr: estimated glomerular filtration rate
    :return: stage string
    """
    raise NotImplementedError
