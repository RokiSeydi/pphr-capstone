"""Week 1 reference solutions - lists, dicts and indexing."""
import copy

BNF_LIPID_REGULATING_DRUGS = {
    "Atorvastatin": {"brand": "Lipitor", "bnf_chemical_substance": "0212000B0"},
    "Fluvastatin": {"brand": "Lescol", "bnf_chemical_substance": "0212000M0"},
    "Rosuvastatin": {"brand": "Crestor", "bnf_chemical_substance": "0212000AA"},
    "Simvastatin": {"brand": "Zocor", "bnf_chemical_substance": "0212000Y0"},
}


def build_patient_records():
    return [
        ["P01", 45, "Female", 78],
        ["P02", 63, "Male", 90],
        ["P03", 29, "Female", 65],
    ]


def get_heart_rate(records, patient_id):
    # Search rather than index by position, so reordering cannot break it.
    for record in records:
        if record[0] == patient_id:
            return record[3]
    return None


def records_to_dict(records):
    return {
        record[0]: {"age": record[1], "sex": record[2], "heart_rate": record[3]}
        for record in records
    }


def patients_over_age(records, min_age):
    return [record[0] for record in records if record[1] > min_age]


def mean_heart_rate(records):
    rates = [record[3] for record in records]
    return sum(rates) / len(rates)


def update_brand(drugs, drug, new_brand):
    if drug not in drugs:
        raise KeyError(f"{drug!r} is not in the drug dictionary")
    updated = copy.deepcopy(drugs)
    updated[drug]["brand"] = new_brand
    return updated


def add_drug(drugs, drug, brand, bnf_chemical_substance):
    if drug in drugs:
        raise ValueError(f"{drug!r} is already in the drug dictionary")
    updated = copy.deepcopy(drugs)
    updated[drug] = {
        "brand": brand,
        "bnf_chemical_substance": bnf_chemical_substance,
    }
    return updated


def brands_by_code(drugs):
    return {
        details["bnf_chemical_substance"]: details["brand"]
        for details in drugs.values()
    }
