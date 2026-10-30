import re


MEDICAL_TERMS = {
    "cbc": {
        "full_form": "Complete Blood Count",
        "simple_explanation": (
            "A blood test that checks red blood cells, "
            "white blood cells and platelets."
        ),
        "purpose": "Helps assess anaemia, infections and other blood-related conditions."
    },
    "complete blood count": {
        "full_form": "Complete Blood Count",
        "simple_explanation": (
            "A blood test that checks red blood cells, "
            "white blood cells and platelets."
        ),
        "purpose": "Helps assess anaemia, infections and other blood-related conditions."
    },
    "fbs": {
        "full_form": "Fasting Blood Sugar",
        "simple_explanation": (
            "Measures blood glucose after a period of fasting."
        ),
        "purpose": "Used to screen for and monitor diabetes."
    },
    "fasting blood sugar": {
        "full_form": "Fasting Blood Sugar",
        "simple_explanation": (
            "Measures blood glucose after a period of fasting."
        ),
        "purpose": "Used to screen for and monitor diabetes."
    },
    "ppbs": {
        "full_form": "Post Prandial Blood Sugar",
        "simple_explanation": (
            "Measures blood glucose after a meal."
        ),
        "purpose": "Helps assess how the body handles glucose after eating."
    },
    "rbs": {
        "full_form": "Random Blood Sugar",
        "simple_explanation": (
            "Measures blood glucose at any time, without requiring fasting."
        ),
        "purpose": "Provides a snapshot of blood glucose levels."
    },
    "hba1c": {
        "full_form": "Glycated Haemoglobin",
        "simple_explanation": (
            "Estimates your average blood sugar over approximately "
            "the previous 2 to 3 months."
        ),
        "purpose": "Used to screen for and monitor diabetes."
    },
    "lft": {
        "full_form": "Liver Function Test",
        "simple_explanation": (
            "A group of blood tests that measure substances related "
            "to liver function and health."
        ),
        "purpose": "Helps assess possible liver problems."
    },
    "kft": {
        "full_form": "Kidney Function Test",
        "simple_explanation": (
            "A group of tests that help assess how well the kidneys work."
        ),
        "purpose": "Helps evaluate kidney health."
    },
    "rft": {
        "full_form": "Renal Function Test",
        "simple_explanation": (
            "A group of tests that help assess kidney function."
        ),
        "purpose": "Helps evaluate kidney health."
    },
    "tft": {
        "full_form": "Thyroid Function Test",
        "simple_explanation": (
            "Blood tests that measure thyroid-related hormone levels."
        ),
        "purpose": "Helps assess whether the thyroid is overactive or underactive."
    },
    "tsh": {
        "full_form": "Thyroid Stimulating Hormone",
        "simple_explanation": (
            "A blood test measuring a hormone that helps regulate "
            "the thyroid gland."
        ),
        "purpose": "Helps evaluate thyroid function."
    },
    "lipid profile": {
        "full_form": "Lipid Profile",
        "simple_explanation": (
            "A blood test that measures cholesterol and triglyceride levels."
        ),
        "purpose": "Helps assess cardiovascular risk."
    },
    "ecg": {
        "full_form": "Electrocardiogram",
        "simple_explanation": (
            "A test that records the electrical activity of the heart."
        ),
        "purpose": "Helps assess heart rate and rhythm."
    },
    "urine routine": {
        "full_form": "Urine Routine Examination",
        "simple_explanation": (
            "Examines a urine sample for physical, chemical "
            "and microscopic findings."
        ),
        "purpose": "Can help identify signs of urinary or kidney-related problems."
    },
    "urine culture": {
        "full_form": "Urine Culture",
        "simple_explanation": (
            "A laboratory test that checks whether microorganisms "
            "grow in a urine sample."
        ),
        "purpose": "Helps investigate a possible urinary tract infection."
    },
    "usg abdomen": {
        "full_form": "Ultrasound Abdomen",
        "simple_explanation": (
            "Uses sound waves to create images of organs inside the abdomen."
        ),
        "purpose": "Helps examine abdominal organs."
    },
    "x-ray chest": {
        "full_form": "Chest X-ray",
        "simple_explanation": (
            "An imaging test that creates pictures of the chest, "
            "including the lungs and heart."
        ),
        "purpose": "Helps examine the lungs, heart and chest structures."
    }
}


def normalize_term(term):
    term = term.lower().strip()
    term = re.sub(r"[^a-z0-9\s-]", "", term)
    term = re.sub(r"\s+", " ", term)
    return term


def simplify_medical_term(term):

    if not term or not term.strip():
        raise ValueError("Medical term cannot be empty.")

    normalized_term = normalize_term(term)

    information = MEDICAL_TERMS.get(normalized_term)

    if not information:
        return {
            "original_term": term,
            "found": False,
            "message": (
                "This term is not available in our current "
                "medical terminology dictionary."
            ),
            "requires_review": True
        }

    return {
        "original_term": term,
        "found": True,
        "full_form": information["full_form"],
        "simple_explanation": information["simple_explanation"],
        "purpose": information["purpose"],
        "requires_review": False
    }


def simplify_multiple_terms(terms):

    if not terms:
        raise ValueError("Please provide at least one medical term.")

    results = [
        simplify_medical_term(term)
        for term in terms
    ]

    return {
        "total_terms": len(results),
        "terms_found": sum(
            1 for result in results if result["found"]
        ),
        "terms_not_found": sum(
            1 for result in results if not result["found"]
        ),
        "results": results
    }