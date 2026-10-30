from datetime import datetime, timedelta
import math


def calculate_travel_plan(
    distance_km: float,
    appointment_time: str,
    average_speed_kmph: float = 30,
    buffer_minutes: int = 20,
    preparation_minutes: int = 15
):
    """
    Estimate travel duration and recommended departure time.

    appointment_time format: YYYY-MM-DD HH:MM
    """

    if distance_km <= 0:
        raise ValueError("Distance must be greater than zero.")

    if average_speed_kmph <= 0:
        raise ValueError("Average speed must be greater than zero.")

    if buffer_minutes < 0 or preparation_minutes < 0:
        raise ValueError("Time buffers cannot be negative.")

    try:
        appointment = datetime.strptime(
            appointment_time,
            "%Y-%m-%d %H:%M"
        )
    except ValueError:
        raise ValueError(
            "Invalid appointment time. Use YYYY-MM-DD HH:MM."
        )

    travel_minutes = math.ceil(
        (distance_km / average_speed_kmph) * 60
    )

    total_required_minutes = (
        travel_minutes
        + buffer_minutes
        + preparation_minutes
    )

    departure_time = appointment - timedelta(
        minutes=total_required_minutes
    )

    arrival_time = appointment - timedelta(
        minutes=preparation_minutes
    )

    return {
        "distance_km": distance_km,
        "average_speed_kmph": average_speed_kmph,
        "estimated_travel_minutes": travel_minutes,
        "buffer_minutes": buffer_minutes,
        "preparation_minutes": preparation_minutes,
        "appointment_time": appointment.strftime("%Y-%m-%d %H:%M"),
        "estimated_arrival_time": arrival_time.strftime("%Y-%m-%d %H:%M"),
        "recommended_departure_time": departure_time.strftime(
            "%Y-%m-%d %H:%M"
        ),
        "total_required_minutes": total_required_minutes,
        "traffic_data_used": False,
        "estimate_type": "distance_and_average_speed"
    }