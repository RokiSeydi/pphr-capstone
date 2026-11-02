"""Week 6 - Regular expressions on clinical free text.

Exam archetype: Q6 (10 marks) - extract every waiting time in weeks from a
list of patient messages, ignoring the distractors (days, "don't remember").
"""
import re


def extract_waiting_weeks(messages):
    """Extract every waiting time quoted in weeks.

    Rules:
        - a number followed by "week" or "weeks" counts
        - a number followed by any other unit (days, months) does not
        - a message may contain more than one, and all of them count
        - a message with none contributes nothing

    Example:
        ["I waited 13 weeks.", "I only waited for 25 days."] -> [13]

    :param messages: list of free-text strings
    :return: flat list of ints, in the order encountered
    """
    raise NotImplementedError


def extract_icd10_codes(text):
    """Extract ICD-10 codes from free text.

    An ICD-10 code is one capital letter, two digits, and optionally a dot
    plus one more digit: F20, E11.9, I21.

    :param text: free-text string
    :return: list of code strings, in order, duplicates kept
    """
    raise NotImplementedError


def extract_blood_pressure(text):
    """Extract blood pressure readings written as systolic/diastolic.

    Match two to three digits, a slash, then two to three digits.
    Return them as (systolic, diastolic) integer pairs.

    Example:
        "BP was 140/90, later 128/82" -> [(140, 90), (128, 82)]

    :param text: free-text string
    :return: list of (int, int) tuples
    """
    raise NotImplementedError


def extract_hba1c(text):
    """Extract HbA1c values in mmol/mol from clinic notes.

    The number may have a decimal part, and the unit may be written
    "mmol/mol" with any amount of whitespace before it.

    Example:
        "HbA1c 58 mmol/mol, previously 62.5mmol/mol" -> [58.0, 62.5]

    :param text: free-text string
    :return: list of floats
    """
    raise NotImplementedError


def redact_nhs_numbers(text, placeholder="[NHS NUMBER]"):
    """Replace NHS numbers with a placeholder.

    An NHS number is ten digits, optionally grouped 3-3-4 with spaces or
    hyphens: "4857773456", "485 777 3456", "485-777-3456".

    :param text: free-text string
    :param placeholder: what to substitute in
    :return: the text with every NHS number replaced
    """
    raise NotImplementedError


# --- Classifying free text (Sep 2025 Q10, 15 marks) --------------------------
# The paper gives short self-descriptions of diet and asks you to pick out the
# vegans with regex, then check your labels against the recorded ones. The
# marks are in handling negation ("I used to be vegan", "anything but vegan")
# and in honestly reporting where your rule disagrees with the data.


def classify_vegan(description):
    """Decide from a free-text diet description whether someone is vegan.

    Treat it as vegan when the text asserts a vegan or plant-only diet, and
    not vegan when the mention is negated or in the past - "not vegan",
    "no longer vegan", "used to be vegan", "anything but vegan".

    Match case-insensitively, and watch for three things in the real data:
        - "committed to veganism" - \bvegan\b will not match "veganism"
        - "I don't eat any animal products" - vegan, but never says "vegan",
          and the apostrophe is a curly one (U+2019)
        - test the negations before the positive rule, or "not vegan" matches
          on the word "vegan" alone

    :param description: free-text diet description
    :return: bool
    """
    raise NotImplementedError


def classification_agreement(df, description_column, label_column,
                             positive_label="Vegan"):
    """Compare a regex classification against the recorded diet labels.

    Apply classify_vegan to `description_column` and compare with
    `label_column == positive_label`.

    :param df: DataFrame with the descriptions and the recorded labels
    :param description_column: free-text column, e.g. "Diet_description"
    :param label_column: recorded label column, e.g. "Diet"
    :return: dict with keys "n", "agree", "accuracy",
             "false_positives", "false_negatives"
    """
    raise NotImplementedError
