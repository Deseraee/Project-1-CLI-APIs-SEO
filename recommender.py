# recommender.py - golf recommendation logic


def check_state_input(state):
    if len(state) == 2 and state.isalpha():
        return True
    return False


def get_round_hours(holes):
    if holes == "9 holes":
        return 2
    return 4.5


def get_sunscreen_reapply_count(holes, uv):
    if uv < 3:
        return 0

    if holes == "9 holes":
        return 1

    return 2


def estimate_future_uv(current_uv, hour):
    if hour <= 8:
        return max(0, current_uv - 4)

    if hour >= 17:
        return max(0, current_uv - 4)

    if hour >= 15:
        return max(0, current_uv - 2)

    return current_uv


def get_golf_recommendation(temp, aqi, uv, holes, vehicle, weather_description):
    weather_description = weather_description.lower()

    if "thunderstorm" in weather_description or "storm" in weather_description:
        return "AVOID OR RESCHEDULE", ["Storms are not safe for golf because of lightning risk"], 99

    score = 0
    reasons = []

    if "rain" in weather_description:
        score += 3
        reasons.append("Rain can make the course uncomfortable or unsafe")
    elif "snow" in weather_description:
        score += 5
        reasons.append("Snow is not good for golf conditions")

    if aqi >= 150:
        score += 5
        reasons.append("Air quality is unhealthy")
    elif aqi >= 100:
        score += 3
        reasons.append("Air quality may be unhealthy for sensitive people")
    elif aqi >= 50:
        score += 1
        reasons.append("Air quality is moderate")

    if uv >= 8:
        score += 4
        reasons.append("UV index is very high")
    elif uv >= 6:
        score += 3
        reasons.append("UV index is high")
    elif uv >= 3:
        score += 1
        reasons.append("UV index is moderate")

    if temp >= 95:
        score += 4
        reasons.append("Temperature is very hot")
    elif temp >= 85:
        score += 2
        reasons.append("Temperature is hot")
    elif temp <= 35:
        score += 2
        reasons.append("Temperature is very cold")

    if holes == "18 holes":
        score += 2
        reasons.append("18 holes means a long time outside")

    if vehicle == "walking":
        score += 2
        reasons.append("Walking adds more physical strain than using a cart")

    if len(reasons) == 0:
        reasons.append("Conditions look generally safe for golf")

    if score <= 2:
        verdict = "GOOD TO PLAY"
    elif score <= 9:
        verdict = "PLAY WITH CAUTION"
    else:
        verdict = "AVOID OR RESCHEDULE"

    return verdict, reasons, score


def find_better_tee_window(forecasts, holes, vehicle, current_score, aqi, current_uv):
    best_forecast = None
    best_score = current_score

    for forecast in forecasts:
        hour = forecast["hour"]
        temp = forecast["temp"]
        description = forecast["description"].lower()

        if hour < 6 or hour > 19:
            continue

        if "storm" in description or "thunderstorm" in description:
            continue

        if "rain" in description or "snow" in description:
            continue

        future_uv = estimate_future_uv(current_uv, hour)

        verdict, reasons, forecast_score = get_golf_recommendation(
            temp,
            aqi,
            future_uv,
            holes,
            vehicle,
            description
        )

        if forecast_score < best_score:
            best_score = forecast_score
            best_forecast = forecast

    return best_forecast


def build_golf_summary(verdict, holes, vehicle, round_hours, sunscreen_count, better_tee_window):
    if verdict == "GOOD TO PLAY":
        summary = "This looks like a good tee time for golf. "
    elif verdict == "PLAY WITH CAUTION":
        summary = "This round is playable, but you should use caution. "
    else:
        summary = "This tee time is not ideal, and rescheduling would be a smart choice. "

    summary += "You are planning to play " + holes + ", which is about " + str(round_hours) + " hours outside. "

    if vehicle == "walking":
        summary += "Because you are walking, heat, air quality, and long sun exposure matter more. "
    else:
        summary += "Using a cart lowers the physical strain, but sun exposure still matters. "

    if sunscreen_count == 0:
        summary += "UV is low, but sunscreen is still helpful for a long round. "
    else:
        summary += "Apply sunscreen before tee time and reapply about " + str(sunscreen_count) + " time(s) during the round. "

    if better_tee_window is not None:
        summary += "A better tee window may be " + better_tee_window["time"] + " because the forecast looks more comfortable."
    else:
        summary += "No clearly better tee window was found during normal golf hours."

    return summary