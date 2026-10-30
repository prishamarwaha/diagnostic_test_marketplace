def optimize_staff_roster(
    staff_members,
    required_staff,
    expected_patient_count
):
    if not staff_members:
        raise ValueError("At least one staff member is required.")

    if required_staff < 1:
        raise ValueError("Required staff must be at least 1.")

    if expected_patient_count < 0:
        raise ValueError("Expected patient count cannot be negative.")

    eligible_staff = []
    unavailable_staff = []

    for staff in staff_members:
        required_fields = [
            "staff_id",
            "name",
            "available",
            "skills",
            "working_hours"
        ]

        for field in required_fields:
            if field not in staff:
                raise ValueError(
                    f"Staff record is missing the field: {field}"
                )

        if staff["available"] and staff["working_hours"] > 0:
            eligible_staff.append(staff)
        else:
            unavailable_staff.append(staff["name"])

    # Prioritise staff with more relevant skills and available hours.
    eligible_staff.sort(
        key=lambda staff: (
            len(staff["skills"]),
            staff["working_hours"]
        ),
        reverse=True
    )

    selected_staff = eligible_staff[:required_staff]

    if len(selected_staff) < required_staff:
        status = "understaffed"
    else:
        status = "adequately_staffed"

    assigned_staff = []

    for staff in selected_staff:
        assigned_staff.append({
            "staff_id": staff["staff_id"],
            "name": staff["name"],
            "assigned_hours": staff["working_hours"],
            "skills": staff["skills"]
        })

    # Estimate staffing coverage using an assumed planning ratio.
    # This ratio is configurable for an MVP demonstration.
    estimated_capacity_per_staff = 10

    total_capacity = (
        len(selected_staff) * estimated_capacity_per_staff
    )

    if expected_patient_count > total_capacity:
        demand_status = "high_demand"
    else:
        demand_status = "capacity_sufficient"

    return {
        "expected_patient_count": expected_patient_count,
        "required_staff": required_staff,
        "available_eligible_staff": len(eligible_staff),
        "assigned_staff": assigned_staff,
        "unavailable_staff": unavailable_staff,
        "staffing_status": status,
        "estimated_patient_capacity": total_capacity,
        "demand_status": demand_status,
        "unassigned_staff_required": max(
            0, required_staff - len(selected_staff)
        ),
        "optimization_method": "Rule-based staff allocation",
        "requires_manager_approval": True
    }