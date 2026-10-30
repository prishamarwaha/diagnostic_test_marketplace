def coordinate_family_appointments(family_members):
    if not family_members:
        raise ValueError("At least one family member is required.")

    required_fields = [
        "member_id",
        "member_name",
        "required_test",
        "preferred_centre",
        "available_times"
    ]

    for member in family_members:
        for field in required_fields:
            if field not in member:
                raise ValueError(
                    f"Family member record is missing: {field}"
                )

        if not member["available_times"]:
            raise ValueError(
                f"No available times provided for {member['member_name']}."
            )

    # Group members by their preferred diagnostic centre.
    centre_groups = {}

    for member in family_members:
        centre = member["preferred_centre"]

        if centre not in centre_groups:
            centre_groups[centre] = []

        centre_groups[centre].append(member)

    coordinated_groups = []
    uncoordinated_members = []

    for centre, members in centre_groups.items():

        # Find time slots available to every member in this centre group.
        common_times = set(members[0]["available_times"])

        for member in members[1:]:
            common_times.intersection_update(
                member["available_times"]
            )

        if common_times:
            selected_time = sorted(common_times)[0]

            coordinated_groups.append({
                "centre_name": centre,
                "appointment_time": selected_time,
                "members": [
                    {
                        "member_id": member["member_id"],
                        "member_name": member["member_name"],
                        "required_test": member["required_test"]
                    }
                    for member in members
                ],
                "coordination_status": "shared_time_available"
            })

        else:
            # Members have no common time.
            for member in members:
                uncoordinated_members.append({
                    "member_id": member["member_id"],
                    "member_name": member["member_name"],
                    "preferred_centre": centre,
                    "available_times": member["available_times"],
                    "reason": "No common appointment time found."
                })

    return {
        "total_family_members": len(family_members),
        "coordinated_groups": coordinated_groups,
        "uncoordinated_members": uncoordinated_members,
        "successfully_coordinated": sum(
            len(group["members"])
            for group in coordinated_groups
        ),
        "coordination_method": "Centre-based common time matching",
        "booking_confirmation_required": True,
        "note": (
            "These are suggested appointment groupings. "
            "Actual centre availability must be confirmed before booking."
        )
    }