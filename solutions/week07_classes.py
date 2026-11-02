"""Week 7 reference solutions - classes and inheritance."""


class GlucoseProfile:
    def __init__(self, patient_name, fasting_glucose, postprandial_glucose):
        self.patient_name = patient_name
        self.fasting_glucose = fasting_glucose
        self.postprandial_glucose = postprandial_glucose

    def assess_glycaemia(self):
        # Diabetes is tested first: its thresholds overlap the others, so
        # checking "Normal" first would misclassify a high postprandial.
        if self.fasting_glucose >= 126 or self.postprandial_glucose >= 200:
            return "Diabetes"
        if self.fasting_glucose < 100 and self.postprandial_glucose < 140:
            return "Normal"
        return "Prediabetes"

    def __repr__(self):
        return (
            f"GlucoseProfile({self.patient_name!r}, "
            f"fasting={self.fasting_glucose}, "
            f"postprandial={self.postprandial_glucose})"
        )


class WaitingList:
    def __init__(self, org_code, total, within_18_weeks):
        self.org_code = org_code
        self.total = total
        self.within_18_weeks = within_18_weeks

    def proportion_within_target(self):
        if self.total == 0:
            return None
        return self.within_18_weeks / self.total

    def meets_standard(self, threshold=0.92):
        proportion = self.proportion_within_target()
        if proportion is None:
            return True  # nobody waiting, so the standard is trivially met
        return proportion >= threshold


class AmbulanceWaitingList(WaitingList):
    def meets_standard(self, threshold=0.95):
        return super().meets_standard(threshold=threshold)


class CardioRiskProfile:
    def __init__(self, patient_name, systolic_bp, diastolic_bp,
                 regular_exercise, diet_type):
        self.patient_name = patient_name
        self.systolic_bp = systolic_bp
        self.diastolic_bp = diastolic_bp
        self.regular_exercise = regular_exercise
        self.diet_type = diet_type

    def assess_risk(self):
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
    # Below every threshold, and no adverse lifestyle combination.
    return CardioRiskProfile("Low", 118, 72, True, "vegan")


def moderate_risk_patient():
    # BP in the 130/80 band, but exercises and is not an omnivore.
    return CardioRiskProfile("Moderate", 132, 78, True, "vegetarian")


def high_risk_patient():
    return CardioRiskProfile("High", 148, 94, False, "omnivore")
