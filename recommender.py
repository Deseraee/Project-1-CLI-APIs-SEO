# recommender.py - decides if an outdoor activity is safe

def get_recommendation(activity, temp, aqi, uv):
    activity = activity.lower()

    score = 0
    reasons = []

    # Air quality
    if aqi >= 150:
        score += 3
        reasons.append("Air quality is unhealthy")
    elif aqi >= 100:
        score += 2
        reasons.append("Air quality may be unhealthy for sensitive people")
    elif aqi >= 50:
        score += 1
        reasons.append("Air quality is moderate")

    # UV index
    if uv >= 8:
        score += 2
        reasons.append("UV index is very high")
    elif uv >= 6:
        score += 1
        reasons.append("UV index is high")

    # Temperature
    if temp >= 95:
        score += 2
        reasons.append("Temperature is very hot")
    elif temp >= 85:
        score += 1
        reasons.append("Temperature is hot")

    # Activity-specific risks
    if activity == "golf" and uv >= 6:
        score += 1
        reasons.append("Golf usually means long sun exposure")

    if activity == "run" and aqi >= 100:
        score += 1
        reasons.append("Running is harder on the lungs when air quality is poor")

    if not reasons:
        reasons.append("Conditions look generally safe")

    # Final verdict
    if score <= 2:
        verdict = "GOOD"
    elif score <= 5:
        verdict = "CAUTION"
    else:
        verdict = "AVOID"

    return verdict, reasons