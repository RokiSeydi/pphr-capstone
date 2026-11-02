"""Week 6 reference solutions - regex on clinical free text."""
import re

import pandas as pd

WEEKS_PATTERN = re.compile(r"(\d+)\s*weeks?\b", re.IGNORECASE)
ICD10_PATTERN = re.compile(r"\b([A-Z]\d{2}(?:\.\d)?)\b")
BP_PATTERN = re.compile(r"\b(\d{2,3})\s*/\s*(\d{2,3})\b")
HBA1C_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*mmol/mol\b", re.IGNORECASE)
NHS_NUMBER_PATTERN = re.compile(r"\b\d{3}[\s-]?\d{3}[\s-]?\d{4}\b")


def extract_waiting_weeks(messages):
    found = []
    for message in messages:
        # findall returns every match, so multi-mention messages all count.
        found.extend(int(value) for value in WEEKS_PATTERN.findall(message))
    return found


def extract_icd10_codes(text):
    return ICD10_PATTERN.findall(text)


def extract_blood_pressure(text):
    return [
        (int(systolic), int(diastolic))
        for systolic, diastolic in BP_PATTERN.findall(text)
    ]


def extract_hba1c(text):
    return [float(value) for value in HBA1C_PATTERN.findall(text)]


def redact_nhs_numbers(text, placeholder="[NHS NUMBER]"):
    return NHS_NUMBER_PATTERN.sub(placeholder, text)


# Three details in the exam data that a first-pass regex gets wrong:
#
#   1. "I'm committed to veganism" - \bvegan\b does not match "veganism",
#      because the \b needs a non-word character after the n. Use vegan\w*.
#   2. "I don't eat any animal products" - vegan by description, but the word
#      "vegan" never appears, and the apostrophe is a curly one (U+2019).
#   3. Negation has to be tested before the positive rule, or "not vegan"
#      matches on the word "vegan" alone.
#
# What cannot be fixed: the data labels "I am mostly vegan but sometimes I eat
# meat" as Omnivore, while "I see myself as vegan but I do eat meat sometimes"
# is labelled Vegan. The two descriptions say the same thing and carry
# opposite labels, so no rule gets both right. Say so in the exam - noticing
# that the ground truth is inconsistent is the point of the comparison, and
# the marks are for the honest account rather than a suspiciously perfect
# accuracy.

APOSTROPHE = "[\u2019']"

NOT_VEGAN_PATTERN = re.compile(
    r"\b(?:not|never|no\s+longer|anything\s+but|other\s+than|except)\b"
    r"[^.;]{0,30}\bvegan\w*"
    r"|\b(?:used\s+to\s+be|was|previously|formerly)\b[^.;]{0,20}\bvegan\w*",
    re.IGNORECASE,
)

VEGAN_PATTERN = re.compile(
    r"\bvegan\w*"
    r"|\bplant[\s-]?based\b"
    r"|\b(?:don" + APOSTROPHE + r"?t|do\s+not|never|avoid|no)\b"
    r"[^.;]{0,25}\banimal\s+(?:products|produce|derived)\b"
    r"|\bonly\s+(?:eat\s+)?plants\b",
    re.IGNORECASE,
)


def classify_vegan(description):
    if not isinstance(description, str):
        return False
    if NOT_VEGAN_PATTERN.search(description):
        return False
    return bool(VEGAN_PATTERN.search(description))


def classification_agreement(df, description_column, label_column,
                             positive_label="Vegan"):
    predicted = df[description_column].apply(classify_vegan)
    actual = df[label_column] == positive_label
    agree = int((predicted == actual).sum())
    return {
        "n": int(len(df)),
        "agree": agree,
        "accuracy": agree / len(df) if len(df) else float("nan"),
        "false_positives": int((predicted & ~actual).sum()),
        "false_negatives": int((~predicted & actual).sum()),
    }
