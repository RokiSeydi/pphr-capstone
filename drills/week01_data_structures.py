"""Week 1 - Lists, dicts and indexing.

Exam archetype: Q1 (5 marks) - build a list of lists of patient records,
print it, and select a single value out of it.

Fill in each function, then run:  make drill WEEK=1
"""


def build_patient_records():
    """Return patient observations as a list of lists.

    Each inner list is one patient, in the order:
        [patient_id (str), age (int), sex (str), heart_rate (int)]

    The three patients are:
        P01, 45, Female, 78
        P02, 63, Male,   90
        P03, 29, Female, 65

    :return: list of 3 lists
    """
    raise NotImplementedError


def get_heart_rate(records, patient_id):
    """Return the heart rate for one patient.

    Do not hard-code the row position - search for the matching id, so the
    function still works if the records are reordered.

    :param records: list of lists, as returned by build_patient_records()
    :param patient_id: the id to look up, e.g. "P03"
    :return: heart rate as an int, or None if the id is not present
    """
    raise NotImplementedError


def records_to_dict(records):
    """Reshape the list of lists into a dict keyed by patient id.

    Example:
        {"P01": {"age": 45, "sex": "Female", "heart_rate": 78}, ...}

    :param records: list of lists, as returned by build_patient_records()
    :return: dict of dicts
    """
    raise NotImplementedError


def patients_over_age(records, min_age):
    """Return the ids of patients older than min_age, in input order.

    :param records: list of lists, as returned by build_patient_records()
    :param min_age: age threshold (exclusive)
    :return: list of patient id strings
    """
    raise NotImplementedError


def mean_heart_rate(records):
    """Return the mean heart rate across all patients, using only built-ins.

    No numpy here - the exam sometimes asks for plain Python.

    :param records: list of lists, as returned by build_patient_records()
    :return: float
    """
    raise NotImplementedError


# --- Dictionaries (Sep 2025 Q1, 5 marks) -------------------------------------
# The paper hands you a nested dict of drugs and asks you to change one entry
# and add another. Easy marks, but return a new dict rather than mutating the
# caller's - the exam rewards code that is safe to re-run.

BNF_LIPID_REGULATING_DRUGS = {
    "Atorvastatin": {"brand": "Lipitor", "bnf_chemical_substance": "0212000B0"},
    "Fluvastatin": {"brand": "Lescol", "bnf_chemical_substance": "0212000M0"},
    "Rosuvastatin": {"brand": "Crestor", "bnf_chemical_substance": "0212000AA"},
    "Simvastatin": {"brand": "Zocor", "bnf_chemical_substance": "0212000Y0"},
}


def update_brand(drugs, drug, new_brand):
    """Return a copy of `drugs` with one drug's brand name changed.

    Do not mutate the input - copy deeply enough that the nested dict of
    the drug you change is not shared with the original.

    :param drugs: nested dict, as BNF_LIPID_REGULATING_DRUGS
    :param drug: key of the drug to change, e.g. "Rosuvastatin"
    :param new_brand: the replacement brand name, e.g. "Rocrest"
    :return: new nested dict
    :raises KeyError: if `drug` is not in `drugs`
    """
    raise NotImplementedError


def add_drug(drugs, drug, brand, bnf_chemical_substance):
    """Return a copy of `drugs` with one more drug added.

    :param drugs: nested dict, as BNF_LIPID_REGULATING_DRUGS
    :param drug: name of the new drug, e.g. "Pravastatin"
    :param brand: its brand name, e.g. "Lipostat"
    :param bnf_chemical_substance: its BNF code, e.g. "0212000X0"
    :return: new nested dict
    :raises ValueError: if `drug` is already present
    """
    raise NotImplementedError


def brands_by_code(drugs):
    """Invert the dict: map BNF chemical substance code -> brand name.

    :param drugs: nested dict, as BNF_LIPID_REGULATING_DRUGS
    :return: dict mapping code (str) -> brand (str)
    """
    raise NotImplementedError
