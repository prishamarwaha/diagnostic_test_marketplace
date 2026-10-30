import math
from datetime import datetime, timedelta


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two geographic coordinates in km."""

    earth_radius = 6371

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius * c


def optimize_journey(
    appointments,
    starting_latitude,
    starting_longitude,
    average_speed_kmph=30
):
    """
    Optimise a patient's multi-centre appointment journey.

    Each appointment must contain:
    centre_name, latitude, longitude, appointment_time.

    Appointment time format: YYYY-MM-DD HH:MM
    """

    if not appointments:
        raise ValueError("At least one appointment is required.")

    if average_speed_kmph <= 0:
        raise ValueError("Average speed must be greater than zero.")

    if not (-90 <= starting_latitude <= 90):
        raise ValueError("Invalid starting latitude.")

    if not (-180 <= starting_longitude <= 180):
        raise ValueError("Invalid starting longitude.")

    parsed_appointments = []

    for appointment in appointments:
        try:
            latitude = float(appointment["latitude"])
            longitude = float(appointment["longitude"])

            if not (-90 <= latitude <= 90):
                raise ValueError("Invalid appointment latitude.")

            if not (-180 <= longitude <= 180):
                raise ValueError("Invalid appointment longitude.")

            appointment_time = datetime.strptime(
                appointment["appointment_time"],
                "%Y-%m-%d %H:%M"
            )

            parsed_appointments.append({
                "centre_name": appointment["centre_name"],
                "latitude": latitude,
                "longitude": longitude,
                "appointment_time": appointment_time
            })

        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(
                f"Invalid appointment details: {str(error)}"
            )

    # Start from the patient's current location
    current_latitude = starting_latitude
    current_longitude = starting_longitude

    current_time = min(
        appointment["appointment_time"]
        for appointment in parsed_appointments
    ) - timedelta(days=1)

    remaining = parsed_appointments.copy()
    journey = []

    total_distance = 0
    total_travel_minutes = 0

    while remaining:

        feasible = []

        for appointment in remaining:

            distance = calculate_distance(
                current_latitude,
                current_longitude,
                appointment["latitude"],
                appointment["longitude"]
            )

            travel_minutes = math.ceil(
                (distance / average_speed_kmph) * 60
            )

            estimated_arrival = current_time + timedelta(
                minutes=travel_minutes
            )

            if estimated_arrival <= appointment["appointment_time"]:
                feasible.append((
                    distance,
                    travel_minutes,
                    appointment,
                    estimated_arrival
                ))

        if not feasible:
            break

        # Select the nearest appointment among feasible appointments
        feasible.sort(key=lambda item: item[0])

        distance, travel_minutes, appointment, arrival = feasible[0]

        journey.append({
            "visit_number": len(journey) + 1,
            "centre_name": appointment["centre_name"],
            "distance_from_previous_stop_km": round(distance, 2),
            "estimated_travel_minutes": travel_minutes,
            "estimated_arrival_time": arrival.strftime(
                "%Y-%m-%d %H:%M"
            ),
            "appointment_time": appointment[
                "appointment_time"
            ].strftime("%Y-%m-%d %H:%M"),
            "status": "feasible"
        })

        total_distance += distance
        total_travel_minutes += travel_minutes

        current_latitude = appointment["latitude"]
        current_longitude = appointment["longitude"]
        current_time = appointment["appointment_time"]

        remaining.remove(appointment)

    return {
        "total_appointments": len(parsed_appointments),
        "scheduled_appointments": len(journey),
        "unscheduled_appointments": [
            appointment["centre_name"]
            for appointment in remaining
        ],
        "journey": journey,
        "total_distance_km": round(total_distance, 2),
        "total_travel_minutes": total_travel_minutes,
        "optimization_method": "nearest_feasible_appointment",
        "requires_manual_review": bool(remaining),
        "live_traffic_used": False
    }