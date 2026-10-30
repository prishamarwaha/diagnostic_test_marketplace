import re


def extract_invoice_details(invoice_text):
    if not invoice_text or not invoice_text.strip():
        raise ValueError("Invoice text cannot be empty.")

    lines = [
        line.strip()
        for line in invoice_text.splitlines()
        if line.strip()
    ]

    # Find monetary amounts such as ₹500, Rs. 750, INR 1,200.
    amount_pattern = re.compile(
        r"(?:₹|Rs\.?|INR)\s*([\d,]+(?:\.\d{1,2})?)",
        re.IGNORECASE
    )

    extracted_items = []
    extracted_amounts = []

    for line in lines:
        amounts = amount_pattern.findall(line)

        for amount in amounts:
            numeric_amount = float(amount.replace(",", ""))
            extracted_amounts.append(numeric_amount)

        if amounts:
            # Remove monetary values to retain the item description.
            description = amount_pattern.sub("", line)
            description = re.sub(r"[-:|]+$", "", description).strip()

            if description:
                extracted_items.append({
                    "description": description,
                    "extracted_amounts": [
                        float(amount.replace(",", ""))
                        for amount in amounts
                    ]
                })

    # Identify possible invoice totals.
    total_pattern = re.compile(
        r"(grand\s*total|invoice\s*total|total\s*amount|net\s*amount)"
        r"\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d{1,2})?)",
        re.IGNORECASE
    )

    invoice_total = None

    for line in lines:
        match = total_pattern.search(line)

        if match:
            invoice_total = float(
                match.group(2).replace(",", "")
            )

    # Identify possible discounts and taxes.
    discount_lines = [
        line for line in lines
        if "discount" in line.casefold()
    ]

    tax_lines = [
        line for line in lines
        if any(
            term in line.casefold()
            for term in ["gst", "tax"]
        )
    ]

    return {
        "extracted_items": extracted_items,
        "all_extracted_amounts": extracted_amounts,
        "invoice_total": invoice_total,
        "discount_details": discount_lines,
        "tax_details": tax_lines,
        "items_found": len(extracted_items),
        "requires_manual_verification": True,
        "extraction_method": "Rule-based text extraction",
        "note": (
            "Extracted amounts and descriptions must be checked against "
            "the original invoice or tariff document."
        )
    }