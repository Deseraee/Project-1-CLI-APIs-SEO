# main.py - OutSafe Golf CLI

from datetime import datetime

from database import get_last_login, login_user, save_report, view_recent_reports
from recommender import check_state_input, get_round_hours, get_sunscreen_reapply_count, get_golf_recommendation, find_better_tee_window, build_golf_summary
from weather_api import get_coordinates, get_weather, get_uv, get_aqi, get_forecast_list


def choose_holes():
    print("\nHow many holes are you playing?")
    print("1. 9 holes")
    print("2. 18 holes")

    choice = input("Choice: ")

    if choice == "1":
        return "9 holes"
    elif choice == "2":
        return "18 holes"
    else:
        return None


def choose_vehicle():
    print("\nAre you walking or using a cart?")
    print("1. Walking")
    print("2. Cart")

    choice = input("Choice: ")

    if choice == "1":
        return "walking"
    elif choice == "2":
        return "cart"
    else:
        return None


username = input("Enter your username: ")
username = username.strip()

if username == "":
    username = "guest"

login_time = datetime.now().strftime("%Y-%m-%d %I:%M %p").replace(" 0", " ")
last_login = get_last_login(username)
login_user(username, login_time)

print("Welcome,", username + "!")

if last_login is None:
    print("This is your first time using OutSafe Golf.")
else:
    print("Last login:", last_login)

print("Current login:", login_time)


while True:
    print("\nWelcome to OutSafe Golf")
    print("1. Check golf safety")
    print("2. View recent reports")
    print("3. Exit")

    menu_choice = input("Choose an option: ")

    if menu_choice == "1":
        city = input("\nEnter your city: ")
        state = input("Enter your state abbreviation, like OH or GA: ")

        city = city.strip()
        state = state.strip().upper()

        if city == "" or state == "":
            print("City and state cannot be blank.")
            continue

        if check_state_input(state) == False:
            print("State should be a 2-letter abbreviation, like OH or GA.")
            continue

        location = city + "," + state + ",US"
        display_location = city + ", " + state

        holes = choose_holes()

        if holes is None:
            print("Invalid choice for holes.")
            continue

        vehicle = choose_vehicle()

        if vehicle is None:
            print("Invalid choice for walking/cart.")
            continue

        print("\nGetting golf conditions...")

        try:
            report_time = datetime.now().strftime("%Y-%m-%d %I:%M %p").replace(" 0", " ")

            lat, lon = get_coordinates(location)

            temp, description, humidity = get_weather(location)
            uv = get_uv(lat, lon)
            aqi = get_aqi(lat, lon)

            forecast_list = get_forecast_list(location)
            next_forecast = forecast_list[0]

            forecast_time = next_forecast["time"]
            forecast_temp = next_forecast["temp"]
            forecast_description = next_forecast["description"]

            round_hours = get_round_hours(holes)
            sunscreen_count = get_sunscreen_reapply_count(holes, uv)

            verdict, reasons, score = get_golf_recommendation(
                temp,
                aqi,
                uv,
                holes,
                vehicle,
                description
            )

            better_tee_window = find_better_tee_window(
                forecast_list,
                holes,
                vehicle,
                score,
                aqi,
                uv
            )

            better_tee_time = "None found"
            better_tee_temp = None
            better_tee_weather = "None found"

            if better_tee_window is not None:
                better_tee_time = better_tee_window["time"]
                better_tee_temp = better_tee_window["temp"]
                better_tee_weather = better_tee_window["description"]

            summary = build_golf_summary(
                verdict,
                holes,
                vehicle,
                round_hours,
                sunscreen_count,
                better_tee_window
            )

            print("\nOutSafe Golf Report")
            print("--------------------")
            print("Username:", username)
            print("Report Time:", report_time)
            print("Location:", display_location)
            print("Round:", holes)
            print("Travel:", vehicle)
            print("Estimated Exposure:", round_hours, "hours")

            print("\nCurrent Conditions")
            print("--------------------")
            print("Temperature:", round(temp, 1), "°F")
            print("Weather:", description)
            print("Humidity:", humidity, "%")
            print("AQI:", aqi)
            print("UV Index:", round(uv, 1))

            print("\nGolf Verdict:", verdict)

            print("\nReasons:")
            for reason in reasons:
                print("-", reason)

            print("\nSunscreen Reminder:")
            if sunscreen_count == 0:
                print("- UV is low, but sunscreen is still helpful for a long round.")
            else:
                print("- Apply sunscreen before tee time.")
                print("- Reapply about", sunscreen_count, "time(s) during the round.")

            print("\nNext Forecast:")
            print("Time:", forecast_time)
            print("Temperature:", round(forecast_temp, 1), "°F")
            print("Weather:", forecast_description)

            print("\nBetter Tee Window:")
            if better_tee_window is not None:
                print("A better tee window may be", better_tee_time)
                print("Temperature:", round(better_tee_temp, 1), "°F")
                print("Weather:", better_tee_weather)
            else:
                print("No clearly better tee window was found during normal golf hours.")

            print("\nGolf Recommendation:")
            print(summary)

            save_report(
                username,
                display_location,
                holes,
                vehicle,
                report_time,
                temp,
                description,
                humidity,
                aqi,
                uv,
                verdict,
                reasons,
                forecast_time,
                forecast_temp,
                forecast_description,
                better_tee_time,
                better_tee_temp,
                better_tee_weather,
                summary
            )

            print("\nReport saved to database.")

        except Exception as error:
            print("\nSomething went wrong.")
            print("Error:", error)
            print("Try using a US city and state, like Columbus and OH.")

    elif menu_choice == "2":
        reports = view_recent_reports(username)

        print("\nRecent Golf Reports")
        print("--------------------")

        if len(reports) == 0:
            print("No reports found for this username.")
        else:
            for report in reports:
                location = report[0]
                holes = report[1]
                vehicle = report[2]
                report_time = report[3]
                temp = report[4]
                aqi = report[5]
                uv = report[6]
                verdict = report[7]
                better_tee_time = report[8]

                print(location, "|", holes, "|", vehicle, "|", report_time)
                print("Temp:", round(temp, 1), "°F | AQI:", aqi, "| UV:", round(uv, 1), "|", verdict)
                print("Better tee window:", better_tee_time)
                print("")

    elif menu_choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")