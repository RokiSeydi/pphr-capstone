"""Week 7 - Classes, methods and inheritance.

Exam archetype: Q7 (5 marks) - a class skeleton is given with __init__
already written, and you add the method that applies clinical criteria.
"""


class GlucoseProfile:
    """A patient's fasting and post-meal blood glucose.

    :param patient_name: name of the patient (str)
    :param fasting_glucose: fasting glucose in mg/dL (int/float)
    :param postprandial_glucose: 2-hour post-meal glucose in mg/dL
    """

    def __init__(self, patient_name, fasting_glucose, postprandial_glucose):
        self.patient_name = patient_name
        self.fasting_glucose = fasting_glucose
        self.postprandial_glucose = postprandial_glucose

    def assess_glycaemia(self):
        """Classify the profile against simplified diagnostic criteria.

        Order matters - test for diabetes first:
            "Diabetes"    if fasting >= 126 or postprandial >= 200
            "Normal"      if fasting < 100 and postprandial < 140
            "Prediabetes" otherwise

        :return: one of "Normal", "Prediabetes", "Diabetes"
        """
        raise NotImplementedError

    def __repr__(self):
        """Return a readable representation, e.g.
        GlucoseProfile('Alice', fasting=95, postprandial=130)
        """
        raise NotImplementedError


class WaitingList:
    """Waiting-list figures for one NHS organisation.

    :param org_code: organisation code (str)
    :param total: total patients waiting (int)
    :param within_18_weeks: of those, how many have waited <= 18 weeks
    """

    def __init__(self, org_code, total, within_18_weeks):
        self.org_code = org_code
        self.total = total
        self.within_18_weeks = within_18_weeks

    def proportion_within_target(self):
        """Return within_18_weeks / total, or None when total is zero.

        :return: float proportion, or None
        """
        raise NotImplementedError

    def meets_standard(self, threshold=0.92):
        """Return True when the proportion within target reaches `threshold`.

        An organisation with no patients waiting trivially meets it.

        :param threshold: the constitutional standard, default 92%
        :return: bool
        """
        raise NotImplementedError


class AmbulanceWaitingList(WaitingList):
    """A waiting list for an ambulance trust, which is held to 95%."""

    def meets_standard(self, threshold=0.95):
        """Same test as the parent, but with a stricter default threshold.

        Call the parent implementation rather than repeating the logic.

        :param threshold: default 95% for ambulance trusts
        :return: bool
        """
        raise NotImplementedError


# --- Reading a class to drive its branches (Sep 2025 Q5, 5 marks) ------------
# A twist worth practising: the paper gives you a *finished* class and asks you
# to construct instances that make its method return each possible value. You
# are being marked on reading the conditions correctly, not on writing them.


class CardioRiskProfile:
    """A patient's cardiovascular risk factors. This class is complete.

    :param patient_name: name of the patient (str)
    :param systolic_bp: systolic blood pressure (int)
    :param diastolic_bp: diastolic blood pressure (int)
    :param regular_exercise: True if the patient exercises regularly (bool)
    :param diet_type: "vegan", "vegetarian" or "omnivore"
    """

    def __init__(self, patient_name, systolic_bp, diastolic_bp,
                 regular_exercise, diet_type):
        self.patient_name = patient_name
        self.systolic_bp = systolic_bp
        self.diastolic_bp = diastolic_bp
        self.regular_exercise = regular_exercise
        self.diet_type = diet_type

    def assess_risk(self):
        """Return "High Risk", "Moderate Risk" or "Low Risk"."""
        if self.systolic_bp >= 140 or self.diastolic_bp >= 90:
            return "High Risk"
        if self.systolic_bp >= 130 or self.diastolic_bp >= 80:
            if not self.regular_exercise or self.diet_type == "omnivore":
                return "High Risk"
            return "Moderate Risk"
        if not self.regular_exercise and self.diet_type == "omnivore":
            return "Moderate Risk"
        return "Low Risk"


def low_risk_patient():
    """Return a CardioRiskProfile whose assess_risk() gives "Low Risk".

    :return: CardioRiskProfile instance
    """
    raise NotImplementedError


def moderate_risk_patient():
    """Return a CardioRiskProfile whose assess_risk() gives "Moderate Risk".

    :return: CardioRiskProfile instance
    """
    raise NotImplementedError


def high_risk_patient():
    """Return a CardioRiskProfile whose assess_risk() gives "High Risk".

    :return: CardioRiskProfile instance
    """
    raise NotImplementedError
