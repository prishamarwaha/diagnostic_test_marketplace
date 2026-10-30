
import re
from difflib import SequenceMatcher

from app.services.dataset_service import preprocess_dataset


# Common medical abbreviations and their expanded forms
TEST_ALIASES = {
    "cbc": ["complete blood count", "hemogram"],
    "fbs": ["fasting blood sugar", "fasting glucose"],
    "ppbs": ["post prandial blood sugar", "post meal glucose"],
    "rbs": ["random blood sugar", "random glucose"],
    "lft": ["liver function test", "liver function tests"],
    "kft": ["kidney function test", "renal function test"],
    "rft": ["renal function test"],
    "tft": ["thyroid function test"],
    "tsh": ["thyroid stimulating hormone"],
    "lipid profile": ["lipid panel", "cholesterol profile"],
    "hba1c": ["glycated haemoglobin", "glycated hemoglobin"],
    "urine routine": ["urine examination", "urine analysis"],
    "urine culture": ["urine c and s"],
    "ecg": ["electrocardiogram"],
    "usg abdomen": ["ultrasound abdomen", "sonography abdomen"],
    "x-ray chest": ["chest x ray", "chest radiograph"],
}


def normalize_text(text):
    """Normalize text for matching."""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_test_mentions(prescription_text):
    """Extract known diagnostic test names from prescription text."""

    centres, prices = preprocess_dataset()

    available_tests = (
        prices["Test"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    normalized_prescription = normalize_text(
        prescription_text
    )

    extracted = []

    for test in available_tests:

        normalized_test = normalize_text(test)

        terms = [
            normalized_test
        ] + [
            normalize_text(alias)
            for alias in TEST_ALIASES.get(
                normalized_test, []
            )
        ]

        for term in terms:

            if not term:
                continue

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(term)
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, normalized_prescription):

                extracted.append({
                    "matched_test": test,
                    "matched_term": term,
                    "confidence": 1.0,
                    "match_type": "exact_or_alias"
                })

                break

    # Remove duplicate matches
    unique_results = {}
    for item in extracted:
        unique_results[item["matched_test"]] = item

    return list(unique_results.values())


def get_unmatched_terms(prescription_text, extracted_tests):
    """Return likely investigation terms that were not matched."""

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9-]{2,}\b",
        prescription_text
    )

    matched_terms = {
        normalize_text(item["matched_test"])
        for item in extracted_tests
    }

    ignored_words = {
        "please", "kindly", "patient", "doctor",
        "review", "repeat", "after", "before",
        "fasting", "morning", "daily", "test",
        "tests", "report", "reports"
    }

    unmatched = []

    for word in words:

        normalized = normalize_text(word)

        if normalized in ignored_words:
            continue

        if normalized in matched_terms:
            continue

        if len(normalized) >= 4:
            unmatched.append(word)

    return list(dict.fromkeys(unmatched))


def process_prescription(prescription_text):
    """Main prescription extraction function."""

    if not prescription_text.strip():
        raise ValueError("Prescription text cannot be empty")

    extracted_tests = extract_test_mentions(
        prescription_text
    )

    unmatched_terms = get_unmatched_terms(
        prescription_text,
        extracted_tests
    )

    return {
        "extraction_method": "text_and_medical_alias_matching",
        "total_tests_detected": len(extracted_tests),
        "extracted_tests": extracted_tests,
        "unmatched_terms_for_review": unmatched_terms,
        "requires_clinical_review": True
    }
