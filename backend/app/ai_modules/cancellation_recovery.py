def simulate_cancellation_recovery(
    cancelled_slots,
    waitlist
):
    if not cancelled_slots:
        raise ValueError("At least one cancelled slot is required.")

    if not waitlist:
        raise ValueError("Waitlist cannot be empty.")

    assigned_patients = []
    unfilled_slots = []

    # Process cancelled slots one by one.
    for slot in cancelled_slots:

        required_fields = [
            "slot_id",
            "centre_name",
            "test_name",
            "appointment_time"
        ]

        for field in required_fields:
            if field not in slot:
                raise ValueError(
                    f"Cancelled slot is missing field: {field}"
                )

        eligible_patients = []

        for patient in waitlist:
            patient_fields = [
                "patient_id",
                "patient_name",
                "preferred_tests",
                "available_times",
                "priority"
            ]

            for field in patient_fields:
                if field not in patient:
                    raise ValueError(
                        f"Waitlist record is missing field: {field}"
                    )

            test_matches = any(
                test.casefold() == slot["test_name"].casefold()
                for test in patient["preferred_tests"]
            )

            time_matches = (
                slot["appointment_time"] in patient["available_times"]
            )

            if test_matches and time_matches:
                eligible_patients.append(patient)

        if not eligible_patients:
            unfilled_slots.append(slot["slot_id"])
            continue

        # Higher priority patients are considered first.
        eligible_patients.sort(
            key=lambda patient: patient["priority"],
            reverse=True
        )

        selected_patient = eligible_patients[0]

        assigned_patients.append({
            "slot_id": slot["slot_id"],
            "centre_name": slot["centre_name"],
            "test_name": slot["test_name"],
            "appointment_time": slot["appointment_time"],
            "assigned_patient_id": selected_patient["patient_id"],
            "assigned_patient_name": selected_patient["patient_name"],
            "priority": selected_patient["priority"],
            "status": "offer_recommended"
        })

        # Remove the selected patient to prevent duplicate allocation.
        waitlist.remove(selected_patient)

    total_slots = len(cancelled_slots)
    recovered_slots = len(assigned_patients)

    return {
        "total_cancelled_slots": total_slots,
        "recovered_slots": recovered_slots,
        "unfilled_slots": unfilled_slots,
        "recovery_percentage": round(
            (recovered_slots / total_slots) * 100, 2
        ),
        "recommended_offers": assigned_patients,
        "simulation_method": "Priority-based waitlist matching",
        "patient_confirmation_required": True
    }