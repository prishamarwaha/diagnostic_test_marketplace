def assess_equipment_risk(
    equipment_name,
    days_since_maintenance,
    usage_hours,
    average_daily_usage,
    fault_count,
    critical_fault_count,
    temperature_deviation,
    calibration_overdue
):
    if days_since_maintenance < 0:
        raise ValueError("Days since maintenance cannot be negative.")

    if usage_hours < 0 or average_daily_usage < 0:
        raise ValueError("Usage hours cannot be negative.")

    if fault_count < 0 or critical_fault_count < 0:
        raise ValueError("Fault counts cannot be negative.")

    if critical_fault_count > fault_count:
        raise ValueError(
            "Critical fault count cannot exceed total fault count."
        )

    if temperature_deviation < 0:
        raise ValueError("Temperature deviation cannot be negative.")

    risk_score = 0
    contributing_factors = []

    # 1. Time since last maintenance
    if days_since_maintenance > 90:
        risk_score += 25
        contributing_factors.append(
            "Maintenance overdue by more than 90 days."
        )
    elif days_since_maintenance > 30:
        risk_score += 15
        contributing_factors.append(
            "Maintenance was performed more than 30 days ago."
        )

    # 2. Total equipment usage
    if usage_hours > 5000:
        risk_score += 20
        contributing_factors.append(
            "Equipment has very high accumulated usage."
        )
    elif usage_hours > 2000:
        risk_score += 10
        contributing_factors.append(
            "Equipment has high accumulated usage."
        )

    # 3. Average daily usage
    if average_daily_usage > 16:
        risk_score += 10
        contributing_factors.append(
            "Equipment is being used for more than 16 hours daily."
        )

    # 4. Recorded faults
    if fault_count >= 5:
        risk_score += 15
        contributing_factors.append(
            "Multiple equipment faults have been recorded."
        )
    elif fault_count >= 2:
        risk_score += 8
        contributing_factors.append(
            "Equipment has recorded repeated faults."
        )

    # 5. Critical faults
    if critical_fault_count >= 1:
        risk_score += 20
        contributing_factors.append(
            "One or more critical equipment faults have been recorded."
        )

    # 6. Temperature deviation
    if temperature_deviation > 15:
        risk_score += 15
        contributing_factors.append(
            "Equipment temperature is significantly outside its normal range."
        )
    elif temperature_deviation > 5:
        risk_score += 8
        contributing_factors.append(
            "Equipment temperature deviation requires monitoring."
        )

    # 7. Calibration status
    if calibration_overdue:
        risk_score += 15
        contributing_factors.append(
            "Equipment calibration is overdue."
        )

    risk_score = min(risk_score, 100)

    # Risk classification
    if risk_score >= 75:
        risk_level = "critical"
        recommendation = (
            "Arrange immediate technical inspection. "
            "Consider restricting equipment use until assessed."
        )
    elif risk_score >= 50:
        risk_level = "high"
        recommendation = (
            "Schedule maintenance and technical inspection as soon as possible."
        )
    elif risk_score >= 25:
        risk_level = "moderate"
        recommendation = (
            "Monitor equipment condition and schedule preventive maintenance."
        )
    else:
        risk_level = "low"
        recommendation = (
            "Continue routine monitoring and follow the maintenance schedule."
        )

    return {
        "equipment_name": equipment_name,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "contributing_factors": contributing_factors,
        "recommended_action": recommendation,
        "assessment_method": "Rule-based risk scoring",
        "requires_technical_verification": True,
        "note": (
            "This is an MVP risk estimate, not a trained predictive "
            "maintenance model or a substitute for manufacturer guidelines."
        )
    }