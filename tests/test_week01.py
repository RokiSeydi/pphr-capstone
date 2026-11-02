"""Week 1 - lists, dicts and indexing."""
import pytest

from tests._target import mod

w = mod("week01_data_structures")


def test_records_shape():
    records = w.build_patient_records()
    assert isinstance(records, list)
    assert len(records) == 3
    assert all(isinstance(row, list) and len(row) == 4 for row in records)


def test_records_content():
    assert w.build_patient_records() == [
        ["P01", 45, "Female", 78],
        ["P02", 63, "Male", 90],
        ["P03", 29, "Female", 65],
    ]


def test_get_heart_rate():
    records = w.build_patient_records()
    assert w.get_heart_rate(records, "P03") == 65
    assert w.get_heart_rate(records, "P01") == 78


def test_get_heart_rate_searches_rather_than_indexes():
    # Reordering the records must not change the answer.
    reordered = list(reversed(w.build_patient_records()))
    assert w.get_heart_rate(reordered, "P03") == 65


def test_get_heart_rate_unknown_id():
    assert w.get_heart_rate(w.build_patient_records(), "P99") is None


def test_records_to_dict():
    result = w.records_to_dict(w.build_patient_records())
    assert set(result) == {"P01", "P02", "P03"}
    assert result["P02"] == {"age": 63, "sex": "Male", "heart_rate": 90}


def test_patients_over_age():
    assert w.patients_over_age(w.build_patient_records(), 40) == ["P01", "P02"]
    assert w.patients_over_age(w.build_patient_records(), 100) == []


def test_mean_heart_rate():
    assert w.mean_heart_rate(w.build_patient_records()) == pytest.approx(77.666, abs=1e-3)


def test_update_brand():
    result = w.update_brand(w.BNF_LIPID_REGULATING_DRUGS, "Rosuvastatin", "Rocrest")
    assert result["Rosuvastatin"]["brand"] == "Rocrest"
    assert result["Rosuvastatin"]["bnf_chemical_substance"] == "0212000AA"


def test_update_brand_does_not_mutate_input():
    original = w.BNF_LIPID_REGULATING_DRUGS
    w.update_brand(original, "Rosuvastatin", "Rocrest")
    assert original["Rosuvastatin"]["brand"] == "Crestor"


def test_update_brand_unknown_drug():
    with pytest.raises(KeyError):
        w.update_brand(w.BNF_LIPID_REGULATING_DRUGS, "Aspirin", "Nurofen")


def test_add_drug():
    result = w.add_drug(
        w.BNF_LIPID_REGULATING_DRUGS, "Pravastatin", "Lipostat", "0212000X0"
    )
    assert len(result) == len(w.BNF_LIPID_REGULATING_DRUGS) + 1
    assert result["Pravastatin"] == {
        "brand": "Lipostat",
        "bnf_chemical_substance": "0212000X0",
    }


def test_add_drug_rejects_duplicate():
    with pytest.raises(ValueError):
        w.add_drug(w.BNF_LIPID_REGULATING_DRUGS, "Simvastatin", "X", "Y")


def test_brands_by_code():
    result = w.brands_by_code(w.BNF_LIPID_REGULATING_DRUGS)
    assert result["0212000B0"] == "Lipitor"
    assert len(result) == 4
