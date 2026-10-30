def balance_centre_capacity(
    centres,
    requested_test,
    patient_count=1
):
    if not centres:
        raise ValueError("At least one centre is required.")

    if not requested_test.strip():
        raise ValueError("Requested test cannot be empty.")

    if patient_count < 1:
        raise ValueError("Patient count must be at least 1.")

    centre_results = []

    for centre in centres:
        required_fields = [
            "centre_name",
            "supported_tests",
            "total_capacity",
            "current_bookings",
            "distance_km"
        ]

        for field in required_fields:
            if field not in centre:
                raise ValueError(
                    f"Centre record is missing the field: {field}"
                )

        capacity = centre["total_capacity"]
        bookings = centre["current_bookings"]
        distance = centre["distance_km"]

        if capacity < 0 or bookings < 0 or distance < 0:
            raise ValueError(
                "Capacity, bookings and distance cannot be negative."
            )

        if bookings > capacity:
            raise ValueError(
                f"Current bookings exceed capacity at {centre['centre_name']}."
            )

        supports_test = any(
            requested_test.casefold() == test.strip().casefold()
            for test in centre["supported_tests"]
        )

        if not supports_test:
            continue

        available_capacity = capacity - bookings
        utilisation = (
            (bookings / capacity) * 100 if capacity > 0 else 100
        )

        can_accommodate = available_capacity >= patient_count

        centre_results.append({
            "centre_name": centre["centre_name"],
            "total_capacity": capacity,
            "current_bookings": bookings,
            "available_capacity": available_capacity,
            "utilisation_percentage": round(utilisation, 2),
            "distance_km": round(distance, 2),
            "can_accommodate_requested_patients": can_accommodate
        })

    if not centre_results:
        return {
            "requested_test": requested_test,
            "message": "No centre supporting this test was found.",
            "recommended_centres": [],
            "overloaded_centres": []
        }

    # Recommend centres that can accommodate the requested patients.
    recommended = [
        centre for centre in centre_results
        if centre["can_accommodate_requested_patients"]
    ]

    # Prefer lower utilisation, then shorter distance.
    recommended.sort(
        key=lambda centre: (
            centre["utilisation_percentage"],
            centre["distance_km"]
        )
    )

    overloaded = [
        centre for centre in centre_results
        if centre["utilisation_percentage"] >= 90
    ]

    return {
        "requested_test": requested_test,
        "patient_count": patient_count,
        "total_matching_centres": len(centre_results),
        "recommended_centres": recommended,
        "overloaded_centres": overloaded,
        "balancing_method": "Capacity utilisation and distance ranking",
        "requires_centre_confirmation": True
    }