def estimate_diagnostic_cost(
    tests,
    additional_charges=0,
    home_collection_charge=0,
    discount_percentage=0,
    tax_percentage=0
):
    if not tests:
        raise ValueError("At least one diagnostic test is required.")

    if additional_charges < 0 or home_collection_charge < 0:
        raise ValueError("Additional charges cannot be negative.")

    if not 0 <= discount_percentage <= 100:
        raise ValueError("Discount percentage must be between 0 and 100.")

    if not 0 <= tax_percentage <= 100:
        raise ValueError("Tax percentage must be between 0 and 100.")

    test_details = []
    test_subtotal = 0

    for test in tests:
        if "test_name" not in test or "price" not in test:
            raise ValueError(
                "Each test must contain test_name and price."
            )

        test_name = test["test_name"]
        price = float(test["price"])

        if price < 0:
            raise ValueError("Test prices cannot be negative.")

        test_details.append({
            "test_name": test_name,
            "price": round(price, 2)
        })

        test_subtotal += price

    subtotal = (
        test_subtotal
        + additional_charges
        + home_collection_charge
    )

    discount_amount = subtotal * discount_percentage / 100
    discounted_amount = subtotal - discount_amount

    tax_amount = discounted_amount * tax_percentage / 100

    final_total = discounted_amount + tax_amount

    return {
        "tests": test_details,
        "test_subtotal": round(test_subtotal, 2),
        "additional_charges": round(additional_charges, 2),
        "home_collection_charge": round(home_collection_charge, 2),
        "subtotal": round(subtotal, 2),
        "discount_percentage": discount_percentage,
        "discount_amount": round(discount_amount, 2),
        "tax_percentage": tax_percentage,
        "tax_amount": round(tax_amount, 2),
        "estimated_total": round(final_total, 2),
        "currency": "INR",
        "calculation_method": "Rule-based cost calculation",
        "requires_centre_price_confirmation": True
    }