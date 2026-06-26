# recommender.py - decides if an outdoor activity is safe

def get_recommendation(activity, temp, aqi, uv, time, vehicle):
    activity = activity.lower()
    vehicle = vehicle.lower()

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

    #Time 
    if vehicle == 'y':
      if time <= 2:
        score += 1
        reasons.append("Low risk because it is a short round with vehicle")
      elif time <= 4:
        score +=1
        reasons.append("Medium risk because it is a medium round with a vehicle")
      else:
        score += 0
        reasons.append("Feasible because it is a long round with a vehicle")
    else: 
      if time <= 2: 
        score +=1
        reasons.append("Acceptable risk because it is a short round with no vehicle")
      elif time <=4:
        score +=2
        reasons.append("Moderate risk because it is a 2-4 hour round with no vehicle")
      else:
        score +=3
        reasons.append("High risk, consider rescheduling because there is no vehicle for a long round")

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
