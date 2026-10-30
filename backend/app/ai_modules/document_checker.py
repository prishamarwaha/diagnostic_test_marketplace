from typing import List


def check_document_completeness(
    required_documents: List[str],
    provided_documents: List[str],
    unreadable_documents: List[str] = None
):
    """
    Check whether all required appointment documents
    have been provided and are readable.

    This checks document completeness only.
    It does not verify clinical validity.
    """

    if not required_documents:
        raise ValueError("Required documents list cannot be empty.")

    if unreadable_documents is None:
        unreadable_documents = []

    # Normalize document names for comparison
    required = {
        doc.strip().casefold(): doc.strip()
        for doc in required_documents
        if doc and doc.strip()
    }

    provided = {
        doc.strip().casefold(): doc.strip()
        for doc in provided_documents
        if doc and doc.strip()
    }

    unreadable = {
        doc.strip().casefold(): doc.strip()
        for doc in unreadable_documents
        if doc and doc.strip()
    }

    missing_documents = []
    unreadable_required_documents = []
    available_documents = []

    for normalized_name, original_name in required.items():

        if normalized_name not in provided:
            missing_documents.append(original_name)

        elif normalized_name in unreadable:
            unreadable_required_documents.append(original_name)

        else:
            available_documents.append(original_name)

    total_required = len(required)
    total_complete = len(available_documents)

    is_complete = (
        len(missing_documents) == 0
        and len(unreadable_required_documents) == 0
    )

    if is_complete:
        status = "complete"
        message = "All required documents have been provided and marked readable."

    else:
        status = "incomplete"
        message = "Some required documents are missing or need attention."

    return {
        "status": status,
        "message": message,
        "total_required_documents": total_required,
        "total_complete_documents": total_complete,
        "missing_documents": missing_documents,
        "unreadable_documents": unreadable_required_documents,
        "available_documents": available_documents,
        "requires_manual_verification": True,
        "clinical_validity_checked": False
    }